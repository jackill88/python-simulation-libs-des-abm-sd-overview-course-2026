#!/usr/bin/env python3
"""Verify all quiz markdown files parse correctly."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from course_nav.course_loader import discover_modules, read_markdown
from course_nav.quiz_parser import parse_quiz_markdown


def main() -> int:
    errors: list[str] = []
    modules = discover_modules(ROOT)
    quiz_count = 0

    for module in modules:
        for quiz in module.quizzes:
            quiz_count += 1
            text = read_markdown(quiz.path)
            parsed = parse_quiz_markdown(text)
            if parsed is None:
                errors.append(f"{quiz.path}: failed to parse")
            elif len(parsed.questions) < 8:
                errors.append(f"{quiz.path}: expected at least 8 questions")

    print(f"Checked {quiz_count} quizzes across {len(modules)} modules")
    if errors:
        for err in errors:
            print(f"  ERROR: {err}")
        return 1
    print("All quizzes OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
