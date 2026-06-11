"""
QuickScraper — Simple web scraping for Python.
Extract data from any website in 3 lines of code.
"""

import csv, json, time, re, os
from typing import List, Dict, Optional, Any, Union
from urllib.parse import urljoin, urlparse

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    requests = None
    BeautifulSoup = None


class Scraper:
    """Main scraper class with auto-detection and data extraction."""

    def __init__(self, url: str, headers: Optional[Dict] = None, delay: float = 1.0,
                 use_playwright: bool = False):
        if not requests:
            raise ImportError("Install dependencies: pip install requests beautifulsoup4")
        self.url = url
        self.session = requests.Session()
        self.session.headers.update(headers or {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
        self.delay = delay
        self._data: List[Dict] = []
        self._soup: Optional[BeautifulSoup] = None
        self._fetch(url)

    def _fetch(self, url: str):
        time.sleep(self.delay)
        r = self.session.get(url, timeout=30)
        r.raise_for_status()
        self._soup = BeautifulSoup(r.text, 'html.parser')

    def extract(self, container: str, fields: Dict[str, str]) -> List[Dict]:
        """Extract structured data using CSS selectors.

        Args:
            container: CSS selector for the repeating container element
            fields: Dict mapping field names to CSS selectors.
                    Append ' @attr' to extract an attribute instead of text.
                    Example: {'title': 'h3 a', 'url': 'h3 a @href'}

        Returns:
            List of dicts with extracted data
        """
        if not self._soup:
            return []
        results = []
        items = self._soup.select(container)
        for item in items:
            row = {}
            for field_name, selector in fields.items():
                attr = None
                if ' @' in selector:
                    selector, attr = selector.rsplit(' @', 1)
                el = item.select_one(selector)
                if el:
                    row[field_name] = el.get(attr) if attr else el.get_text(strip=True)
                else:
                    row[field_name] = None
            if any(v is not None for v in row.values()):
                results.append(row)
        self._data = results
        return results

    def extract_table(self, selector: str = 'table', headers: Optional[List[str]] = None) -> List[Dict]:
        """Extract data from an HTML table."""
        if not self._soup:
            return []
        table = self._soup.select_one(selector)
        if not table:
            return []
        rows = table.select('tr')
        if not rows:
            return []
        # Detect headers
        if not headers:
            ths = rows[0].select('th, td')
            headers = [th.get_text(strip=True) for th in ths]
            data_rows = rows[1:]
        else:
            data_rows = rows
        results = []
        for row in data_rows:
            cells = row.select('td')
            if len(cells) >= len(headers):
                results.append({headers[i]: cells[i].get_text(strip=True) for i in range(len(headers))})
        self._data = results
        return results

    def paginate(self, container: str, fields: Dict[str, str],
                 next_selector: str, max_pages: int = 10) -> List[Dict]:
        """Extract data across multiple pages.

        Args:
            container: CSS selector for data container
            fields: Field extraction mapping
            next_selector: CSS selector for "Next" link
            max_pages: Maximum pages to scrape
        """
        all_data = []
        current_url = self.url
        for page in range(max_pages):
            print(f'Scraping page {page + 1}: {current_url}')
            self._fetch(current_url)
            page_data = self.extract(container, fields)
            all_data.extend(page_data)
            # Find next page
            next_el = self._soup.select_one(next_selector) if self._soup else None
            if next_el and next_el.get('href'):
                current_url = urljoin(current_url, next_el['href'])
            else:
                break
        self._data = all_data
        return all_data

    def to_csv(self, path: str):
        """Save extracted data to CSV."""
        if not self._data:
            return
        with open(path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=self._data[0].keys())
            writer.writeheader()
            writer.writerows(self._data)

    def to_json(self, path: str):
        """Save extracted data to JSON."""
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(self._data, f, ensure_ascii=False, indent=2)

    def to_sqlite(self, path: str, table: str = 'data'):
        """Save extracted data to SQLite database."""
        try:
            import sqlite3
        except ImportError:
            raise ImportError("sqlite3 is built-in, should be available")
        conn = sqlite3.connect(path)
        if self._data:
            cols = list(self._data[0].keys())
            conn.execute(f'CREATE TABLE IF NOT EXISTS {table} ({", ".join(f"{c} TEXT" for c in cols)})')
            conn.executemany(
                f'INSERT INTO {table} VALUES ({", ".join("?" for _ in cols)})',
                [tuple(row.get(c) for c in cols) for row in self._data]
            )
        conn.commit()
        conn.close()

    def auto_detect(self) -> Dict[str, Any]:
        """Auto-detect structured data on the page. Returns detected patterns."""
        if not self._soup:
            return {}
        result = {
            'tables': len(self._soup.select('table')),
            'lists': len(self._soup.select('ul, ol')),
            'articles': len(self._soup.select('article')),
            'cards': len(self._soup.select('[class*="card"]')),
            'products': len(self._soup.select('[class*="product"]')),
            'links': len(self._soup.select('a[href]')),
            'forms': len(self._soup.select('form')),
        }
        return result

    @property
    def data(self) -> List[Dict]:
        return self._data

    def __len__(self) -> int:
        return len(self._data)

    def __repr__(self) -> str:
        return f'Scraper(url={self.url!r}, items={len(self._data)})'


if __name__ == '__main__':
    print("QuickScraper - Python web scraping made simple")
    print("Usage: from quick_scraper import Scraper")
    print()
    print("Quick start:")
    print("  scraper = Scraper('https://example.com')")
    print("  data = scraper.extract('.item', {'title': 'h2', 'price': '.price'})")
    print("  scraper.to_csv('output.csv')")
