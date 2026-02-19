#!/usr/bin/env python3

"""
Lint YAML, Markdown, Python files, or build and check mkdocs site.
Usage: lint.py --format markdown|yaml|docs|python:mypy|python:ruff [--fix] [--any] <glob1> <glob2> ...
"""

import argparse
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import List, Optional, Set

import pathspec


def log(level: str, message: str) -> None:
    """
    Log a message with timestamp and emoji prefix.
    
    Args:
        level: Log level (INFO, WARN, ERROR, SUCCESS, DEBUG)
        message: Message to log
        
    Behavior:
        Prints formatted message to stdout with timestamp and emoji.
        Format: "YYYY-MM-DD HH:MM:SS LEVEL - emoji message"
    """
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
    """
    Find repository root directory by searching for .markdownlint.json marker file.
    
    Args:
        start_dir: Starting directory to search from
        
    Returns:
        Path to repository root, or start_dir if not found
        
    Behavior:
        Walks up directory tree from start_dir until finding .markdownlint.json.
        Returns the directory containing that file, or start_dir if never found.
    """
    current = start_dir.resolve()
    while current != current.parent:
        if (current / '.markdownlint.json').exists():
            return current
        current = current.parent
    return start_dir


def load_markdownlint_ignore(repo_root: Path) -> pathspec.PathSpec:
    """
    Load ignore patterns from .markdownlintignore file using pathspec library.
    
    Args:
        repo_root: Repository root directory
        
    Returns:
        pathspec.PathSpec object with gitwildmatch patterns, empty if file doesn't exist
        
    Behavior:
        Reads .markdownlintignore from repo_root, filters out comments and empty lines,
        and returns a PathSpec configured for gitwildmatch pattern matching.
        Returns empty PathSpec if file doesn't exist.
    """
    ignore_file = repo_root / '.markdownlintignore'
    if not ignore_file.exists():
        return pathspec.PathSpec.from_lines('gitwildmatch', [])
    
    with open(ignore_file, 'r') as f:
        lines = [line.strip() for line in f if line.strip() and not line.strip().startswith('#')]
    
    return pathspec.PathSpec.from_lines('gitwildmatch', lines)


def should_ignore_file(file_path: Path, ignore_spec: pathspec.PathSpec, repo_root: Path) -> bool:
    """
    Check if a file matches ignore patterns using pathspec library.
    
    Args:
        file_path: Absolute path to file to check
        ignore_spec: pathspec.PathSpec with ignore patterns
        repo_root: Repository root directory
        
    Returns:
        True if file should be ignored, False otherwise
        
    Behavior:
        Converts file_path to relative path from repo_root, normalizes separators,
        and uses pathspec.match_file() to check if it matches any ignore pattern.
        Returns False if ignore_spec is empty or file is outside repo_root.
    """
    if not ignore_spec or not ignore_spec.patterns:
        return False
    
    # Convert to relative path from repo root for pattern matching
    try:
        rel_path = file_path.relative_to(repo_root)
        rel_path_str = str(rel_path).replace('\\', '/')  # Normalize separators
    except ValueError:
        # File is outside repo root, don't ignore
        return False
    
    # pathspec expects paths relative to repo root with forward slashes
    return ignore_spec.match_file(rel_path_str)


def expand_globs_with_git(globs: List[str]) -> Set[Path]:
    """
    Expand glob patterns to matching tracked files using git ls-files.
    
    Args:
        globs: List of glob patterns (e.g., ["*.md", "docs/**/*.yml"])
        
    Returns:
        Set of Path objects for matching tracked files
        
    Behavior:
        Runs 'git ls-files' to get all tracked files, then matches them against
        glob patterns using fnmatch and regex (for ** patterns). Falls back to
        expand_globs_with_find() if git is unavailable or repo has no tracked files.
    """
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
    """
    Expand glob patterns to matching files using Python's glob module (includes all files).
    
    Args:
        globs: List of glob patterns (e.g., ["*.md", "docs/**/*.yml"])
        
    Returns:
        Set of Path objects for matching files
        
    Behavior:
        Uses Path.rglob() for ** patterns and Path.glob() for simple patterns.
        Searches from current directory, includes gitignored files.
    """
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


def run_markdown_lint(file_path: Path, fix: bool, repo_root: Path, ignore_spec: Optional[pathspec.PathSpec] = None) -> bool:
    """
    Run markdownlint-cli on a single markdown file.
    
    Args:
        file_path: Path to markdown file to lint
        fix: If True, attempt to auto-fix issues
        repo_root: Repository root directory (for config file lookup)
        ignore_spec: Optional pathspec for ignore patterns
        
    Returns:
        True if linting passed or file was ignored, False on error
        
    Behavior:
        Checks ignore_spec first; if file matches, returns True without linting.
        Loads .markdownlint.json config if present. Runs npx markdownlint-cli
        with --fix flag if requested. Prints output and returns False on non-zero exit.
    """
    # Check if file should be ignored
    if ignore_spec and should_ignore_file(file_path, ignore_spec, repo_root):
        log('INFO', f'Skipping ignored file: {file_path}')
        return True
    
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
    """
    Run yamllint on a single YAML file.
    
    Args:
        file_path: Path to YAML file to lint
        
    Returns:
        True if linting passed, False on error
        
    Behavior:
        Tries system yamllint first, falls back to npx yaml-lint if not found.
        Uses 'standard' format. Prints output and returns False on non-zero exit.
    """
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


