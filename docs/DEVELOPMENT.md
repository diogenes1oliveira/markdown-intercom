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

Lint YAML files:
```bash
.dev/lint.py --format yaml "**/*.yml" "**/*.yaml"
```

Check mkdocs site for errors (missing links, nav items, etc.):
```bash
.dev/lint.py --format docs
```

### Documentation Development

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
- [Examples](examples/index.md) - Example implementations
- [Main README](../README.md) - Project overview
