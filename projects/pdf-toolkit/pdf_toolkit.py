"""
PDF Toolkit — Merge, split, extract, compress, and convert PDFs in Python.
"""

import os
from pathlib import Path
from typing import List, Optional

try:
    from pypdf import PdfReader, PdfWriter
except ImportError:
    PdfReader = PdfWriter = None

try:
    import pdfplumber
except ImportError:
    pdfplumber = None

try:
    from PIL import Image
except ImportError:
    Image = None


class PDFToolkit:
    """All-in-one PDF manipulation."""

    def __init__(self, path: Optional[str] = None):
        self.path = path
        self._reader = PdfReader(path) if path and PdfReader and os.path.exists(path) else None

    def merge(self, paths: List[str], output: str):
        """Merge multiple PDFs into one."""
        writer = PdfWriter()
        for p in paths:
            reader = PdfReader(p)
            for page in reader.pages:
                writer.add_page(page)
        if self._reader:
            for page in self._reader.pages:
                writer.add_page(page)
        writer.write(output)
        return output

    def split(self, output_dir: str):
        """Split PDF into individual pages."""
        if not self._reader:
            raise ValueError("No PDF loaded")
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        files = []
        for i, page in enumerate(self._reader.pages):
            writer = PdfWriter()
            writer.add_page(page)
            fname = os.path.join(output_dir, f'page_{i+1:03d}.pdf')
            writer.write(fname)
            files.append(fname)
        return files

    def extract_text(self, output: Optional[str] = None) -> str:
        """Extract text from PDF."""
        if pdfplumber and self.path:
            text_parts = []
            with pdfplumber.open(self.path) as pdf:
                for page in pdf.pages:
                    t = page.extract_text()
                    if t:
                        text_parts.append(t)
            full_text = '\n\n'.join(text_parts)
        elif self._reader:
            full_text = '\n\n'.join(page.extract_text() or '' for page in self._reader.pages)
        else:
            raise ValueError("No PDF loaded")
        if output:
            with open(output, 'w', encoding='utf-8') as f:
                f.write(full_text)
        return full_text

    def compress(self, output: str, quality: int = 70):
        """Compress PDF by converting pages to JPEG and back."""
        if not Image or not self._reader:
            raise ImportError("Pillow and pypdf required")
        writer = PdfWriter()
        # Use pdfplumber for better image extraction
        if pdfplumber and self.path:
            with pdfplumber.open(self.path) as pdf:
                for page in pdf.pages:
                    img = page.to_image(resolution=150)
                    tmp = '/tmp/_pdf_page.jpg'
                    img.save(tmp, 'JPEG', quality=quality)
                    # Add as image page
                    pil_img = Image.open(tmp)
                    pil_img.save(tmp.replace('.jpg', '.pdf'))
                    reader = PdfReader(tmp.replace('.jpg', '.pdf'))
                    if reader.pages:
                        writer.add_page(reader.pages[0])
        writer.write(output)
        return output

    def page_count(self) -> int:
        """Return number of pages."""
        return len(self._reader.pages) if self._reader else 0

    def rotate(self, output: str, angle: int = 90):
        """Rotate all pages by angle degrees."""
        if not self._reader:
            raise ValueError("No PDF loaded")
        writer = PdfWriter()
        for page in self._reader.pages:
            page.rotate(angle)
            writer.add_page(page)
        writer.write(output)
        return output

    def __repr__(self):
        return f'PDFToolkit(path={self.path!r}, pages={self.page_count()})'


if __name__ == '__main__':
    print("PDF Toolkit — Python PDF manipulation library")
    print("Usage: from pdf_toolkit import PDFToolkit")
