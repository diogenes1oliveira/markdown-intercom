set dotenv-load := true

default:
    just --list

# Run recipes from the Go project (src/gomdi)
go *args:
    cd src/gomdi && just {{args}}

# Setup IDE environment (just-lsp, shfmt, etc.)
[group('dev')]
setup:
    bash .dev/setup-ide.sh

# Serve the documentation locally with auto-reload
[group('dev')]
dev:
    uv run mkdocs serve --livereload

# Lint markdown files
[group('dev')]
lint fix="" any="":
    uv run python .dev/lint.py --format markdown {{ if fix != "" { "--fix" } else { "" } }} {{ if any != "" { "--any" } else { "" } }} "**/*.md"

# Lint Python files with ruff
[group('dev')]
lint-python fix="" any="":
    uv run python .dev/lint.py --format python:ruff {{ if fix != "" { "--fix" } else { "" } }} {{ if any != "" { "--any" } else { "" } }} "**/*.py"

# Type check Python files with mypy
[group('dev')]
typecheck any="":
    uv run python .dev/lint.py --format python:mypy {{ if any != "" { "--any" } else { "" } }} "**/*.py"

# Build the prod documentation
[group('ci')]
build:
    uv run mkdocs build

# Deploy the prod documentation to GitHub Pages
[group('ci')]
deploy:
    uv run mkdocs build

# Deploy local site/ directory to GitHub Pages (commits site/ and triggers workflow)
[group('dev')]
deploy-site:
    bash .dev/deploy-site.sh
