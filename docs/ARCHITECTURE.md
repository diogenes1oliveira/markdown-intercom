# Architecture

## Conceptual Model

This design follows the **actor model** pattern, similar to Elixir processes and their mailboxes:

- **Agents are actors** — Each agent is an independent process that can send and receive messages
- **INBOX.md is the mailbox** — Like an Elixir process mailbox, messages are appended to a queue and processed sequentially
- **Messages are immutable** — Once written, messages are never modified (append-only), similar to Erlang/Elixir's "let it crash" philosophy
- **Asynchronous communication** — Agents send messages without blocking, and recipients process them when ready
- **Location transparency** — Just as Elixir processes can communicate across nodes, agents can communicate across different storage backends (local files, Git, HTTP, etc.)

The key difference is that instead of in-memory message passing, communication happens through persistent markdown files, making conversations durable, version-controlled (via Git), and accessible across different systems and time periods.

## Protocol Details

### INBOX.md Structure

- **Write-ahead log (WAL)** — Append-only message queue
- **Email-style headers** — From, To, Date, Status, Re (for ACKs)
- **Monotonic numbering** — `Message #1`, `Message #2`, ... (never resets)
- **Status tracking** — UNREAD/ACK without mutating existing messages
- **Concurrency** — Git index locks or `flock` for safe concurrent writes
- **Rotation** — Max 100 messages per file, with automatic backup file creation

### THREAD.md Structure

- **Turn-based format** — Sequential conversation turns with timestamps
- **Request/Response pattern** — Synchronous communication model
- **Multi-participant support** — Multiple agents and humans in same thread
- **Git-friendly** — Each turn can be a commit, preserving conversation history

### Transport Agnosticism

The protocol is transport-agnostic: agents only need to read and write markdown files. The storage backend (local, Git, HTTP, etc.) is an implementation detail handled by the agent's environment.

## Documentation and Visualization

This project uses standardized formats for documenting and visualizing architecture:

- **Mermaid diagrams** — For sequence diagrams, flowcharts, and state diagrams
- **OpenAPI** — For REST API specifications and message schemas
- **AsyncAPI** — For asynchronous message protocols and event-driven architectures
- **C4 Model** — For system context, container, component, and code-level diagrams
- **ETL visualizations** — Easy-to-generate diagrams for data flow and transformation pipelines

All diagrams and specifications will be defined in markdown-compatible formats, making them version-controlled, human-readable, and easily integrated into documentation.

## Modeling Capabilities

The markdown-based communication protocol can model various real-world processes and interactions:

- **Company processes** — Business workflows, approval chains, and organizational communication
- **User interactions** — User journeys, session flows, and interaction patterns
- **Jobs** — Task scheduling, job queues, and execution workflows
- **Builds** — CI/CD pipelines, build processes, and deployment workflows
- **Data analytics** — Data pipelines, analysis workflows, and reporting processes
- **Clickstream** — User navigation patterns, event tracking, and behavioral analytics
- **And more** — Any process that can be represented as a sequence of messages or events between actors

By treating these as conversations between agents (whether human or automated), we can apply the same communication patterns, version control, and observability tools across different domains.
