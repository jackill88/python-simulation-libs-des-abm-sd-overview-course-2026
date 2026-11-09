#!/usr/bin/env python3
"""Generate course markdown from _scripts/theory_content and module metadata."""

from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = Path(__file__).resolve().parent
THEORY_SRC = SCRIPTS / "theory_content"


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.strip() + "\n", encoding="utf-8")
    print(f"  wrote {path.relative_to(ROOT)}")


def sync_theory() -> None:
    from theory_manifest import THEORY_LESSONS  # noqa: PLC0415

    for module_id, lessons in THEORY_LESSONS.items():
        dest_dir = ROOT / module_id / "theory"
        dest_dir.mkdir(parents=True, exist_ok=True)
        src_dir = THEORY_SRC / module_id
        allowed = {filename for filename, _title in lessons}
        for filename, _title in lessons:
            src = src_dir / filename
            if not src.is_file():
                raise FileNotFoundError(f"Missing theory source: {src}")
            shutil.copy2(src, dest_dir / filename)
        for stale in dest_dir.glob("*.md"):
            if stale.name not in allowed:
                stale.unlink()


def main() -> None:
    from modules_readmes import MODULE_READMES  # noqa: PLC0415
    from quiz_content import QUIZZES  # noqa: PLC0415

    root_readme = (SCRIPTS / "root_readme.md").read_text(encoding="utf-8")

    print("Bootstrapping simulation course content...")
    write(ROOT / "README.md", root_readme)
    sync_theory()

    for module_id, readme in sorted(MODULE_READMES.items()):
        write(ROOT / module_id / "README.md", readme)
        if module_id in QUIZZES:
            write(ROOT / module_id / "quizzes" / "module_quiz.md", QUIZZES[module_id])

    print("Done.")


if __name__ == "__main__":
    main()
