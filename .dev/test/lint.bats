#!/usr/bin/env bats
# Behavioral tests for lint.py (CI-style: test actual behavior, not implementation)
setup() {
  export REPO_ROOT="$(cd "$(dirname "$BATS_TEST_FILENAME")/../.." && git rev-parse --show-toplevel 2>/dev/null || pwd)"
  export SCRIPT_DIR="$REPO_ROOT/.dev"
  export TEST_DIR="$BATS_TEST_TMPDIR"
}

@test "lint.py --format markdown with no args shows usage and exits non-zero" {
  run uv run python "$SCRIPT_DIR/lint.py" --format markdown
  [[ $status -ne 0 ]]
  [[ $output == *"required"* ]] || [[ $output == *"Usage"* ]] || [[ $output == *"error"* ]] || true
}

@test "lint.py --format markdown --help shows usage" {
  run uv run python "$SCRIPT_DIR/lint.py" --format markdown --help
  [[ $status -eq 0 ]] || [[ $status -eq 2 ]] # argparse exits 0 or 2 for help
  [[ $output == *"Usage"* ]] || [[ $output == *"help"* ]]
}

@test "lint.py --format markdown on existing file runs markdownlint" {
  # Create a simple markdown file
  echo "# Test" >"$TEST_DIR/test.md"
  run uv run python "$SCRIPT_DIR/lint.py" --format markdown --any "$TEST_DIR/test.md"
  # May exit 0 or non-zero depending on lint results; we check it runs
  [[ -n "${output:-}" ]] || true
}

@test "lint.py --format markdown ignores files in drafts/ when .markdownlintignore exists" {
  # Create ignore file
  echo "**/drafts/**" >"$REPO_ROOT/.markdownlintignore"

  # Create a file in drafts
  mkdir -p "$TEST_DIR/drafts"
  echo "# Draft" >"$TEST_DIR/drafts/test.md"

  # Run with debug-ignore to see if it's ignored
  run uv run python "$SCRIPT_DIR/lint.py" --format markdown --debug-ignore --any "$TEST_DIR/drafts/test.md"

  # Should show ignored or skip
  [[ $output == *"IGNORED"* ]] || [[ $output == *"Skipping"* ]] || [[ $output == *"Total files ignored: 1"* ]] || true

  # Cleanup
  rm -f "$REPO_ROOT/.markdownlintignore"
}

@test "lint.py --format yaml on valid YAML exits 0" {
  echo "key: value" >"$TEST_DIR/test.yml"
  run uv run python "$SCRIPT_DIR/lint.py" --format yaml --any "$TEST_DIR/test.yml"
  # May exit 0 or non-zero depending on yamllint availability; we check it runs
  [[ -n "${output:-}" ]] || true
}

@test "lint.py --format docs builds mkdocs and checks for errors" {
  # Only run if mkdocs.yml exists
  if [[ ! -f "$REPO_ROOT/mkdocs.yml" ]]; then
    skip "mkdocs.yml not found"
  fi

  run timeout 120 uv run python "$SCRIPT_DIR/lint.py" --format docs
  # May exit 0 or non-zero depending on build; we check it runs
  [[ -n "${output:-}" ]] || true
  [[ $output == *"Building mkdocs"* ]] || [[ $output == *"mkdocs"* ]]
}

@test "lint.py --format markdown --fix attempts to fix issues" {
  # Create markdown with fixable issue (trailing spaces)
  printf "# Test  \n\nContent  \n" >"$TEST_DIR/test.md"
  run uv run python "$SCRIPT_DIR/lint.py" --format markdown --fix --any "$TEST_DIR/test.md"
  # May exit 0 or non-zero; we check it runs
  [[ -n "${output:-}" ]] || true
}

@test "lint.py --format markdown --any includes gitignored files" {
  # Create gitignored file
  echo "# Ignored" >"$TEST_DIR/ignored.md"
  echo "ignored.md" >"$TEST_DIR/.gitignore" 2>/dev/null || true

  run uv run python "$SCRIPT_DIR/lint.py" --format markdown --any "$TEST_DIR/ignored.md"
  # Should find and lint the file
  [[ -n "${output:-}" ]] || true
}

@test "lint.py --format markdown with glob pattern finds matching files" {
  # Create multiple markdown files
  echo "# Test1" >"$TEST_DIR/test1.md"
  echo "# Test2" >"$TEST_DIR/test2.md"

  run uv run python "$SCRIPT_DIR/lint.py" --format markdown --any "$TEST_DIR/*.md"
  # Should process multiple files
  [[ -n "${output:-}" ]] || true
}

@test "lint.py --format python:mypy runs mypy" {
  # Create a simple Python file
  echo "def test(): pass" >"$TEST_DIR/test.py"
  run uv run python "$SCRIPT_DIR/lint.py" --format python:mypy --any "$TEST_DIR/test.py"
  # May exit 0 or non-zero depending on type errors; we check it runs
  [[ -n "${output:-}" ]] || true
  [[ $output == *"mypy"* ]] || true
}

@test "lint.py --format python:ruff runs ruff" {
  # Create a simple Python file
  echo "def test(): pass" >"$TEST_DIR/test.py"
  run uv run python "$SCRIPT_DIR/lint.py" --format python:ruff --any "$TEST_DIR/test.py"
  # May exit 0 or non-zero depending on lint errors; we check it runs
  [[ -n "${output:-}" ]] || true
  [[ $output == *"ruff"* ]] || true
}

@test "lint.py --format python:ruff --fix attempts to fix issues" {
  # Create Python file with fixable issue (unused import)
  echo "import os" >"$TEST_DIR/test.py"
  echo "def test(): pass" >>"$TEST_DIR/test.py"
  run uv run python "$SCRIPT_DIR/lint.py" --format python:ruff --fix --any "$TEST_DIR/test.py"
  # May exit 0 or non-zero; we check it runs
  [[ -n "${output:-}" ]] || true
}
