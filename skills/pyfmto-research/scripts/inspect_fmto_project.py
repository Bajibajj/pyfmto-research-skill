#!/usr/bin/env python3
"""Summarize a PyFMTO project structure without modifying files."""

from __future__ import annotations

import argparse
from pathlib import Path


KEY_FILES = ["README.md", "CONVENTIONS.md", "requirements.txt", "config.yaml", "minimal.yaml"]
KEY_DIRS = ["algorithms", "problems", "configs", "out"]


def list_packages(root: Path, name: str) -> list[str]:
    base = root / name
    if not base.is_dir():
        return []
    return sorted(
        item.name for item in base.iterdir()
        if item.is_dir() and not item.name.startswith("__")
    )


def exists_label(path: Path) -> str:
    return "yes" if path.exists() else "no"


def print_section(title: str) -> None:
    print()
    print(title)
    print("-" * len(title))

def inspect(root: Path) -> int:
    root = root.resolve()
    print(f"Project: {root}")

    print_section("Key files")
    for name in KEY_FILES:
        print(f"{name}: {exists_label(root / name)}")

    print_section("Key directories")
    for name in KEY_DIRS:
        print(f"{name}: {exists_label(root / name)}")

    algorithms = list_packages(root, "algorithms")
    problems = list_packages(root, "problems")

    print_section("Algorithms")
    if algorithms:
        for name in algorithms:
            print(f"- {name}")
    else:
        print("none found")

    print_section("Problems")
    if problems:
        for name in problems:
            print(f"- {name}")
    else:
        print("none found")

    print_section("Templates")
    print(f"algorithms/DEMO: {exists_label(root / 'algorithms' / 'DEMO')}")
    print(f"problems/demo: {exists_label(root / 'problems' / 'demo')}")

    print_section("Suggestions")
    if not (root / "config.yaml").exists() and not (root / "minimal.yaml").exists():
        print("Create a config YAML before running PyFMTO experiments.")
    if "DEMO" not in algorithms:
        print("No algorithms/DEMO template found; inspect an existing algorithm before adding a new one.")
    if "demo" not in problems:
        print("No problems/demo template found; inspect an existing problem before adding a new one.")
    if algorithms and problems:
        print("Project structure looks usable. Run PyFMTO list/show commands for discovery validation.")

    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Inspect a PyFMTO project layout.")
    parser.add_argument("root", nargs="?", default=".", help="PyFMTO project root")
    args = parser.parse_args()
    return inspect(Path(args.root))


if __name__ == "__main__":
    raise SystemExit(main())
