#!/usr/bin/env python3

from pathlib import Path
import shutil
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DIST_DIR = PROJECT_ROOT / ".dist"
RELEASE_DIR = DIST_DIR / PROJECT_ROOT.name

EXCLUDED_DIRS = {
    ".dist",
    "scripts",
    "tests",
    "examples",
    "__pycache__",
    ".git",
    ".github",
    ".idea",
    ".vscode",
}

EXCLUDED_FILES = {
    ".gitignore",
    "Makefile",
    "README.md",
}


def clean():
    if RELEASE_DIR.exists():
        shutil.rmtree(RELEASE_DIR)


def create_release():
    clean()

    RELEASE_DIR.mkdir(parents=True)

    for item in PROJECT_ROOT.iterdir():
        if not item.is_dir():
            if item.name not in EXCLUDED_FILES:
                shutil.copy2(item, RELEASE_DIR / item.name)
            continue

        if item.name in EXCLUDED_DIRS:
            continue

        shutil.copytree(
            item,
            RELEASE_DIR / item.name,
            ignore=shutil.ignore_patterns(
                "__pycache__",
                "*.pyc",
                "*.pyo"
            )
        )
    
    shutil.make_archive(
        str(RELEASE_DIR),
        "zip",
        DIST_DIR,
        PROJECT_ROOT.name
    )


if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] == 'release':
        create_release()
    elif sys.argv[1] == 'clean':
        clean()
    else:
        sys.exit(1)
