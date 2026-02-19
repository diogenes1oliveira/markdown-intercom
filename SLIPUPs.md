# SLIPUPs - Mistakes and Learnings

## Not Setting Up Bats Tests and Checking External Libraries

**What happened:**  
When implementing ignore pattern matching for `.markdownlintignore`, the agent implemented custom pattern matching logic instead of:
1. Setting up bats tests for CI-style behavioral testing
2. Checking if external libraries (like `pathspec`) could handle gitignore-style patterns
3. Adding proper docstrings documenting function behavior

**What should have been done:**

1. **Check external libraries first:** Before implementing custom pattern matching, search for Python libraries that handle gitignore-style patterns (e.g., `pathspec`)
2. **Set up bats tests immediately:** Create `test/lint.bats` with CI-style behavioral tests documenting expected behavior
3. **Add docstrings:** Document what each function should do (behavior) before implementing, then test that behavior
4. **CI-style testing:** Tests should verify actual behavior, not guess implementation details

**Fix applied:**

- Added `pathspec>=0.12.0` to `pyproject.toml` dependencies
- Replaced custom pattern matching with `pathspec.PathSpec.from_lines('gitwildmatch', ...)`
- Created `test/lint.bats` with 10 behavioral tests covering:
  - Usage/help output
  - Markdown/YAML/Docs format linting
  - Ignore pattern matching (with `--debug-ignore` flag)
  - `--fix`, `--any`, and glob pattern handling
- Added comprehensive docstrings to all functions documenting:
  - What the function should do (behavior)
  - Args and return values
  - Expected behavior in different scenarios
- Created `CI.md` documenting test behavior and results
- Added `--debug-ignore` flag to help debug ignore pattern matching

**Lesson:**  
Always check if external libraries can simplify code before implementing custom logic. Set up behavioral tests (bats) immediately to document and verify expected behavior. Add docstrings that describe what functions should do, then test that behavior. Don't guess—test CI-style.

---

## Not Using shfmt to Check Bash Syntax

**What happened:**  
When checking `.bats` file syntax, the agent used `bash -n` instead of `uv run shfmt` to check bash syntax.

**What should have been done:**

1. Use `uv run shfmt -d` to check syntax and formatting of bash/shell scripts
2. Format with `uv run shfmt -w` if needed
3. Don't try to run scripts if they have syntax issues

**Fix applied:**

- Used `uv run shfmt -w` to format `test/lint.bats`
- Updated workflow to use shfmt for syntax checking

**Lesson:**  
Always use `uv run shfmt` to check bash syntax for `.bats` files and shell scripts. Don't try to run scripts if they have syntax issues—fix them first.

---

## VSCode Settings JSON Trailing Commas

**What happened:**  
When updating `.vscode/settings.json`, the agent removed trailing commas to fix JSON syntax errors, not realizing VSCode settings files use JSONC (JSON with Comments) which supports trailing commas.

**What should have been done:**

1. Remove all trailing commas to validate JSON syntax
2. Run/validate the file
3. Add trailing commas back (since JSONC supports them)

**Fix applied:**

- Restored trailing commas in `.vscode/settings.json` after validation
- Documented that VSCode settings use JSONC format

**Lesson:**  
VSCode settings files are JSONC, not strict JSON. Always remove trailing commas to validate, then add them back for consistency.
