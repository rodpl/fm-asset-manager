"""Utilities for moving Football Manager asset files into place."""

from __future__ import annotations

import shutil
from pathlib import Path


def move_asset(source_path: str, destination_dir: str, dest_stem: str) -> Path:
    """Move a single asset file into the destination directory."""
    source = Path(source_path).expanduser()
    if not source.exists():
        raise FileNotFoundError(f"Source asset does not exist: {source}")

    destination_root = Path(destination_dir).expanduser()
    destination_root.mkdir(parents=True, exist_ok=True)

    suffix = source.suffix or ".png"
    destination = destination_root / f"{dest_stem}{suffix}"

    try:
        if source.resolve(strict=True) == destination.resolve(strict=False):
            return destination
    except FileNotFoundError:
        # destination may not exist yet; safe to ignore
        pass

    if destination.exists():
        if destination.is_dir():
            raise IsADirectoryError(f"Destination refers to a directory: {destination}")
        destination.unlink()

    shutil.move(str(source), str(destination))
    return destination


def move_optional_asset(
    source_path: str | None, destination_dir: str, dest_stem: str
) -> Path | None:
    """Move an asset if a source path is provided."""
    if not source_path:
        return None
    return move_asset(source_path, destination_dir, dest_stem)
