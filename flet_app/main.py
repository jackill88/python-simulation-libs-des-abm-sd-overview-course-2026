"""Offline Android course navigator — run with: flet run flet_app/main.py"""

from __future__ import annotations

import sys
from pathlib import Path

import flet as ft

FLET_APP_DIR = Path(__file__).resolve().parent
REPO_ROOT = FLET_APP_DIR.parent
for nav_root in (FLET_APP_DIR, REPO_ROOT):
    if (nav_root / "course_nav" / "quiz_parser.py").is_file():
        nav_path = str(nav_root)
        if nav_path not in sys.path:
            sys.path.insert(0, nav_path)
        break
else:
    if str(FLET_APP_DIR) not in sys.path:
        sys.path.insert(0, str(FLET_APP_DIR))

from course_nav.course_loader import ContentItem, discover_modules, read_markdown
from course_nav.quiz_parser import parse_quiz_markdown
from course_nav.database import (
    ModuleStatus,
    completion_stats,
    configure_db_dir,
    get_progress,
    init_db,
    set_module_status,
    touch_module,
)
from config import get_app_data_dir, get_course_root
from quiz_view import build_quiz_controls

_ACCENT = "#1565C0"

STATUS_ICONS = {
    ModuleStatus.NOT_STARTED: "⬜",
    ModuleStatus.IN_PROGRESS: "🔵",
    ModuleStatus.COMPLETED: "✅",
}

STATUS_LABELS = {
    ModuleStatus.NOT_STARTED: "Not started",
    ModuleStatus.IN_PROGRESS: "In progress",
    ModuleStatus.COMPLETED: "Completed",
}

_COURSE_MD_STYLE = ft.MarkdownStyleSheet(
    code_text_style=ft.TextStyle(
        font_family="monospace",
        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
    ),
    codeblock_padding=12,
    codeblock_decoration=ft.BoxDecoration(
        bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
        border_radius=8,
        border=ft.Border.all(1, ft.Colors.OUTLINE_VARIANT),
    ),
)


def _course_markdown(text: str) -> ft.Markdown:
    return ft.Markdown(
        value=text,
        extension_set=ft.MarkdownExtensionSet.GITHUB_FLAVORED,
        code_theme=ft.MarkdownCodeTheme.GITHUB,
        selectable=True,
        md_style_sheet=_COURSE_MD_STYLE,
        code_style_sheet=_COURSE_MD_STYLE,
    )


