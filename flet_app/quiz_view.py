"""Interactive quiz UI for the Flet course navigator."""

from __future__ import annotations

import random
from typing import Callable

import flet as ft

from course_nav.quiz_parser import Quiz, QuizQuestion

_ACCENT = "#1565C0"
_CORRECT = "#2E7D32"
_CORRECT_BG = "#E8F5E9"
_WRONG = "#C62828"
_WRONG_BG = "#FFEBEE"


def build_quiz_controls(
    quiz: Quiz,
    *,
    selections: dict[int, str],
    submitted: bool,
    option_order: dict[int, list[str]],
    on_select: Callable[[int, str], None],
    on_submit: Callable[[], None],
    on_reset: Callable[[], None],
) -> list[ft.Control]:
    controls: list[ft.Control] = []

    if quiz.intro:
        controls.append(
            ft.Text(quiz.intro, size=14, color=ft.Colors.ON_SURFACE_VARIANT)
        )
        controls.append(ft.Divider())

    for question in quiz.questions:
        order = option_order.get(question.number)
        if order is None:
            order = _shuffled_letters(question)
            option_order[question.number] = order
        controls.append(
            _question_card(question, order, selections, submitted, on_select)
        )

    if submitted:
        correct_count = sum(
            1
            for q in quiz.questions
            if selections.get(q.number) == q.correct
        )
        total = len(quiz.questions)
        ratio = correct_count / total if total else 0.0
        message = (
            "Perfect score!"
            if correct_count == total
            else "Good effort!"
            if ratio >= 0.6
            else "Keep studying — review the theory lessons."
        )
        controls.append(
            ft.Container(
                padding=16,
                border_radius=10,
                bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
                content=ft.Column(
                    spacing=6,
                    controls=[
                        ft.Text(
                            f"Score: {correct_count} / {total}",
                            size=20,
                            weight=ft.FontWeight.BOLD,
                        ),
                        ft.ProgressBar(value=ratio, color=_ACCENT),
                        ft.Text(message, size=13, color=ft.Colors.ON_SURFACE_VARIANT),
                    ],
                ),
            )
        )
        controls.append(
            ft.OutlinedButton(
                "Try again",
                icon=ft.Icons.RESTART_ALT,
                on_click=lambda _: on_reset(),
            )
        )
    else:
        answered = sum(1 for q in quiz.questions if q.number in selections)
        total = len(quiz.questions)
        controls.append(
            ft.Text(
                f"Answered {answered} of {total}",
                size=13,
                color=ft.Colors.ON_SURFACE_VARIANT,
            )
        )
        controls.append(
            ft.FilledButton(
                "Check answers",
                icon=ft.Icons.CHECK,
                style=ft.ButtonStyle(bgcolor=_ACCENT),
                disabled=answered < total,
                on_click=lambda _: on_submit(),
            )
        )

    return controls


def _shuffled_letters(question: QuizQuestion) -> list[str]:
    letters = list(question.options.keys())
    random.shuffle(letters)
    return letters


def _question_card(
    question: QuizQuestion,
    display_order: list[str],
    selections: dict[int, str],
    submitted: bool,
    on_select: Callable[[int, str], None],
) -> ft.Control:
    selected = selections.get(question.number)
    is_correct = submitted and selected == question.correct
    is_wrong = submitted and selected is not None and selected != question.correct

    if is_correct:
        border_color = _CORRECT
        header_bg = _CORRECT_BG
        status_icon = ft.Icons.CHECK_CIRCLE
        status_color = _CORRECT
    elif is_wrong:
        border_color = _WRONG
        header_bg = _WRONG_BG
        status_icon = ft.Icons.CANCEL
        status_color = _WRONG
    else:
        border_color = ft.Colors.OUTLINE_VARIANT
        header_bg = ft.Colors.SURFACE_CONTAINER_LOW
        status_icon = None
        status_color = None

    option_controls: list[ft.Control] = []
    for display_idx, orig_letter in enumerate(display_order):
        display_label = chr(ord("A") + display_idx)
        text = question.options[orig_letter]
        label = f"{display_label}. {text}"

        if submitted:
            if orig_letter == question.correct:
                option_controls.append(
                    _result_option(label, _CORRECT_BG, _CORRECT, ft.Icons.CHECK)
                )
            elif orig_letter == selected and orig_letter != question.correct:
                option_controls.append(
                    _result_option(label, _WRONG_BG, _WRONG, ft.Icons.CLOSE)
                )
            else:
                option_controls.append(_result_option(label, None, None, None))
        else:
            option_controls.append(
                ft.Radio(
                    value=orig_letter,
                    label=label,
                    label_style=ft.TextStyle(size=14),
                )
            )

    header_controls: list[ft.Control] = [
        ft.Text(
            f"Question {question.number}",
            size=12,
            weight=ft.FontWeight.W_600,
            color=ft.Colors.ON_SURFACE_VARIANT,
        ),
        ft.Text(question.prompt, size=15, weight=ft.FontWeight.W_500),
    ]
    if submitted and status_icon:
        header_controls.append(
            ft.Row(
                controls=[
                    ft.Icon(status_icon, color=status_color, size=18),
                    ft.Text(
                        "Correct" if is_correct else "Incorrect",
                        color=status_color,
                        weight=ft.FontWeight.W_600,
                        size=13,
                    ),
                ],
                spacing=6,
            )
        )

    body: list[ft.Control]
    if submitted:
        body = option_controls
        if question.explanation:
            body.append(
                ft.Container(
                    padding=12,
                    border_radius=8,
                    bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
                    content=ft.Text(
                        question.explanation,
                        size=13,
                        color=ft.Colors.ON_SURFACE_VARIANT,
                    ),
                )
            )
        elif not is_correct:
            body.append(
                ft.Container(
                    padding=12,
                    border_radius=8,
                    bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
                    content=ft.Text(
                        f"Correct answer: {question.correct}. "
                        f"{question.options.get(question.correct, '')}",
                        size=13,
                        color=ft.Colors.ON_SURFACE_VARIANT,
                    ),
                )
            )
    else:
        body = [
            ft.RadioGroup(
                value=selected,
                content=ft.Column(spacing=4, controls=option_controls),
                on_change=lambda e, n=question.number: on_select(
                    n, (e.data or e.control.value or "")
                ),
            )
        ]

    return ft.Container(
        padding=14,
        border_radius=10,
        bgcolor=header_bg,
        border=ft.Border.all(1.5, border_color),
        content=ft.Column(spacing=10, controls=[*header_controls, *body]),
    )


def _result_option(
    label: str,
    bgcolor: str | None,
    text_color: str | None,
    icon: str | None,
) -> ft.Container:
    row_controls: list[ft.Control] = []
    if icon:
        row_controls.append(ft.Icon(icon, size=16, color=text_color))
    row_controls.append(ft.Text(label, size=14, color=text_color, expand=True))
    return ft.Container(
        padding=ft.Padding.symmetric(horizontal=8, vertical=6),
        border_radius=6,
        bgcolor=bgcolor,
        content=ft.Row(spacing=8, controls=row_controls),
    )
