# SLIPUPs - Mistakes and Learnings

## Creating Messages in Wrong Location

**What happened:**  
When asked to split messages into a messages folder with hive-style partitioning, the agent created files in `docs/messages/` instead of checking for and using the existing structure in `docs/examples/messages/` where `turn=1/user.001.md` already existed.

**What should have been done:**

1. Search for existing hive-style partition structures (e.g., `turn=1/`, `turn=N/` directories)
2. If found, use that existing structure
3. If not found or unclear, ask the user for clarification about the location and structure
4. Never assume the location without checking first

**Fix applied:**

- Moved all created files from `docs/messages/` to `docs/examples/messages/`
- Updated `docs/examples/messages/devindex.md` with the correct table
- Removed the incorrectly created `docs/messages/` directory

**Lesson:**  
Always search for existing structures before creating new ones. When the user mentions they've already created something, find it first and ask for clarification if it's not immediately clear where it is or how it's structured.

---

## Choosing Naming Conventions Without User Input

**What happened:**  
When asked to rename message files with a prefix that conveys the user is the initiator, the agent chose "init" without providing alternatives for the user to choose from.

**What should have been done:**  
For stylistic choices, especially user-visible names and naming conventions, provide multiple alternatives and let the user choose rather than making a unilateral decision.

**Alternatives that should have been presented:**

- `1.user.001.md` / `1.bot.001.md` - Number prefix, sorts first
- `a.user.001.md` / `a.bot.001.md` - Letter prefix, sorts first alphabetically
- `first.user.001.md` / `first.bot.001.md` - Descriptive word
- `lead.user.001.md` / `lead.bot.001.md` - Leader/leading prefix
- `req.user.001.md` / `req.bot.001.md` - Request prefix (shorter)

**Lesson:**  
When making stylistic or naming decisions that affect user-visible files, always provide multiple alternatives and ask the user to choose rather than picking one unilaterally.

---

## Not Running Linting Script After Generating Markdown Files

**What happened:**  
After generating multiple markdown files (devindex.md, README.md files, etc.), the agent did not run the linting script to verify and fix markdown syntax issues.

**What should have been done:**

1. After generating or modifying any markdown files, always run `.dev/verify-channel.sh --fix` on those files
2. The script uses `.markdownlint.json` config from the repo root
3. Apply fixes automatically where possible using the `--fix` flag
4. Document this requirement in PROTOCOL.md

**Fix applied:**

- Copied `verify-channel.sh` to `.dev/verify-channel.sh`
- Added missing `run_markdown_lint` function to the script
- Updated script to use `.markdownlint.json` config from repo root
- Copied `.markdownlint.json` to repo root
- Updated PROTOCOL.md with linting requirements
- Added entry to SLIPUPs.md

**Lesson:**  
Always run `.dev/verify-channel.sh --fix` on all generated markdown files at the end of any response that creates or modifies markdown files. This ensures consistent formatting and catches syntax issues early.

---

## Making Justfile Too Complex Instead of Delegating to .dev Scripts

**What happened:**  
The Justfile was made complex with inline bash logic instead of keeping it simple and delegating to scripts in `.dev/`.

**What should have been done:**

1. Keep Justfile simple - it should just invoke commands in `.dev/`
2. Put complex logic in `.dev/` scripts
3. Scripts should accept clear parameters (e.g., `--format markdown|yaml` and file paths)
4. Justfile recipes should be thin wrappers that call `.dev/` scripts

**Fix applied:**

- Renamed `verify-channel.sh` to `lint.sh`
- Refactored `lint.sh` to accept mandatory `--format markdown|yaml` parameter and list of file paths
- Simplified Justfile to just invoke `.dev/lint.sh` with appropriate arguments
- Updated PROTOCOL.md to reference the new script

**Lesson:**  
Justfile should be very simple and just invoke commands in `.dev/`. Complex logic belongs in the scripts themselves, not in Justfile recipes.
