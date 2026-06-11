# QuickScraper

> Python web scraping made simple. Extract data from any website in 3 lines of code.

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

## Features

- **Zero config** — Auto-detects tables, lists, and structured data
- **Smart pagination** — Handles "Load More", infinite scroll, and numbered pages
- **Auto-export** — CSV, JSON, Excel, or SQLite output
- **Anti-block** — Built-in delays, UA rotation, and cookie management
- **Browser support** — Optional Playwright backend for JS-heavy sites

## Quick Start

```bash
pip install quick-scraper
```

```python
from quick_scraper import Scraper

# Scrape a product listing
scraper = Scraper('https://books.toscrape.com')
products = scraper.extract('.product_pod', {
    'title': 'h3 a',
    'price': '.price_color',
    'link': 'h3 a @href',
    'image': 'img @src'
})

scraper.to_csv('books.csv')
print(f'Extracted {len(products)} products')
```

## One-liner mode

```bash
# Scrape a page to CSV
python -m quick_scraper https://example.com/table .data-table --output data.csv

# Scrape with pagination
python -m quick_scraper https://example.com/list .item --paginate --max-pages 10 --output items.json
```

## Use Cases

| Industry | Use Case |
|----------|----------|
| E-commerce | Price monitoring, competitor analysis |
| Real Estate | Property listings aggregation |
| Job Boards | Aggregate job postings |
| Research | Academic data collection |
| Finance | Market data extraction |
| News | Article aggregation and analysis |

## Documentation

Full docs at [quick-scraper.dev](https://github.com/ZHOUZHOU-Yvonne/quick-scraper/wiki)

## Need Custom Scraping?

Contact for custom development:
- Enterprise-scale data extraction pipelines
- Anti-detection and proxy rotation
- API integration and data delivery

---

**Built with ❤️ | [Hire me](https://github.com/ZHOUZHOU-Yvonne)**
