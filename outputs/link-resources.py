#!/usr/bin/env python3
"""Utility to symlink generated Football Manager resources into the game folder."""

from __future__ import annotations

import argparse
import platform
import sys
from pathlib import Path

MAC_GRAPHICS_ROOT = Path(
    "~/Library/Application Support/Sports Interactive/Football Manager 26/graphics"
).expanduser()


def resolve_target_root(system_name: str) -> Path:
    """Return the base graphics directory for the current platform."""
    if system_name == "Darwin":
        return MAC_GRAPHICS_ROOT
    if system_name == "Windows":
        raise NotImplementedError(
            "Windows linking is not implemented yet. Please create links manually."
        )
    raise RuntimeError(f"Unsupported platform: {system_name!r}")


def create_symlink(source: Path, destination: Path) -> None:
    """Create a symlink from destination -> source with safety checks."""
    if destination.is_symlink():
        if destination.resolve() == source.resolve():
            print(f"✓ Already linked: {destination} -> {source}")
            return
        print(
            f"! Skipping {destination}: existing symlink points elsewhere "
            f"({destination.resolve()})"
        )
        return

    if destination.exists():
        print(f"! Skipping {destination}: path already exists and is not a symlink")
        return

    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.symlink_to(source)
    print(f"→ Linked {destination} -> {source}")


def iter_source_directories(base_dir: Path) -> list[Path]:
    """Return the list of immediate subdirectories to link."""
    return sorted(
        child
        for child in base_dir.iterdir()
        if child.is_dir() and child.name != "__pycache__"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Symlink generated outputs into the Football Manager graphics folder."
    )
    parser.add_argument(
        "--source",
        type=Path,
        default=Path(__file__).resolve().parent,
        help="Root directory containing resource subfolders (default: script directory).",
    )
    parser.add_argument(
        "--target",
        type=Path,
        default=None,
        help="Override target graphics directory (default: detected per platform).",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    source_root = args.source.resolve()

    if not source_root.exists():
        print(f"Source directory does not exist: {source_root}", file=sys.stderr)
        return 1

    system_name = platform.system()
    try:
        target_root = (
            args.target.expanduser() if args.target else resolve_target_root(system_name)
        )
    except (RuntimeError, NotImplementedError) as exc:
        print(str(exc), file=sys.stderr)
        return 2

    print(f"System detected: {system_name}")
    print(f"Source root: {source_root}")
    print(f"Target root: {target_root}")

    try:
        directories = iter_source_directories(source_root)
    except FileNotFoundError:
        print(f"Source root is not accessible: {source_root}", file=sys.stderr)
        return 1

    if not directories:
        print("No subdirectories found to link. Nothing to do.")
        return 0

    for subdir in directories:
        destination = target_root / subdir.name
        create_symlink(subdir, destination)

    return 0


if __name__ == "__main__":
    sys.exit(main())
