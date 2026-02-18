#!/usr/bin/env python3

"""
Lint YAML and Markdown files.
Usage: lint.py --format markdown|yaml [--fix] [--any] <glob1> <glob2> ...
"""

import argparse
import glob
import os
import subprocess
import sys
from pathlib import Path
from typing import List, Set


def log(level: str, message: str) -> None:
    """Log a message with timestamp and emoji."""
    import datetime
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    emojis = {
        'INFO': 'ℹ️ ',
        'WARN': '⚠️ ',
        'ERROR': '❌',
        'SUCCESS': '✅',
        'DEBUG': '🔍',
    }
    emoji = emojis.get(level, '📝')
    print(f"{timestamp} {level} - {emoji} {message}")


def find_repo_root(start_dir: Path) -> Path:
    """Find repo root by looking for .markdownlint.json."""
    current = start_dir.resolve()
    while current != current.parent:
        if (current / '.markdownlint.json').exists():
            return current
        current = current.parent
    return start_dir


def expand_globs_with_git(globs: List[str]) -> Set[Path]:
    """Expand globs using git ls-files (only tracked files)."""
    files = set()
    
    try:
        result = subprocess.run(
            ['git', 'ls-files'],
            capture_output=True,
            text=True,
            check=True
        )
        tracked_files = result.stdout.strip().split('\n')
    except (subprocess.CalledProcessError, FileNotFoundError):
        log('WARN', 'git not found or not a git repo, falling back to find')
        return expand_globs_with_find(globs)
    
    if not tracked_files or tracked_files == ['']:
        log('WARN', 'No tracked files found, falling back to find')
        return expand_globs_with_find(globs)
    
    # Convert globs to patterns and match against tracked files
    import fnmatch
    import re
    
    for glob_pattern in globs:
        # Convert ** glob pattern to regex for matching
        # fnmatch doesn't support **, so we need to handle it specially
        if '**' in glob_pattern:
            # Convert glob pattern to regex:
            # ** matches any number of directories
            # * matches any characters except /
            # ? matches single character except /
            regex_pattern = glob_pattern
            # Escape dots first
            regex_pattern = regex_pattern.replace('.', r'\.')
            # Replace ** with .* (matches any characters including /)
            regex_pattern = regex_pattern.replace('**', '__DOUBLE_STAR__')
            # Replace * with [^/]* (matches any chars except /)
            regex_pattern = regex_pattern.replace('*', '[^/]*')
            # Replace ? with . (matches single char except /)
            regex_pattern = regex_pattern.replace('?', '[^/]')
            # Restore ** as .*
            regex_pattern = regex_pattern.replace('__DOUBLE_STAR__', '.*')
            
            compiled = re.compile(f'^{regex_pattern}$')
            for tracked_file in tracked_files:
                if tracked_file and compiled.match(tracked_file):
                    file_path = Path(tracked_file)
                    if file_path.is_file():
                        files.add(file_path)
        else:
            # Use fnmatch for simple patterns (no **)
            for tracked_file in tracked_files:
                if tracked_file and fnmatch.fnmatch(tracked_file, glob_pattern):
                    file_path = Path(tracked_file)
                    if file_path.is_file():
                        files.add(file_path)
    
    return files


def expand_globs_with_find(globs: List[str]) -> Set[Path]:
    """Expand globs using Python's glob module (includes all files)."""
    files = set()
    
    for glob_pattern in globs:
        # Handle ** patterns with rglob
        if '**' in glob_pattern:
            # Replace ** with * for rglob
            pattern = glob_pattern.replace('**', '*')
            # Remove leading ./ if present
            if pattern.startswith('./'):
                pattern = pattern[2:]
            # Use rglob for recursive matching
            for file_path in Path('.').rglob(pattern):
                if file_path.is_file():
                    files.add(file_path)
        else:
            # Use regular glob
            for file_path in Path('.').glob(glob_pattern):
                if file_path.is_file():
                    files.add(file_path)
    
    return files


