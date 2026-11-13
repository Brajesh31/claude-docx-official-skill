#!/usr/bin/env python3
"""Accept tracked insertions and deletions in word/document.xml in a DOCX copy."""

from __future__ import annotations
import argparse
import os
import tempfile
import zipfile
from pathlib import Path
import xml.etree.ElementTree as ET

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"

def process(parent):
    for child in list(parent):
        if child.tag == W + "ins":
            index = list(parent).index(child)
            parent.remove(child)
            for nested in list(child):
                parent.insert(index, nested)
                index += 1
        elif child.tag == W + "del":
            parent.remove(child)
        else:
            process(child)

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    if not args.input.is_file() or not zipfile.is_zipfile(args.input):
        parser.error("Input must be an existing DOCX package")
    if args.input.resolve() == args.output.resolve():
        parser.error("Output must differ from input")
    with zipfile.ZipFile(args.input) as source:
        names = source.namelist()
        if "word/document.xml" not in names:
            parser.error("Missing word/document.xml")
        data = {name: source.read(name) for name in names}
    try:
        root = ET.fromstring(data["word/document.xml"])
    except ET.ParseError as exc:
        parser.error(f"Invalid document XML: {exc}")
    process(root)
    data["word/document.xml"] = ET.tostring(root, encoding="utf-8", xml_declaration=True)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(dir=args.output.parent, suffix=".docx")
    os.close(fd)
    try:
        with zipfile.ZipFile(temp_name, "w", zipfile.ZIP_DEFLATED) as target:
            for name, content in data.items():
                target.writestr(name, content)
        os.replace(temp_name, args.output)
    finally:
        if os.path.exists(temp_name):
            os.unlink(temp_name)
    print(f"Created {args.output}")
    print("LIMITATION: processes only w:ins and w:del in word/document.xml. Review move ranges, nested revisions, headers, footers, footnotes, and other parts separately.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
