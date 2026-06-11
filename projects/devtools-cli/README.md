# organize-cli

> Tidy up any folder in one command. Sort files by type, date, or custom rules.

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://python.org)

## Features

- **Auto-categorize** — Images, Documents, Videos, Archives, Code, and more
- **Smart grouping** — By extension, creation date, file size, or regex pattern
- **Dry-run mode** — Preview changes before moving anything
- **Undo support** — Revert the last organization
- **Configurable** — Custom rules via `.organize.yaml`

## Install

```bash
pip install organize-cli
```

## Usage

```bash
# Organize current directory
organize

# Dry run (preview only)
organize --dry-run

# Organize by date (group files by month)
organize --by date

# Undo last operation
organize --undo

# Use custom rules file
organize --config my-rules.yaml
```

## Before → After

```
Downloads/                          Downloads/
├── photo1.jpg                      ├── Images/
├── photo2.png                      │   ├── photo1.jpg
├── report.pdf                      │   └── photo2.png
├── song.mp3                        ├── Documents/
├── video.mp4                       │   └── report.pdf
├── script.py                       ├── Audio/
├── data.csv                        │   └── song.mp3
├── archive.zip                     ├── Video/
└── notes.txt                       │   └── video.mp4
                                    ├── Code/
                                    │   └── script.py
                                    ├── Data/
                                    │   └── data.csv
                                    ├── Archives/
                                    │   └── archive.zip
                                    └── Text/
                                        └── notes.txt
```

## Custom Rules

Create `.organize.yaml`:

```yaml
rules:
  - name: Work Projects
    match: "*-work-*"
    target: "Work/{year}/{month}/"
  
  - name: Screenshots
    match: "Screenshot*"
    target: "Screenshots/"
  
  - name: Old Files
    match: "*.log"
    older_than: 30d
    action: delete
```

## Like this tool?

I build custom CLI tools, automation scripts, and developer utilities. Contact for freelance work.
