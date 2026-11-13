#!/usr/bin/env python3
"""Safely extract a DOCX package into a directory."""

from __future__ import annotations
import argparse
import zipfile
from pathlib import Path

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    if not args.input.is_file() or not zipfile.is_zipfile(args.input):
        parser.error("Input must be an existing DOCX package")
    args.output.mkdir(parents=True, exist_ok=True)
    root = args.output.resolve()
    with zipfile.ZipFile(args.input) as zf:
        for member in zf.infolist():
            target = (root / member.filename).resolve()
            if target != root and root not in target.parents:
                raise ValueError(f"Unsafe archive path: {member.filename}")
        zf.extractall(root)
    print(f"Extracted package to {root}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
