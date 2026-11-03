"""Parse multiple-choice quiz markdown into structured data."""

from __future__ import annotations

import re
from dataclasses import dataclass, field

QUESTION_START = re.compile(r"^\*\*(\d+)\.\s*(.+?)\*\*\s*$")
QUESTION_START_OPEN = re.compile(r"^\*\*(\d+)\.\*\*\s*(.+)$")
OPTION_BULLET = re.compile(r"^-\s*([A-D])\)\s+(.+)$")
OPTION_PLAIN = re.compile(r"^([A-D])\.\s+(.+)$")
ANSWER_LINE = re.compile(
    r"^(\d+)\.\s+\*\*([A-D])\*\*\s*(?:—|-)\s*(.+)$"
)
COMPACT_ANSWER = re.compile(r"(\d+)\.\s*\*?\*?([A-D])\*?\*?")


@dataclass
class QuizQuestion:
    number: int
    prompt: str
    options: dict[str, str]
    correct: str = ""
    explanation: str = ""


@dataclass
class Quiz:
    title: str
    intro: str = ""
    questions: list[QuizQuestion] = field(default_factory=list)


def _parse_question_block(block: str) -> list[QuizQuestion]:
    questions: list[QuizQuestion] = []
    number: int | None = None
    prompt = ""
    options: dict[str, str] = {}

    def flush() -> None:
        nonlocal number, prompt, options
        if number is not None and options:
            questions.append(
                QuizQuestion(number=number, prompt=prompt, options=dict(options))
            )
        number = None
        prompt = ""
        options = {}

    for line in block.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        q_match = QUESTION_START.match(stripped) or QUESTION_START_OPEN.match(stripped)
        if q_match:
            flush()
            number = int(q_match.group(1))
            prompt = q_match.group(2).strip()
            continue
        for pattern in (OPTION_BULLET, OPTION_PLAIN):
            o_match = pattern.match(stripped)
            if o_match and number is not None:
                options[o_match.group(1)] = o_match.group(2).strip()
                break

    flush()
    return questions


def _parse_first_section(section: str) -> tuple[str, str, list[QuizQuestion]]:
    title = "Quiz"
    body_lines: list[str] = []

    for line in section.splitlines():
        stripped = line.strip()
        if stripped.startswith("# "):
            title = stripped.lstrip("# ").strip()
            continue
        if stripped and stripped != "---":
            body_lines.append(line)

    intro_lines: list[str] = []
    question_lines: list[str] = []
    in_question = False
    for line in body_lines:
        stripped = line.strip()
        if QUESTION_START.match(stripped) or QUESTION_START_OPEN.match(stripped):
            in_question = True
        if in_question:
            question_lines.append(line)
        elif stripped:
            intro_lines.append(stripped)

    intro = "\n".join(intro_lines).strip()
    questions = _parse_question_block("\n".join(question_lines)) if question_lines else []
    return title, intro, questions


def _parse_answers(answer_text: str) -> dict[int, tuple[str, str]]:
    answers: dict[int, tuple[str, str]] = {}

    for line in answer_text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        match = ANSWER_LINE.match(stripped)
        if match:
            answers[int(match.group(1))] = (match.group(2), match.group(3).strip())
            continue
        for num, letter in COMPACT_ANSWER.findall(stripped):
            n = int(num)
            if n not in answers:
                answers[n] = (letter, "")

    return answers


def parse_quiz_markdown(text: str) -> Quiz | None:
    """Parse quiz markdown. Returns None if the text is not a valid quiz."""
    parts = re.split(r"^## Answers\s*$", text, maxsplit=1, flags=re.MULTILINE | re.IGNORECASE)
    if len(parts) != 2:
        return None

    question_text, answer_text = parts[0].strip(), parts[1].strip()
    if not question_text:
        return None

    answers = _parse_answers(answer_text)
    if not answers:
        return None

    sections = [s.strip() for s in re.split(r"\n---\n", question_text) if s.strip()]
    if not sections:
        return None

    title, intro, questions = _parse_first_section(sections[0])
    for section in sections[1:]:
        questions.extend(_parse_question_block(section))

    if not questions:
        return None

    for question in questions:
        if question.number in answers:
            question.correct, question.explanation = answers[question.number]
        else:
            return None

    return Quiz(title=title, intro=intro, questions=questions)


def is_quiz_markdown(text: str) -> bool:
    return parse_quiz_markdown(text) is not None
