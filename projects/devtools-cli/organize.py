#!/usr/bin/env python3
"""
organize-cli — Tidy up any folder in one command.
"""
import os, sys, json, shutil, argparse
from pathlib import Path
from datetime import datetime
from collections import defaultdict

CATEGORIES = {
    'Images':    ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp', '.ico', '.tiff', '.heic'],
    'Documents': ['.pdf', '.doc', '.docx', '.ppt', '.pptx', '.xls', '.xlsx', '.odt', '.pages', '.key'],
    'Audio':     ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a', '.wma'],
    'Video':     ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm', '.m4v'],
    'Archives':  ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', '.xz', '.dmg', '.iso'],
    'Code':      ['.py', '.js', '.ts', '.jsx', '.tsx', '.html', '.css', '.scss', '.java',
                  '.c', '.cpp', '.h', '.rs', '.go', '.rb', '.php', '.swift', '.kt', '.sh',
                  '.json', '.xml', '.yaml', '.yml', '.toml', '.ini', '.cfg', '.env'],
    'Data':      ['.csv', '.tsv', '.sql', '.sqlite', '.db', '.parquet', '.feather'],
    'Fonts':     ['.ttf', '.otf', '.woff', '.woff2', '.eot'],
    'Text':      ['.txt', '.md', '.rst', '.log', '.readme'],
}

HISTORY_FILE = os.path.expanduser('~/.organize_history.json')


def get_category(filepath):
    ext = filepath.suffix.lower()
    for cat, exts in CATEGORIES.items():
        if ext in exts:
            return cat
    return 'Other'


def organize_by_type(directory, dry_run=False):
    """Organize files into category folders."""
    moves = []
    for item in directory.iterdir():
        if item.is_file() and not item.name.startswith('.'):
            cat = get_category(item)
            target = directory / cat / item.name
            if target != item:
                moves.append((item, target))

    if dry_run:
        return moves

    for src, dst in moves:
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(src), str(dst))

    _save_history(moves)
    return moves


def organize_by_date(directory, dry_run=False):
    """Organize files into year/month folders based on modification time."""
    moves = []
    for item in directory.iterdir():
        if item.is_file() and not item.name.startswith('.'):
            mtime = datetime.fromtimestamp(item.stat().st_mtime)
            target = directory / str(mtime.year) / f'{mtime.month:02d}' / item.name
            moves.append((item, target))

    if dry_run:
        return moves

    for src, dst in moves:
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(src), str(dst))

    _save_history(moves)
    return moves


def undo_last():
    """Undo the last organization operation."""
    if not os.path.exists(HISTORY_FILE):
        print('No history found.')
        return

    with open(HISTORY_FILE) as f:
        history = json.load(f)

    if not history:
        print('Nothing to undo.')
        return

    last = history[-1]
    print(f'Undoing {len(last)} moves...')

    for src, dst in last:
        src_path = Path(src)
        dst_path = Path(dst)
        if dst_path.exists():
            src_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(dst_path), str(src_path))
        # Clean up empty dirs
        if dst_path.parent.exists():
            try:
                dst_path.parent.rmdir()
            except OSError:
                pass

    history.pop()
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f)

    print('Undo complete.')


def _save_history(moves):
    history = []
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE) as f:
            history = json.load(f)
    history.append([(str(s), str(d)) for s, d in moves])
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f)


def print_summary(moves, dry_run):
    if not moves:
        print('Nothing to organize — directory is already clean!')
        return

    groups = defaultdict(list)
    for src, dst in moves:
        cat = dst.parent.name if len(dst.parents) > len(src.parents) else 'root'
        groups[cat].append(src.name)

    prefix = '[DRY RUN] ' if dry_run else ''
    print(f'\n{prefix}Organized {len(moves)} files:')
    for cat, files in sorted(groups.items()):
        print(f'  📁 {cat}/ ({len(files)} files)')

    if dry_run:
        print('\nRun without --dry-run to apply changes.')


def main():
    parser = argparse.ArgumentParser(description='Organize files in a directory.')
    parser.add_argument('directory', nargs='?', default='.',
                        help='Directory to organize (default: current)')
    parser.add_argument('--by', choices=['type', 'date'], default='type',
                        help='Organization method (default: type)')
    parser.add_argument('--dry-run', action='store_true',
                        help='Preview changes without moving files')
    parser.add_argument('--undo', action='store_true',
                        help='Undo the last organization')

    args = parser.parse_args()

    if args.undo:
        undo_last()
        return

    directory = Path(args.directory).resolve()
    if not directory.is_dir():
        print(f'Error: {directory} is not a directory')
        sys.exit(1)

    if args.by == 'date':
        moves = organize_by_date(directory, dry_run=args.dry_run)
    else:
        moves = organize_by_type(directory, dry_run=args.dry_run)

    print_summary(moves, args.dry_run)


if __name__ == '__main__':
    main()