def run_mypy_lint(file_path: Path, repo_root: Path) -> bool:
    """
    Run mypy type checker on a single Python file.
    
    Args:
        file_path: Path to Python file to type check
        repo_root: Repository root directory (for config lookup)
        
    Returns:
        True if type checking passed, False on error
        
    Behavior:
        Runs 'uv run mypy' on the file, using mypy configuration from pyproject.toml.
        Prints output and returns False on non-zero exit or if mypy not found.
    """
    log('INFO', f'Type checking with mypy: {file_path}')
    
    try:
        result = subprocess.run(
            ['uv', 'run', 'mypy', str(file_path)],
            cwd=str(repo_root),
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
        log('ERROR', 'uv not found. Please install uv: https://github.com/astral-sh/uv')
        return False


def run_ruff_lint(file_path: Path, fix: bool, repo_root: Path) -> bool:
    """
    Run ruff linter on a single Python file.
    
    Args:
        file_path: Path to Python file to lint
        fix: If True, attempt to auto-fix issues
        repo_root: Repository root directory (for config lookup)
        
    Returns:
        True if linting passed, False on error
        
    Behavior:
        Runs 'uv run ruff check' (or 'ruff check --fix' if fix=True) on the file,
        using ruff configuration from pyproject.toml. Prints output and returns
        False on non-zero exit or if ruff not found.
    """
    log('INFO', f'Linting with ruff: {file_path}')
    
    try:
        cmd = ['uv', 'run', 'ruff', 'check']
        if fix:
            cmd.append('--fix')
        cmd.append(str(file_path))
        
        result = subprocess.run(
            cmd,
            cwd=str(repo_root),
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
        log('ERROR', 'uv not found. Please install uv: https://github.com/astral-sh/uv')
        return False


def lint_file(file_path: Path, format_type: str, fix: bool, repo_root: Path, ignore_spec: Optional[pathspec.PathSpec] = None) -> bool:
    """
    Lint a single file based on format type.
    
    Args:
        file_path: Path to file to lint
        format_type: Format type ('markdown', 'yaml', 'python:mypy', 'python:ruff')
        fix: If True, attempt to auto-fix issues (markdown and ruff only)
        repo_root: Repository root directory
        ignore_spec: Optional pathspec for ignore patterns (markdown only)
        
    Returns:
        True if linting passed, False on error or invalid format
        
    Behavior:
        Validates file exists, then delegates to appropriate linter function
        based on format_type. Returns False if file doesn't exist or format is invalid.
    """
    if not file_path.is_file():
        log('ERROR', f'File not found: {file_path}')
        return False
    
    if format_type == 'markdown':
        return run_markdown_lint(file_path, fix, repo_root, ignore_spec)
    elif format_type == 'yaml':
        return run_yaml_lint(file_path)
    elif format_type == 'python:mypy':
        return run_mypy_lint(file_path, repo_root)
    elif format_type == 'python:ruff':
        return run_ruff_lint(file_path, fix, repo_root)
    else:
        log('ERROR', f'Invalid format: {format_type}')
        return False


def run_docs_lint(repo_root: Path) -> bool:
    """
    Build mkdocs site to temporary directory and check for errors.
    
    Args:
        repo_root: Repository root directory
        
    Returns:
        True if build succeeded with no errors, False otherwise
        
    Behavior:
        Creates temporary directory, runs 'uv run mkdocs build' with 5-minute timeout,
        checks output for warnings/errors (missing links, nav items, etc.).
        Returns False if mkdocs.yml missing, build fails, or errors detected in output.
    """
    log('INFO', 'Building mkdocs site to check for errors...')
    
    # Create temporary directory for build output
    with tempfile.TemporaryDirectory() as tmpdir:
        build_dir = Path(tmpdir) / 'site'
        
        # Check if mkdocs.yml exists
        mkdocs_yml = repo_root / 'mkdocs.yml'
        if not mkdocs_yml.exists():
            log('ERROR', f'mkdocs.yml not found at {mkdocs_yml}')
            return False
        
        # Try to build with mkdocs
        try:
            # First check if uv is available
            result = subprocess.run(
                ['uv', 'run', 'mkdocs', 'build', '--site-dir', str(build_dir)],
                cwd=str(repo_root),
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            
            if result.returncode != 0:
                log('ERROR', 'mkdocs build failed')
                if result.stdout:
                    print(result.stdout, end='')
                if result.stderr:
                    print(result.stderr, end='', file=sys.stderr)
                return False
            
            # Parse output for warnings/errors
            output = result.stdout + result.stderr
            errors_found = False
            
            # Check for common mkdocs errors
            error_patterns = [
                ('WARNING', 'WARNING'),
                ('ERROR', 'ERROR'),
                ('not found', 'Missing file'),
                ('broken link', 'Broken link'),
                ('invalid', 'Invalid'),
            ]
            
            for pattern, label in error_patterns:
                if pattern.lower() in output.lower():
                    # Extract relevant lines
                    lines = output.split('\n')
                    for i, line in enumerate(lines):
                        if pattern.lower() in line.lower():
                            # Show context (3 lines before and after)
                            start = max(0, i - 3)
                            end = min(len(lines), i + 4)
                            context = '\n'.join(lines[start:end])
                            log('ERROR', f'{label} found:\n{context}')
                            errors_found = True
            
            # Check for missing nav items
            if 'not found in the documentation' in output.lower():
                log('ERROR', 'Missing navigation items detected')
                errors_found = True
            
            if errors_found:
                log('ERROR', 'mkdocs build completed but errors were found')
                return False
            
            log('SUCCESS', 'mkdocs build completed successfully with no errors')
            return True
            
        except FileNotFoundError:
            log('ERROR', 'uv not found. Please install uv: https://github.com/astral-sh/uv')
            return False
        except subprocess.TimeoutExpired:
            log('ERROR', 'mkdocs build timed out after 5 minutes')
            return False
        except Exception as e:
            log('ERROR', f'Unexpected error building mkdocs: {e}')
            return False


def main() -> int:
    parser = argparse.ArgumentParser(
        description='Lint YAML or Markdown files matching glob patterns.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  lint.py --format markdown "*.md"
  lint.py --format markdown --fix "docs/**/*.md"
  lint.py --format yaml "*.yml" "*.yaml"
  lint.py --format markdown --any "*.md"  # Include gitignored files
  lint.py --format python:mypy "**/*.py"  # Type check Python files
  lint.py --format python:ruff "**/*.py"  # Lint Python files
  lint.py --format python:ruff --fix "**/*.py"  # Lint and fix Python files
  lint.py --format docs  # Build and check mkdocs site
        """
    )
    
    parser.add_argument(
        '--format',
        required=True,
        choices=['markdown', 'yaml', 'docs', 'python:mypy', 'python:ruff'],
        help='File format to lint (markdown/yaml/python:mypy/python:ruff) or docs to build and check mkdocs site'
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
        '--debug-ignore',
        action='store_true',
        help='Print files that match ignore patterns (for debugging)'
    )
    parser.add_argument(
        'globs',
        nargs='*',
        help='One or more glob patterns (e.g., "*.md", "docs/**/*.yml"). Not used for docs format.'
    )
    
    args = parser.parse_args()
    
    # Find repo root
    script_dir = Path(__file__).parent
    repo_root = find_repo_root(script_dir)
    
    # Handle docs format separately
    if args.format == 'docs':
        if args.fix:
            log('WARN', '--fix not applicable to docs format')
        if args.any:
            log('WARN', '--any not applicable to docs format')
        if args.globs:
            log('WARN', 'Glob patterns not used for docs format, ignoring')
        return 0 if run_docs_lint(repo_root) else 1
    
    # Handle markdown/yaml/python formats
    if args.fix and args.format == 'yaml':
        log('WARN', 'YAML fix not implemented, only checking')
    if args.fix and args.format == 'python:mypy':
        log('WARN', 'mypy fix not implemented, only checking')
    
    if not args.globs:
        log('ERROR', 'At least one glob pattern required for markdown/yaml format')
        return 1
    
    # Expand globs
    if args.any:
        files = expand_globs_with_find(args.globs)
    else:
        files = expand_globs_with_git(args.globs)
    
    if not files:
        log('WARN', f'No files found matching glob patterns: {", ".join(args.globs)}')
        return 0
    
    # Load ignore patterns if needed (only for markdown)
    ignore_spec = None
    if args.format == 'markdown':
        ignore_spec = load_markdownlint_ignore(repo_root)
        if args.debug_ignore:
            log('INFO', f'Ignore patterns loaded: {len(ignore_spec.patterns)} patterns')
    
    # Lint all files
    failed = False
    ignored_count = 0
    for file_path in sorted(files):
        # Debug ignore matching
        if args.debug_ignore and args.format == 'markdown' and ignore_spec:
            if should_ignore_file(file_path, ignore_spec, repo_root):
                log('DEBUG', f'IGNORED: {file_path}')
                ignored_count += 1
                continue
        
        if not lint_file(file_path, args.format, args.fix, repo_root, ignore_spec):
            failed = True
    
    if args.debug_ignore:
        log('INFO', f'Total files ignored: {ignored_count}')
    
    if not failed:
        log('SUCCESS', 'All checks passed')
    
    return 1 if failed else 0


if __name__ == '__main__':
    sys.exit(main())
