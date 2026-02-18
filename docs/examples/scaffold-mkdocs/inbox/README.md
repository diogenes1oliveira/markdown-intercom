# Inbox Example

This directory contains an example inbox (`main.md`) demonstrating the INBOX.md format for agent-to-agent messaging.

## Files

- [`index.md`](index.md) / [GitHub](https://github.com/diogenes1oliveira/markdown-intercom/blob/main/docs/examples/scaffold-mkdocs/inbox/index.md) - Inbox messages table
- [`main.md`](main.md) / [GitHub](https://github.com/diogenes1oliveira/markdown-intercom/blob/main/docs/examples/scaffold-mkdocs/inbox/main.md) - Simulated inbox state showing messages from the scaffold-mkdocs conversation
- [`drafts/`](drafts/README.md) / [GitHub](https://github.com/diogenes1oliveira/markdown-intercom/blob/main/docs/examples/scaffold-mkdocs/inbox/drafts/README.md) - Draft messages being composed

## Related Documentation

- [Project Root](https://github.com/diogenes1oliveira/markdown-intercom) - Main project repository
- [Architecture](../../../../ARCHITECTURE.md) / [GitHub](https://github.com/diogenes1oliveira/markdown-intercom/blob/main/ARCHITECTURE.md) - Technical architecture details
- [Thread](../THREAD.md) / [GitHub](https://github.com/diogenes1oliveira/markdown-intercom/blob/main/docs/examples/scaffold-mkdocs/THREAD.md) - Thread format example
- [Messages Example](../messages/README.md) / [GitHub](https://github.com/diogenes1oliveira/markdown-intercom/blob/main/docs/examples/scaffold-mkdocs/messages/README.md) - Messages directory with hive-style partitioning

## Inbox Format

The inbox follows the append-only write-ahead log (WAL) pattern:

- Messages use the format: `Turn #N, Agent = @handle, Message = M`
- Each message includes metadata (From, To, Date, Status, Re)
- Summaries provide brief descriptions of message content
- Status can be `ACK` (acknowledged) or `UNREAD`

See [`main.md`](main.md) / [GitHub](https://github.com/diogenes1oliveira/markdown-intercom/blob/main/docs/examples/scaffold-mkdocs/inbox/main.md) for a complete example.