def run_markdown_lint(file_path: Path, fix: bool, repo_root: Path) -> bool:
    """Run markdownlint on a file."""
    log('INFO', f'Linting markdown: {file_path}')
    
    config_arg = []
    config_file = repo_root / '.markdownlint.json'
    if config_file.exists():
        config_arg = ['--config', str(config_file)]
    
    cmd = ['npx', '-y', 'markdownlint-cli'] + config_arg
    if fix:
        cmd.append('--fix')
    cmd.append(str(file_path))
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            if result.stdout:
                print(result.stdout, end='')
            if result.stderr:
                print(result.stderr, end='', file=sys.stderr)
            return False
        return True
    except FileNotFoundError:
        log('ERROR', 'npx not found. Please install Node.js and npm.')
        return False


def run_yaml_lint(file_path: Path) -> bool:
    """Run yamllint on a file."""
    log('INFO', f'Linting YAML: {file_path}')
    
    # Try system yamllint first
    try:
        result = subprocess.run(
            ['yamllint', '-f', 'standard', str(file_path)],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            return True
        if result.stdout:
            print(result.stdout, end='')
        if result.stderr:
            print(result.stderr, end='', file=sys.stderr)
        return False
    except FileNotFoundError:
        # Fall back to npx yaml-lint
        log('INFO', 'Using npx yaml-lint (auto-install if needed)')
        try:
            result = subprocess.run(
                ['npx', '-y', 'yaml-lint', str(file_path)],
                capture_output=True,
                text=True
            )
            if result.returncode != 0:
                if result.stdout:
                    print(result.stdout, end='')
                if result.stderr:
                    print(result.stderr, end='', file=sys.stderr)
                return False
            return True
        except FileNotFoundError:
            log('ERROR', 'Neither yamllint nor npx found.')
            return False


def lint_file(file_path: Path, format_type: str, fix: bool, repo_root: Path) -> bool:
    """Lint a single file."""
    if not file_path.is_file():
        log('ERROR', f'File not found: {file_path}')
        return False
    
    if format_type == 'markdown':
        return run_markdown_lint(file_path, fix, repo_root)
    elif format_type == 'yaml':
        return run_yaml_lint(file_path)
    else:
        log('ERROR', f'Invalid format: {format_type}')
        return False


def main():
    parser = argparse.ArgumentParser(
        description='Lint YAML or Markdown files matching glob patterns.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  lint.py --format markdown "*.md"
  lint.py --format markdown --fix "docs/**/*.md"
  lint.py --format yaml "*.yml" "*.yaml"
  lint.py --format markdown --any "*.md"  # Include gitignored files
        """
    )
    
    parser.add_argument(
        '--format',
        required=True,
        choices=['markdown', 'yaml'],
        help='File format to lint'
    )
    parser.add_argument(
        '--fix',
        action='store_true',
        help='Attempt to fix issues automatically (markdown only)'
    )
    parser.add_argument(
        '--any',
        action='store_true',
        help='Include gitignored files (default: only tracked files)'
    )
    parser.add_argument(
        'globs',
        nargs='+',
        help='One or more glob patterns (e.g., "*.md", "docs/**/*.yml")'
    )
    
    args = parser.parse_args()
    
    if args.fix and args.format == 'yaml':
        log('WARN', 'YAML fix not implemented, only checking')
    
    # Find repo root
    script_dir = Path(__file__).parent
    repo_root = find_repo_root(script_dir)
    
    # Expand globs
    if args.any:
        files = expand_globs_with_find(args.globs)
    else:
        files = expand_globs_with_git(args.globs)
    
    if not files:
        log('WARN', f'No files found matching glob patterns: {", ".join(args.globs)}')
        return 0
    
    # Lint all files
    failed = False
    for file_path in sorted(files):
        if not lint_file(file_path, args.format, args.fix, repo_root):
            failed = True
    
    if not failed:
        log('SUCCESS', 'All checks passed')
    
    return 1 if failed else 0


if __name__ == '__main__':
    sys.exit(main())
