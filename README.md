# markdown-intercom

Agents talking through Markdown

## Use Case

This project implements a file-based communication protocol for AI agents to communicate with each other and with humans using markdown files. The core idea is to enable agent-to-agent and human-to-agent messaging through simple file operations that work across different storage backends: local filesystems, Git repositories, GitHub Gists, HTTP endpoints, and more.

### Core Components

**INBOX.md** — A write-ahead log (WAL) for asynchronous messaging:

- Append-only message queue for agent-to-agent and human-to-agent communication
- Email-style headers (From, To, Date, Status, Re)
- Monotonic message numbering (`Message #1`, `Message #2`, ...)
- UNREAD/ACK status tracking without mutating existing messages
- Supports concurrent writes via Git index locks or file locking (`flock`)
- Automatic rotation (max 100 messages per file, with backup files)

**THREAD.md** — Structured conversation threads:

- Turn-based conversation format with timestamps
- Request/Response pattern for synchronous communication
- Supports multiple participants and sessions
- Human-readable timestamps and metadata
- Git-friendly format where each turn can be a commit

### Communication Channels

Agents can communicate through:

- **Local filesystem** — Direct file read/write operations
- **Git repositories** — Using commits as message delivery mechanism
- **GitHub Gists** — Sharing threads via raw markdown URLs
- **HTTP/HTTPS** — Fetching and posting markdown files via REST APIs
- **Any file-based storage** — As long as agents can read/write markdown files

The protocol is transport-agnostic: agents only need to read and write markdown files. The storage backend (local, Git, HTTP, etc.) is an implementation detail handled by the agent's environment.

## Documentation

- [Development Guide](docs/DEVELOPMENT.md) - Setup instructions and development workflow
- [Architecture](docs/ARCHITECTURE.md) - Technical architecture details
- [CI Tests](docs/CI.md) - Behavioral test documentation
- [Examples](docs/examples/index.md) - Example implementations

## Quick Start

1. Install dependencies: `uv sync`
2. Setup IDE tools: `just setup` (optional)
3. Serve documentation: `just dev`
4. Build documentation: `just build`
