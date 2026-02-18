set dotenv-load := true

default:
    just --list

# Run recipes from the Go project (src/gomdi)
go *args:
    cd src/gomdi && just {{args}}

# Lint markdown files
lint fix="" any="":
    .dev/lint.py --format markdown {{if fix}}--fix{{fi}} {{if any}}--any{{fi}} "**/*.md"
