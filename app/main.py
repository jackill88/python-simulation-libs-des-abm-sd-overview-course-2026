"""Streamlit course browser — run with: streamlit run app/main.py"""

from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

APP_DIR = Path(__file__).resolve().parent
if str(APP_DIR.parent) not in sys.path:
    sys.path.insert(0, str(APP_DIR.parent))

from course_nav.course_loader import COURSE_ROOT, discover_modules, read_markdown
from course_nav.database import (
    ModuleStatus,
    completion_stats,
    get_progress,
    init_db,
    set_module_status,
    touch_module,
)

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


def _init_session() -> None:
    if "modules" not in st.session_state:
        st.session_state.modules = discover_modules()
        init_db([m.module_id for m in st.session_state.modules])
    if "page" not in st.session_state:
        st.session_state.page = "home"
    if "selected_module" not in st.session_state:
        st.session_state.selected_module = None
    if "content_path" not in st.session_state:
        st.session_state.content_path = None


def _go_home() -> None:
    st.session_state.page = "home"
    st.session_state.selected_module = None
    st.session_state.content_path = None


def _open_module(module_id: str) -> None:
    st.session_state.page = "module"
    st.session_state.selected_module = module_id
    st.session_state.content_path = None
    touch_module(module_id)


def _open_content(module_id: str, content_path: str) -> None:
    st.session_state.page = "content"
    st.session_state.selected_module = module_id
    st.session_state.content_path = content_path
    touch_module(module_id)


def _mark_in_progress(module_id: str) -> None:
    set_module_status(module_id, ModuleStatus.IN_PROGRESS)


def _mark_completed(module_id: str) -> None:
    set_module_status(module_id, ModuleStatus.COMPLETED)


def _reset_module(module_id: str) -> None:
    set_module_status(module_id, ModuleStatus.NOT_STARTED)
    _go_home()


def _find_module(module_id: str):
    for module in st.session_state.modules:
        if module.module_id == module_id:
            return module
    return None


def _render_sidebar() -> None:
    modules = st.session_state.modules
    completed, total = completion_stats([m.module_id for m in modules])

    st.sidebar.title("Course Navigator")
    st.sidebar.progress(completed / total if total else 0.0)
    st.sidebar.caption(f"{completed} of {total} modules completed")

    st.sidebar.button(
        "🏠 Course Home",
        use_container_width=True,
        on_click=_go_home,
    )

    st.sidebar.divider()
    st.sidebar.subheader("Modules")

    progress_map = {m.module_id: get_progress(m.module_id) for m in modules}
    for module in modules:
        prog = progress_map[module.module_id]
        icon = STATUS_ICONS[prog.status]
        label = f"{icon} {module.number:02d}. {module.title}"
        st.sidebar.button(
            label,
            key=f"nav_{module.module_id}",
            use_container_width=True,
            on_click=_open_module,
            args=(module.module_id,),
        )


def _render_home() -> None:
    st.title("Python Simulation Libraries Course")
    st.caption("LLM integration · structured output · FastAPI patterns · self-paced · test-driven")

    modules = st.session_state.modules
    completed, total = completion_stats([m.module_id for m in modules])

    col1, col2, col3 = st.columns(3)
    col1.metric("Modules", total)
    col2.metric("Completed", completed)
    col3.metric("Remaining", total - completed)

    readme_path = COURSE_ROOT / "README.md"
    if readme_path.is_file():
        with st.expander("About this course", expanded=True):
            st.markdown(read_markdown(readme_path))

    st.subheader("Your learning path")
    progress_map = {m.module_id: get_progress(m.module_id) for m in modules}
    for module in modules:
        prog = progress_map[module.module_id]
        icon = STATUS_ICONS[prog.status]
        cols = st.columns([1, 6, 2])
        cols[0].write(f"**{module.number:02d}**")
        cols[1].write(f"{icon} **{module.title}** — {STATUS_LABELS[prog.status]}")
        cols[2].button(
            "Open",
            key=f"home_open_{module.module_id}",
            on_click=_open_module,
            args=(module.module_id,),
        )


def _render_module(module_id: str) -> None:
    module = _find_module(module_id)
    if module is None:
        st.error("Module not found.")
        return

    progress = get_progress(module_id)

    st.title(module.title)
    st.caption(f"Module {module.number:02d} · `{module.module_id}`")

    cols = st.columns([2, 2, 2, 2])
    cols[0].metric("Status", STATUS_LABELS[progress.status])
    cols[1].metric("Theory lessons", len(module.theory))
    cols[2].metric("Quizzes", len(module.quizzes))
    cols[3].metric("Challenges", len(module.challenges))

    action_cols = st.columns(3)
    action_cols[0].button(
        "Mark in progress",
        use_container_width=True,
        on_click=_mark_in_progress,
        args=(module_id,),
    )
    action_cols[1].button(
        "Mark completed",
        type="primary",
        use_container_width=True,
        on_click=_mark_completed,
        args=(module_id,),
    )
    action_cols[2].button(
        "Reset module",
        use_container_width=True,
        on_click=_reset_module,
        args=(module_id,),
    )

    st.divider()

    if module.readme:
        st.button(
            "📖 Module overview (README)",
            use_container_width=True,
            on_click=_open_content,
            args=(module_id, str(module.readme.path)),
        )

    if module.theory:
        st.subheader("Theory")
        for item in module.theory:
            st.button(
                f"📄 {item.title}",
                key=f"theory_{item.path}",
                use_container_width=True,
                on_click=_open_content,
                args=(module_id, str(item.path)),
            )

    if module.quizzes:
        st.subheader("Quizzes")
        for item in module.quizzes:
            st.button(
                f"❓ {item.title}",
                key=f"quiz_{item.path}",
                use_container_width=True,
                on_click=_open_content,
                args=(module_id, str(item.path)),
            )

    if module.challenges:
        st.subheader("Challenges")
        st.caption("Open the `.py` file in your editor, implement the stubs, then run pytest.")
        for item in module.challenges:
            st.code(str(item.path.relative_to(COURSE_ROOT)), language="text")

        test_dir = COURSE_ROOT / "tests" / module.module_id
        if test_dir.is_dir():
            st.info(f"Run tests: `pytest {test_dir.relative_to(COURSE_ROOT)} -v`")


def _render_content(module_id: str, content_path: str) -> None:
    module = _find_module(module_id)
    path = Path(content_path)
    if not path.is_file():
        st.error("Content file not found.")
        return

    if module:
        st.caption(f"{module.title} · {path.name}")

    st.button(
        "← Back to module",
        on_click=_open_module,
        args=(module_id,),
    )

    st.divider()
    st.markdown(read_markdown(path))


def main() -> None:
    st.set_page_config(
        page_title="Python Simulation Libraries Course",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    _init_session()
    _render_sidebar()

    page = st.session_state.page
    if page == "home":
        _render_home()
    elif page == "module" and st.session_state.selected_module:
        _render_module(st.session_state.selected_module)
    elif page == "content" and st.session_state.selected_module and st.session_state.content_path:
        _render_content(st.session_state.selected_module, st.session_state.content_path)
    else:
        _render_home()


if __name__ == "__main__":
    main()
