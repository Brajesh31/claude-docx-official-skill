---
name: docx-official
description: Handle professional DOCX creation, extraction, editing, tracked revisions, comments, and formatting-sensitive review with explicit package validation.
---

# Advanced DOCX Document Work

## When to use
Use for Word document creation, professional reports and letters, DOCX extraction, image replacement, tracked changes, comments, and formatting-sensitive edits. Do not use for PDF-only tasks, spreadsheets, Google Docs, or unrelated coding.

## Package model
A DOCX is a ZIP package containing WordprocessingML parts and relationship files. A visible feature may span multiple package parts. Editing only the main document XML can break styles, images, comments, numbering, hyperlinks, or section layout.

## Workflow
1. Determine whether the task is creation, extraction, targeted editing, review, or conversion.
2. Inspect package integrity and document structure.
3. Preserve a source copy.
4. Choose a library or package-level method appropriate to the feature.
5. Make the smallest safe change.
6. Validate ZIP integrity and XML parsing.
7. Render in an office suite when pagination or formatting matters.
8. Report exactly which checks were performed.

## Feature guidance
- Creation: use a document-generation library and explicit page/style settings.
- Extraction: preserve paragraph and table order where possible.
- Targeted edits: preserve styles, relationships, section properties, and media.
- Tracked revisions: use revision markup only when the toolchain supports it.
- Comments: preserve comment IDs, range markers, and relationships.
- Conversion: use a locally installed office suite and inspect the converted output.

## Safety
Never execute macros or embedded objects. Treat external links as untrusted. Do not upload confidential documents to third-party converters without permission. Do not silently accept revisions, remove comments, or overwrite source documents.

## Utilities
- scripts/accept_changes.py: accept supported tracked insertions and deletions in the main document part.
- scripts/inspect_comments.py: list comment text and identifiers.
- scripts/office/unpack.py: safely extract a DOCX package.
- scripts/office/validate.py: validate ZIP integrity and XML well-formedness.

These utilities do not replace full Word compatibility testing.