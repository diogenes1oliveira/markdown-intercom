# Development Guide

This guide covers the setup and development workflow for the markdown-intercom project.

## Requirements

### System Requirements

- **Python 3.9+** - Required for running mkdocs and Python tooling
- **uv** - Fast Python package installer and resolver ([install](https://github.com/astral-sh/uv))
- **just** - Command runner ([install](https://github.com/casey/just))
- **Node.js** - Required for markdownlint-cli (for linting)
- **Git** - Version control

### Optional Tools

- **Rust/Cargo** - Required for installing `just-lsp` (via `just setup`)
- **Go** - Required for installing `shfmt` (via `just setup`)

## Initial Setup

1. **Clone the repository:**

    ```bash
    git clone https://github.com/diogenes1oliveira/markdown-intercom.git
    cd markdown-intercom
    ```

2. **Install dependencies:**

    ```bash
    uv sync
    ```

3. **Setup IDE tools (optional but recommended):**

    ```bash
    just setup
    ```

    This installs:
    - `just-lsp` - Language server for Justfiles
    - `shfmt` - Shell script formatter

## Development Workflow

### Linting

Lint markdown files:

```bash
just lint                    # Lint tracked markdown files
just lint fix=true           # Lint and auto-fix markdown files
just lint any=true           # Include gitignored files
```

Lint Python files:

```bash
just lint-python                    # Lint Python files with ruff
just lint-python fix=true           # Lint and auto-fix Python files
just lint-python any=true           # Include gitignored files
just typecheck                      # Type check Python files with mypy
```

Lint YAML files:

```bash
uv run python .dev/lint.py --format yaml "**/*.yml" "**/*.yaml"
```

Lint Python files directly:

```bash
uv run python .dev/lint.py --format python:ruff "**/*.py"
uv run python .dev/lint.py --format python:ruff --fix "**/*.py"  # Auto-fix
uv run python .dev/lint.py --format python:mypy "**/*.py"        # Type check
```

Check mkdocs site for errors (missing links, nav items, etc.):

```bash
uv run python .dev/lint.py --format docs
```

### Documentation Development

**MkDocs and the `docs/` sandbox:** MkDocs only serves files under `docs/`. Do not link to files outside that directory (e.g. the repository root `README.md`) using relative paths like `../README.md` — the build will fail or the link will be broken. For the project root README or any file outside `docs/`, use the GitHub URL instead (e.g. `https://github.com/diogenes1oliveira/markdown-intercom/blob/main/README.md`).

**Index section pattern:** Always include an "Index" section (like in `docs/examples/README.md`) at the top of markdown files that contain multiple sections or messages. This helps with navigation and avoids duplicate heading warnings (MD024). For files with repeated headings like "Summary", make them unique by adding context (e.g., `#### Summary: Turn #1, Message #1`).

**Serve documentation locally:**

```bash
just dev
```

This starts a local mkdocs server with live reload at `http://127.0.0.1:8000`.

**Build documentation:**

```bash
just build
```

This builds the static site to the `site/` directory.

**Deploy to GitHub Pages:**

You can deploy the built `site/` directory to GitHub Pages in three ways:

1. **Automatic deployment** (on push to `main`): The `.github/workflows/deploy.yml` workflow automatically builds and deploys the site.

2. **Manual deployment from local `site/`** (recommended, no commits to your branch): Deploy your locally built `site/` directory without affecting your current branch:

   ```bash
   just build          # Build the site
   just deploy-site    # Deploy without committing to current branch
   ```

   This script uses a temporary branch and git worktree to deploy your local `site/` directory without committing to your current branch. Perfect for rapid iteration during development!

3. **Manual deployment** (from VS Code GitHub Actions extension):
   - Build the site locally: `just build`
   - Commit the `site/` directory: `git add site/ && git commit -m "Update site"`
   - Open the GitHub Actions extension in VS Code
   - Find "Deploy site/ to GitHub Pages" workflow
   - Click "Run workflow" to trigger manual deployment

**Note:** The `just deploy-site` command creates a temporary branch, pushes your local `site/` there, triggers the workflow, and cleans up—all without touching your current branch or working directory.

**Check for documentation errors:**

```bash
.dev/lint.py --format docs
```

This builds the site to a temporary directory and checks for:

- Missing links
- Broken navigation items
- Build errors
- Warnings

### Project Structure

- `docs/` - Documentation source files
  - `index.md` - Home page
  - `ARCHITECTURE.md` - Technical architecture
  - `examples/` - Example implementations
- `mkdocs.yml` - MkDocs configuration
- `pyproject.toml` - Python project configuration and dependencies
- `.dev/` - Development scripts
  - `lint.py` - Linting script for markdown, YAML, and docs
  - `setup-ide.sh` - IDE setup script
- `.github/workflows/` - CI/CD workflows
  - `deploy.yml` - GitHub Pages deployment

## IDE Setup

The project includes a setup script that installs IDE tools:

```bash
just setup
```

This installs:

- **just-lsp** - Provides language server support for Justfiles in your IDE
- **shfmt** - Shell script formatter for consistent bash script formatting

### Environment Variables

You can customize the setup behavior with environment variables:

- `DEV_IDE_COMMANDS` - Comma-separated list of IDE commands (default: `code`)
- `DEV_ADHOC_VSIX_URLS` - Comma-separated URLs of .vsix extensions to install
- `DEV_DRY_RUN` - Set to `1` to see what would be installed without actually installing
- `DEV_NO_ENVFILE` - Set to `1` to skip loading `.env` file

Example:

```bash
DEV_IDE_COMMANDS="code,cursor" just setup
```

## CI/CD

The project uses GitHub Actions for continuous integration and deployment:

- **Deploy workflow** (`.github/workflows/deploy.yml`):
  - Triggers on push to `main` branch
  - Builds mkdocs site using `uv` and Python 3.9
  - Deploys to GitHub Pages

## Troubleshooting

### mkdocs build fails

1. Ensure all dependencies are installed: `uv sync`
2. Check for missing files referenced in `mkdocs.yml` nav
3. Run lint check: `.dev/lint.py --format docs`

### Linting errors

- For markdown: Run `just lint fix=true` to auto-fix issues
- For YAML: Check syntax manually or use `yamllint`
- For docs: Check the build output for specific error messages

### IDE tools not working

- Ensure `just setup` completed successfully
- Check that tools are in `.venv/bin/`:

    ```bash
    ls -la .venv/bin/just-lsp .venv/bin/shfmt
    ```

- Verify PATH includes `.venv/bin` or configure your IDE to use it

## Related Documentation

- [Architecture](ARCHITECTURE.md) - Technical architecture details
- [CI Tests](CI.md) - Behavioral test documentation
- [Examples](examples/devindex.md) - Example implementations
- [Main README](https://github.com/diogenes1oliveira/markdown-intercom/blob/main/README.md) - Project overview
