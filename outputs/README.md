# Outputs Directory

This folder hosts generated assets and helper utilities for linking them into a local
Football Manager installation.

## `link-resources.py`

Symlinks each immediate subfolder in this directory (for example, `faces-rod/`) into
the Football Manager graphics folder on macOS.

### Usage

```bash
python3 outputs/link-resources.py
```

The script detects macOS automatically and targets:
`~/Library/Application Support/Sports Interactive/Football Manager 26/graphics/`.

Optional flags:

- `--source`: override the directory that contains resource subfolders (defaults to
  the script directory).
- `--target`: override the Football Manager graphics directory (useful for dry runs
  or custom installs).

Existing files or symlinks in the target location are left untouched. Windows support
is planned but not implemented yet.
