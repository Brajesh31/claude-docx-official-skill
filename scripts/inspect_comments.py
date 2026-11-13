#!/usr/bin/env python3
"""List comment IDs, authors, and text from a DOCX comments part."""

from __future__ import annotations
import argparse
import zipfile
from pathlib import Path
import xml.etree.ElementTree as ET

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", type=Path)
    args = parser.parse_args()
    if not args.file.is_file() or not zipfile.is_zipfile(args.file):
        parser.error("Expected an existing DOCX package")
    with zipfile.ZipFile(args.file) as zf:
        if "word/comments.xml" not in zf.namelist():
            print("No comments.xml part found.")
            return 0
        root = ET.fromstring(zf.read("word/comments.xml"))
    comments = root.findall(W + "comment")
    for item in comments:
        comment_id = item.attrib.get(W + "id", "?")
        author = item.attrib.get(W + "author", "Unknown")
        text = "".join(node.text or "" for node in item.iter(W + "t"))
        print(f"ID {comment_id} | {author}: {text}")
    print(f"Comments: {len(comments)}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
