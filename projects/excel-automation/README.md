# Excel Automation Toolkit

> Automate your Excel workflows with Python. Merge, split, format, and generate reports in minutes, not hours.

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Stars](https://img.shields.io/github/stars/ZHOUZHOU-Yvonne/excel-automation)](https://github.com/ZHOUZHOU-Yvonne/excel-automation)

## Features

- **Report Generator** - Auto-generate formatted Excel reports from templates
- **Data Merger** - Merge multiple Excel files/sheets into one
- **Data Splitter** - Split large Excel files by criteria
- **Format Cleaner** - Clean and normalize Excel formatting
- **Chart Creator** - Create charts and visualizations programmatically

## Quick Start

```bash
pip install -r requirements.txt
```

```python
from excel_auto import ReportGenerator

# Generate a monthly report from data
gen = ReportGenerator('template.xlsx')
gen.fill_data(df)
gen.add_charts()
gen.save('monthly_report.xlsx')
```

## Why This Toolkit?

Manually processing Excel files is time-consuming and error-prone. This toolkit:
- **Saves hours** per week on repetitive Excel tasks
- **Reduces errors** with automated validation
- **Handles large files** efficiently (>100MB supported)
- **No Excel license needed** - works entirely in Python

## Use Cases

| Industry | Use Case |
|----------|----------|
| Finance | Monthly P&L reports, audit workpapers |
| HR | Payroll reports, attendance tracking |
| Sales | Pipeline reports, commission calculations |
| Operations | Inventory reports, KPI dashboards |

## Documentation

Full documentation at [docs/](docs/)

## Need Custom Solutions?

Contact for custom development:
- Enterprise Excel automation pipelines
- Integration with your existing systems
- Custom report templates and dashboards
- Training and support

---

**Built with ❤️ | [Hire me for custom development](https://github.com/ZHOUZHOU-Yvonne)**
