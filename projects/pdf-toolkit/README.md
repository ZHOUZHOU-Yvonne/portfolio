# PDF Toolkit

> Python library for PDF manipulation: merge, split, extract text, compress, and convert.

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

## Quick Start

```bash
pip install pypdf pdfplumber pillow reportlab
```

```python
from pdf_toolkit import PDFToolkit

pdf = PDFToolkit('document.pdf')
pdf.merge(['page1.pdf', 'page2.pdf'], 'merged.pdf')
pdf.split('output_folder/')
pdf.extract_text('output.txt')
pdf.compress('compressed.pdf', quality=70)
pdf.to_images('images/')
```

## Features

- Merge multiple PDFs
- Split PDF into individual pages
- Extract text with layout preservation
- Compress/reduce file size
- Convert pages to images
- Add watermarks
- Rotate pages

## CLI Usage

```bash
python -m pdf_toolkit merge a.pdf b.pdf -o merged.pdf
python -m pdf_toolkit split doc.pdf -o pages/
python -m pdf_toolkit compress large.pdf -q 80
python -m pdf_toolkit extract doc.pdf -o text.txt
```

## Need custom PDF solutions?

I build PDF automation pipelines for businesses. Contact for custom work.
