set dotenv-load := true

default:
    just --list

# Run recipes from the Go project (src/gomdi)
go *args:
    cd src/gomdi && just {{args}}

# Setup IDE environment (just-lsp, shfmt, etc.)
[group('dev')]
setup:
    uv run bash .dev/setup-ide.sh

# Serve the documentation locally with auto-reload
[group('dev')]
dev:
    uv run mkdocs serve --livereload

# Lint markdown files
[group('dev')]
lint fix="" any="":
    .dev/lint.py --format markdown {{if fix}}--fix{{fi}} {{if any}}--any{{fi}} "**/*.md"

# Build the prod documentation
[group('ci')]
build:
    uv run mkdocs build

# Deploy the prod documentation to GitHub Pages
[group('ci')]
deploy:
    uv run mkdocs build