class CourseNavigator:
    def __init__(self, page: ft.Page) -> None:
        self.page = page
        configure_db_dir(get_app_data_dir())
        self.modules = discover_modules(root=get_course_root())
        init_db([m.module_id for m in self.modules])

        self.page_name = "home"
        self.selected_module: str | None = None
        self.content_path: str | None = None
        self._quiz_selections: dict[str, dict[int, str]] = {}
        self._quiz_submitted: set[str] = set()
        self._quiz_option_order: dict[str, dict[int, list[str]]] = {}

        self.body = ft.Column(expand=True, scroll=ft.ScrollMode.AUTO, spacing=12)
        self.content_container = ft.Container(
            content=self.body,
            expand=True,
            padding=ft.Padding.symmetric(horizontal=16, vertical=12),
        )
        self.progress_text = ft.Text("")
        self.progress_bar = ft.ProgressBar(value=0, bar_height=6, color=_ACCENT)
        self.appbar_title = ft.Text("Course Navigator")

    def start(self) -> None:
        self.page.title = "Python Simulation Libraries Course"
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.theme = ft.Theme(color_scheme_seed=_ACCENT)
        self.page.padding = 0
        self.page.appbar = ft.AppBar(
            leading=ft.IconButton(
                icon=ft.Icons.MENU,
                tooltip="Menu",
                on_click=self._open_drawer,
            ),
            title=self.appbar_title,
            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
        )
        self.page.drawer = self._build_drawer()
        self.page.add(
            ft.SafeArea(
                expand=True,
                content=self.content_container,
            )
        )
        self._do_render()

    def _find_module(self, module_id: str):
        for module in self.modules:
            if module.module_id == module_id:
                return module
        return None

    def _module_content_items(self, module_id: str) -> list[ContentItem]:
        module = self._find_module(module_id)
        if module is None:
            return []
        items: list[ContentItem] = []
        if module.readme:
            items.append(module.readme)
        items.extend(module.theory)
        items.extend(module.quizzes)
        return items

    def _go_home(self) -> None:
        self.page_name = "home"
        self.selected_module = None
        self.content_path = None
        self._schedule_render()

    def _open_module(self, module_id: str) -> None:
        self.page_name = "module"
        self.selected_module = module_id
        self.content_path = None
        touch_module(module_id)
        self._schedule_render()

    def _open_content(self, module_id: str, content_path: str) -> None:
        self.page_name = "content"
        self.selected_module = module_id
        self.content_path = content_path
        touch_module(module_id)
        self._schedule_render()

    def _navigate_content(self, offset: int) -> None:
        if not self.selected_module or not self.content_path:
            return
        items = self._module_content_items(self.selected_module)
        paths = [str(item.path) for item in items]
        try:
            idx = paths.index(self.content_path)
        except ValueError:
            return
        new_idx = idx + offset
        if 0 <= new_idx < len(paths):
            self._open_content(self.selected_module, paths[new_idx])

    def _mark_in_progress(self, module_id: str) -> None:
        set_module_status(module_id, ModuleStatus.IN_PROGRESS)
        self._schedule_render()

    def _mark_completed(self, module_id: str) -> None:
        set_module_status(module_id, ModuleStatus.COMPLETED)
        self._schedule_render()

    def _on_back(self, _=None) -> None:
        if self.page_name == "content" and self.selected_module:
            self._open_module(self.selected_module)
        elif self.page_name == "module":
            self._go_home()

    def _reset_module(self, module_id: str) -> None:
        set_module_status(module_id, ModuleStatus.NOT_STARTED)
        self._go_home()

    def _schedule_render(self) -> None:
        async def _render_async() -> None:
            self._do_render()

        self.page.run_task(_render_async)

    def _update_appbar(self) -> None:
        if self.page_name == "home":
            self.page.appbar.leading = ft.IconButton(
                icon=ft.Icons.MENU,
                tooltip="Menu",
                on_click=self._open_drawer,
            )
            self.appbar_title.value = "Course Navigator"
        else:
            self.page.appbar.leading = ft.IconButton(
                icon=ft.Icons.ARROW_BACK,
                tooltip="Back",
                on_click=self._on_back,
            )
            if self.page_name == "module" and self.selected_module:
                module = self._find_module(self.selected_module)
                self.appbar_title.value = module.title if module else "Module"
            elif self.page_name == "content" and self.content_path:
                self.appbar_title.value = Path(self.content_path).stem.replace("_", " ").title()
            else:
                self.appbar_title.value = "Course Navigator"

    def _do_render(self) -> None:
        self._update_drawer_progress()
        self._update_appbar()

        new_body = ft.Column(expand=True, scroll=ft.ScrollMode.AUTO, spacing=12)
        self.body = new_body

        if self.page_name == "home":
            self._render_home()
        elif self.page_name == "module" and self.selected_module:
            self._render_module(self.selected_module)
        elif (
            self.page_name == "content"
            and self.selected_module
            and self.content_path
        ):
            self._render_content(self.selected_module, self.content_path)
        else:
            self._render_home()

        self.content_container.content = new_body
        self.content_container.update()
        self.page.update()

    def _update_drawer_progress(self) -> None:
        completed, total = completion_stats([m.module_id for m in self.modules])
        ratio = completed / total if total else 0.0
        self.progress_bar.value = ratio
        self.progress_text.value = f"{completed} of {total} modules completed"

    async def _open_drawer(self, _=None) -> None:
        self._update_drawer_progress()
        self.page.drawer = self._build_drawer()
        await self.page.show_drawer()

    def _drawer_action(self, action):
        async def handler(_=None) -> None:
            await self._drawer_navigate(action)

        return handler

    def _build_drawer(self) -> ft.NavigationDrawer:
        progress_map = {m.module_id: get_progress(m.module_id) for m in self.modules}
        destinations: list[ft.Control] = [
            ft.Container(
                padding=16,
                content=ft.Column(
                    spacing=8,
                    controls=[
                        ft.Text("Course Navigator", size=18, weight=ft.FontWeight.BOLD),
                        self.progress_bar,
                        self.progress_text,
                    ],
                ),
            ),
            ft.ListTile(
                leading=ft.Icon(ft.Icons.HOME),
                title=ft.Text("Course Home"),
                on_click=self._drawer_action(self._go_home),
            ),
            ft.Divider(height=1),
            ft.Container(
                padding=ft.Padding.only(left=16, top=8, bottom=4),
                content=ft.Text("Modules", weight=ft.FontWeight.W_600),
            ),
        ]

        for module in self.modules:
            prog = progress_map[module.module_id]
            icon = STATUS_ICONS[prog.status]
            module_id = module.module_id

            destinations.append(
                ft.ListTile(
                    title=ft.Text(f"{icon} {module.number:02d}. {module.title}"),
                    on_click=self._drawer_action(
                        lambda mid=module_id: self._open_module(mid)
                    ),
                )
            )

        return ft.NavigationDrawer(controls=destinations)

    async def _drawer_navigate(self, action) -> None:
        await self.page.close_drawer()
        action()

    def _metric_card(self, label: str, value: str | int) -> ft.Container:
        return ft.Container(
            expand=True,
            padding=12,
            border_radius=8,
            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
            content=ft.Column(
                spacing=4,
                controls=[
                    ft.Text(str(value), size=24, weight=ft.FontWeight.BOLD),
                    ft.Text(label, size=12, color=ft.Colors.ON_SURFACE_VARIANT),
                ],
            ),
        )

    def _lesson_tile(
        self,
        *,
        module_id: str,
        item: ContentItem,
        icon: str,
        subtitle: str | None = None,
    ) -> ft.ListTile:
        path = str(item.path)
        return ft.ListTile(
            leading=ft.Icon(icon),
            title=ft.Text(item.title, size=14),
            subtitle=ft.Text(subtitle, size=12) if subtitle else None,
            trailing=ft.Icon(ft.Icons.CHEVRON_RIGHT, size=18),
            on_click=lambda _, p=path: self._open_content(module_id, p),
        )

    def _render_home(self) -> None:
        modules = self.modules
        completed, total = completion_stats([m.module_id for m in modules])
        course_root = get_course_root()
        progress_map = {m.module_id: get_progress(m.module_id) for m in modules}

        self.body.controls.extend(
            [
                ft.Text("Python Simulation Libraries Course", size=22, weight=ft.FontWeight.BOLD),
                ft.Text(
                    "SimPy DES · Mesa ABM · system dynamics · offline theory & quizzes",
                    color=ft.Colors.ON_SURFACE_VARIANT,
                ),
                ft.Row(
                    controls=[
                        self._metric_card("Modules", total),
                        self._metric_card("Completed", completed),
                        self._metric_card("Remaining", total - completed),
                    ],
                ),
            ]
        )

        readme_path = course_root / "README.md"
        if readme_path.is_file():
            self.body.controls.append(
                ft.ExpansionTile(
                    title=ft.Text("About this course"),
                    expanded=False,
                    controls=[
                        ft.Container(
                            padding=ft.Padding.only(left=8, right=8, bottom=12),
                            content=_course_markdown(read_markdown(readme_path)),
                        )
                    ],
                )
            )

        if not modules:
            self.body.controls.append(
                ft.Container(
                    padding=16,
                    bgcolor=ft.Colors.ERROR_CONTAINER,
                    border_radius=8,
                    content=ft.Column(
                        spacing=8,
                        controls=[
                            ft.Text(
                                "No course modules found",
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.ON_ERROR_CONTAINER,
                            ),
                            ft.Text(
                                "Rebuild after running: python flet_app/prepare_assets.py",
                                size=12,
                                color=ft.Colors.ON_ERROR_CONTAINER,
                            ),
                            ft.Text(
                                f"Looked under: {course_root}",
                                size=11,
                                color=ft.Colors.ON_ERROR_CONTAINER,
                            ),
                        ],
                    ),
                )
            )
            return

        self.body.controls.append(
            ft.Text("Your learning path", size=18, weight=ft.FontWeight.W_600)
        )

        for module in modules:
            prog = progress_map[module.module_id]
            icon = STATUS_ICONS[prog.status]
            module_id = module.module_id
            self.body.controls.append(
                ft.Card(
                    content=ft.ListTile(
                        leading=ft.Text(f"{module.number:02d}", weight=ft.FontWeight.BOLD),
                        title=ft.Text(f"{icon} {module.title}"),
                        subtitle=ft.Text(STATUS_LABELS[prog.status]),
                        trailing=ft.Icon(ft.Icons.CHEVRON_RIGHT),
                        on_click=lambda _, mid=module_id: self._open_module(mid),
                    )
                )
            )

    def _render_module(self, module_id: str) -> None:
        module = self._find_module(module_id)
        if module is None:
            self.body.controls.append(ft.Text("Module not found.", color=ft.Colors.ERROR))
            return

        progress = get_progress(module_id)

        self.body.controls.extend(
            [
                ft.Text(module.title, size=22, weight=ft.FontWeight.BOLD),
                ft.Text(
                    f"Module {module.number:02d} · {module.module_id}",
                    color=ft.Colors.ON_SURFACE_VARIANT,
                ),
                ft.Row(
                    controls=[
                        self._metric_card("Status", STATUS_LABELS[progress.status]),
                        self._metric_card("Theory lessons", len(module.theory)),
                        self._metric_card("Quizzes", len(module.quizzes)),
                    ],
                ),
                ft.Row(
                    controls=[
                        ft.Button(
                            "Mark in progress",
                            expand=True,
                            on_click=lambda _: self._mark_in_progress(module_id),
                        ),
                        ft.Button(
                            "Mark completed",
                            expand=True,
                            style=ft.ButtonStyle(
                                bgcolor=ft.Colors.PRIMARY, color=ft.Colors.ON_PRIMARY
                            ),
                            on_click=lambda _: self._mark_completed(module_id),
                        ),
                        ft.OutlinedButton(
                            "Reset module",
                            expand=True,
                            on_click=lambda _: self._reset_module(module_id),
                        ),
                    ],
                ),
                ft.Divider(),
            ]
        )

        if module.readme:
            self.body.controls.append(
                self._lesson_tile(
                    module_id=module_id,
                    item=module.readme,
                    icon=ft.Icons.MENU_BOOK,
                )
            )

        if module.theory:
            self.body.controls.append(
                ft.Text("Theory", size=16, weight=ft.FontWeight.W_600)
            )
            for item in module.theory:
                self.body.controls.append(
                    self._lesson_tile(
                        module_id=module_id,
                        item=item,
                        icon=ft.Icons.ARTICLE,
                    )
                )

        if module.quizzes:
            self.body.controls.append(
                ft.Text("Quizzes", size=16, weight=ft.FontWeight.W_600)
            )
            for item in module.quizzes:
                self.body.controls.append(
                    self._lesson_tile(
                        module_id=module_id,
                        item=item,
                        icon=ft.Icons.QUIZ,
                        subtitle="Interactive · tap to answer",
                    )
                )

    def _build_content_nav_row(
        self,
        module_id: str,
        *,
        has_prev: bool,
        has_next: bool,
    ) -> ft.Row:
        return ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.TextButton(
                    "← Previous",
                    disabled=not has_prev,
                    on_click=lambda _: self._navigate_content(-1),
                ),
                ft.TextButton(
                    "Back to module",
                    on_click=lambda _: self._open_module(module_id),
                ),
                ft.TextButton(
                    "Next →",
                    disabled=not has_next,
                    on_click=lambda _: self._navigate_content(1),
                ),
            ],
        )

    def _is_quiz_path(self, path: Path, items: list[ContentItem]) -> bool:
        for item in items:
            if str(item.path) == str(path):
                return item.kind == "quiz"
        return "quiz" in path.stem.lower()

    def _quiz_state(self, content_path: str) -> dict[int, str]:
        return self._quiz_selections.setdefault(content_path, {})

    def _quiz_order(self, content_path: str) -> dict[int, list[str]]:
        return self._quiz_option_order.setdefault(content_path, {})

    def _select_quiz_answer(self, content_path: str, question: int, letter: str) -> None:
        if content_path in self._quiz_submitted or not letter:
            return
        self._quiz_state(content_path)[question] = letter
        self._schedule_render()

    def _submit_quiz(self, content_path: str) -> None:
        self._quiz_submitted.add(content_path)
        self._schedule_render()

    def _reset_quiz(self, content_path: str) -> None:
        self._quiz_submitted.discard(content_path)
        self._quiz_selections.pop(content_path, None)
        self._quiz_option_order.pop(content_path, None)
        self._schedule_render()

    def _render_interactive_quiz(self, content_path: str, quiz) -> list[ft.Control]:
        return build_quiz_controls(
            quiz,
            selections=self._quiz_state(content_path),
            submitted=content_path in self._quiz_submitted,
            option_order=self._quiz_order(content_path),
            on_select=lambda q, letter, p=content_path: self._select_quiz_answer(p, q, letter),
            on_submit=lambda p=content_path: self._submit_quiz(p),
            on_reset=lambda p=content_path: self._reset_quiz(p),
        )

    def _render_content(self, module_id: str, content_path: str) -> None:
        module = self._find_module(module_id)
        path = Path(content_path)
        if not path.is_file():
            self.body.controls.append(
                ft.Text("Content file not found.", color=ft.Colors.ERROR)
            )
            return

        items = self._module_content_items(module_id)
        paths = [str(item.path) for item in items]
        idx = paths.index(content_path) if content_path in paths else -1
        has_prev = idx > 0
        has_next = 0 <= idx < len(paths) - 1

        title = path.stem.replace("_", " ").title()
        for item in items:
            if str(item.path) == content_path:
                title = item.title
                break

        if module:
            self.body.controls.append(
                ft.Text(
                    f"Module {module.number:02d} · {module.title}",
                    size=12,
                    color=ft.Colors.ON_SURFACE_VARIANT,
                )
            )
        self.body.controls.append(ft.Text(title, size=20, weight=ft.FontWeight.BOLD))

        self.body.controls.append(
            self._build_content_nav_row(module_id, has_prev=has_prev, has_next=has_next)
        )
        self.body.controls.append(ft.Divider())

        raw = read_markdown(path)
        quiz = parse_quiz_markdown(raw) if self._is_quiz_path(path, items) else None
        if quiz:
            self.body.controls.extend(self._render_interactive_quiz(content_path, quiz))
        else:
            self.body.controls.append(_course_markdown(raw))

        self.body.controls.append(ft.Divider())
        self.body.controls.append(
            self._build_content_nav_row(module_id, has_prev=has_prev, has_next=has_next)
        )


def main(page: ft.Page) -> None:
    try:
        CourseNavigator(page).start()
    except Exception as exc:  # noqa: BLE001 — show startup failures on device
        page.add(
            ft.SafeArea(
                content=ft.Container(
                    padding=16,
                    content=ft.Column(
                        controls=[
                            ft.Text("Course navigator failed to start", size=18, weight=ft.FontWeight.BOLD),
                            ft.Text(str(exc), selectable=True),
                            ft.Text(
                                "If this is an APK build, run prepare_assets.py before flet build apk.",
                                size=12,
                                color=ft.Colors.ON_SURFACE_VARIANT,
                            ),
                        ]
                    ),
                )
            )
        )
        page.update()


if __name__ == "__main__":
    ft.run(main, assets_dir="assets")
