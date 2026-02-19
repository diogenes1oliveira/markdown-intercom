# CI / behavioral test documentation

Run all tests from the repository root:

```bash
bats .dev/test/
```

Install bats if needed: `npm install -g bats` or `apt install bats-core`.

---

## What each test file does

### .dev/test/lint.bats

**Script:** `.dev/lint.py` (lints markdown/yaml/python files or builds mkdocs site).

| Test | Behavior | Snippet |
|------|----------|--------|
| No args shows usage, exit non-zero | Run with --format but no globs; expect non-zero and "required" or "Usage". | `run uv run python "$SCRIPT_DIR/lint.py" --format markdown` |
| --help shows usage | Run --help; expect 0 or 2 and "Usage". | `run uv run python "$SCRIPT_DIR/lint.py" --format markdown --help` |
| On existing file runs markdownlint | Create temp .md, run lint; expect output (may exit 0 or non-zero). | `run uv run python "$SCRIPT_DIR/lint.py" --format markdown --any "$TEST_DIR/test.md"` |
| Ignores files in drafts/ when .markdownlintignore exists | Create .markdownlintignore with `**/drafts/**`, create file in drafts/, run with --debug-ignore; expect "IGNORED" or "Skipping" or "Total files ignored: 1". | `run uv run python "$SCRIPT_DIR/lint.py" --format markdown --debug-ignore --any "$TEST_DIR/drafts/test.md"` |
| On valid YAML exits appropriately | Create temp .yml, run lint; expect output (may exit 0 or non-zero depending on yamllint). | `run uv run python "$SCRIPT_DIR/lint.py" --format yaml --any "$TEST_DIR/test.yml"` |
| --format python:mypy runs mypy | Create temp .py, run type check; expect output (may exit 0 or non-zero). | `run uv run python "$SCRIPT_DIR/lint.py" --format python:mypy --any "$TEST_DIR/test.py"` |
| --format python:ruff runs ruff | Create temp .py, run lint; expect output (may exit 0 or non-zero). | `run uv run python "$SCRIPT_DIR/lint.py" --format python:ruff --any "$TEST_DIR/test.py"` |
| --format python:ruff --fix fixes issues | Create .py with fixable issue, run --fix; expect output. | `run uv run python "$SCRIPT_DIR/lint.py" --format python:ruff --fix --any "$TEST_DIR/test.py"` |
| --format docs builds mkdocs | Run --format docs; expect "Building mkdocs" or "mkdocs" in output (skips if mkdocs.yml missing). | `run timeout 120 uv run python "$SCRIPT_DIR/lint.py" --format docs` |
| --fix attempts to fix issues | Create .md with fixable issue, run --fix; expect output. | `run uv run python "$SCRIPT_DIR/lint.py" --format markdown --fix --any "$TEST_DIR/test.md"` |
| --any includes gitignored files | Create gitignored .md, run with --any; expect file is found and linted. | `run uv run python "$SCRIPT_DIR/lint.py" --format markdown --any "$TEST_DIR/ignored.md"` |
| Glob pattern finds matching files | Create multiple .md files, run with glob; expect multiple files processed. | `run uv run python "$SCRIPT_DIR/lint.py" --format markdown --any "$TEST_DIR/*.md"` |

**Note:** Tests that invoke `npx` (markdownlint-cli, yaml-lint), `uv run` (mypy, ruff, mkdocs) can be slow on first run or in constrained environments. The docs test has a 120s timeout. Tests check that commands run and produce output rather than asserting specific exit codes (since lint results vary).

---

## Test results (last run)

Run from the repository root and paste below:

```bash
bats .dev/test/
```

| Suite | Result | Notes |
|-------|--------|-------|
| lint.bats | ok 13 | Usage, help, markdown/yaml/python:mypy/python:ruff/docs formats, ignore patterns, --fix, --any, globs |

**Total:** 13 tests. Fast tests: usage, help. Slower (npx/uv): markdown lint, yaml lint, python linters (mypy, ruff), docs build. Tests use `uv run` to ensure dependencies are available.
