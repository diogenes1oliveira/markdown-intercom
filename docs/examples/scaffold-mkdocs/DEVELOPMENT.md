# Protocol

## Markdown and YAML Linting

After generating or modifying markdown or YAML files, always run the linting script:

```bash
../../.dev/lint.py --format markdown [--fix] [--any] <glob1> <glob2> ...
../../.dev/lint.py --format yaml [--any] <glob1> <glob2> ...
```

Or use the Justfile recipe from the repo root:

```bash
just lint          # Lint all tracked markdown files
just lint fix=1    # Lint and fix all tracked markdown files
just lint any=1    # Include gitignored files
```

The script:

- Requires `--format markdown|yaml` parameter
- Accepts glob patterns (e.g., `"*.md"`, `"docs/**/*.md"`)
- By default, only lints tracked files (uses `git ls-files`)
- Use `--any` flag to include gitignored files
- Uses `markdownlint-cli` for markdown files (with `.markdownlint.json` config from repo root)
- Uses `yamllint` or `npx yaml-lint` for YAML files
- Supports `--fix` flag to automatically fix markdown issues where possible (YAML fix not implemented)

**Important:** Always run the linting script at the end of any response that generates or modifies markdown or YAML files.

## Example-Specific Guidelines

This example demonstrates scaffolding mkdocs projects using the markdown-intercom protocol. Follow these guidelines:

1. **Check existing structure** - Before creating files, search for existing hive-style partitions or directory structures
2. **Use consistent naming** - Follow established naming conventions (e.g., `a.user.00N.md`, `b.bot.00N.md` for messages)
3. **Create index.md files** - For technical tables, create `index.md` files with just the tables (no headers)
4. **Create README.md files** - For user-friendly navigation, create `README.md` files that link to `index.md`
5. **Dual links** - Include both relative paths and GitHub repo paths in links: `[text](relative) / [GitHub](github-url)`
6. **Run linting** - Always run linting on generated files before completing the response
