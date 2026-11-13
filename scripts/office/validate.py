#!/usr/bin/env python3
"""Validate DOCX ZIP integrity and XML well-formedness."""

from __future__ import annotations
import argparse
import zipfile
from pathlib import Path
import xml.etree.ElementTree as ET

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", type=Path)
    args = parser.parse_args()
    if not args.file.is_file() or not zipfile.is_zipfile(args.file):
        parser.error("Expected an existing DOCX package")
    failures = []
    with zipfile.ZipFile(args.file) as zf:
        bad = zf.testzip()
        if bad:
            failures.append(f"Corrupt ZIP member: {bad}")
        names = set(zf.namelist())
        for part in ("[Content_Types].xml", "word/document.xml"):
            if part not in names:
                failures.append(f"Missing {part}")
        for name in names:
            if name.endswith(".xml") or name.endswith(".rels") or name == "[Content_Types].xml":
                try:
                    ET.fromstring(zf.read(name))
                except ET.ParseError as exc:
                    failures.append(f"{name}: {exc}")
    if failures:
        print("\n".join(failures))
        return 1
    print("PASS: package ZIP and XML parsing checks succeeded.")
    print("This is not a full OOXML schema or visual-layout validation.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
