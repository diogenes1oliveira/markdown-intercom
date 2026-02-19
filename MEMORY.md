# Memory

Key learnings and important information to remember.

| Key | Value |
|:----|:------|
| `system-holiu-thread-path` | `/home/diogenes/projects/github.com/markdown-intercom/docs/examples/system-holiu/THREAD.md` |
| `system-holiu-purpose` | Example THREAD.md documenting a ChatGPT prompt engineering session, formatted for copying into a new project's README.md |
| `session-boundary-rule` | When documenting conversations in THREAD.md, each distinct conversation context (different agents, tools, time periods) should be its own Session #N |
| `wal-style-documentation` | THREAD.md follows Write-Ahead Log (WAL) style: append-only, never modify existing content. When unsure whether to add new session or modify existing, prefer creating new session |
| `slipup-session-documentation` | User wanted Session #2 added from the start when creating THREAD.md, but unclear wording led to misunderstanding. Issue was user's wording, not agent mistake, but should ask for clarification |
| `devindex-table-format` | Simple markdown table format like SQL SELECT output from dbeaver, can be represented as MAP<STRING, STRING> in SQL DDL |
| `memory-table-requirement` | MEMORY.md should contain simple key-value table summarizing most important learnings, formatted like devindex.md tables |
