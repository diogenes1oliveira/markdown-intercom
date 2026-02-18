# Development Guide

This document describes the structure and purpose of files in this example.

## Main Documentation

- [`README.md`](README.md) / [GitHub](https://github.com/diogenes1oliveira/markdown-intercom/blob/main/docs/examples/scaffold-mkdocs/README.md) - User-friendly overview of the example with links to hive-like table structures and main contents
- [`index.md`](index.md) / [GitHub](https://github.com/diogenes1oliveira/markdown-intercom/blob/main/docs/examples/scaffold-mkdocs/index.md) - Technical index table listing all markdown files with relative and GitHub paths

## Protocol and Agent Documentation

- [`PROTOCOL.md`](PROTOCOL.md) / [GitHub](https://github.com/diogenes1oliveira/markdown-intercom/blob/main/docs/examples/scaffold-mkdocs/PROTOCOL.md) - Communication protocol and guidelines for this example
- [`AGENTS.md`](AGENTS.md) / [GitHub](https://github.com/diogenes1oliveira/markdown-intercom/blob/main/docs/examples/scaffold-mkdocs/AGENTS.md) - Instructions for agents working with this example
- [`ONBOARDING.md`](ONBOARDING.md) / [GitHub](https://github.com/diogenes1oliveira/markdown-intercom/blob/main/docs/examples/scaffold-mkdocs/ONBOARDING.md) - Onboarding guide for new agents joining this example
- [`SLIPUPs.md`](SLIPUPs.md) / [GitHub](https://github.com/diogenes1oliveira/markdown-intercom/blob/main/docs/examples/scaffold-mkdocs/SLIPUPs.md) - Log of mistakes and learnings specific to this example

## Conversation Thread

- [`THREAD.md`](THREAD.md) / [GitHub](https://github.com/diogenes1oliveira/markdown-intercom/blob/main/docs/examples/scaffold-mkdocs/THREAD.md) - Complete conversation thread showing the turn-based interaction between user and agent scaffolding the mkdocs website

## Message Structure

### Messages Directory

- [`messages/README.md`](messages/README.md) / [GitHub](https://github.com/diogenes1oliveira/markdown-intercom/blob/main/docs/examples/scaffold-mkdocs/messages/README.md) - User-friendly overview of the messages directory
- [`messages/index.md`](messages/index.md) / [GitHub](https://github.com/diogenes1oliveira/markdown-intercom/blob/main/docs/examples/scaffold-mkdocs/messages/index.md) - Technical table of all messages organized by turn

### Turn Directories

Each turn directory (`turn=1/`, `turn=2/`) contains:

- `README.md` - User-friendly overview with links to messages
- `index.md` - Technical table listing messages in that turn
- `a.user.00N.md` - User message files (verbatim from THREAD.md)
- `b.bot.00N.md` - Bot message files (verbatim from THREAD.md)

## Inbox Structure

### Inbox Directory

- [`inbox/README.md`](inbox/README.md) / [GitHub](https://github.com/diogenes1oliveira/markdown-intercom/blob/main/docs/examples/scaffold-mkdocs/inbox/README.md) - Overview of the inbox example
- [`inbox/index.md`](inbox/index.md) / [GitHub](https://github.com/diogenes1oliveira/markdown-intercom/blob/main/docs/examples/scaffold-mkdocs/inbox/index.md) - Technical table of inbox messages
- [`inbox/main.md`](inbox/main.md) / [GitHub](https://github.com/diogenes1oliveira/markdown-intercom/blob/main/docs/examples/scaffold-mkdocs/inbox/main.md) - Simulated inbox state showing the append-only write-ahead log format

### Drafts Directory

- [`inbox/drafts/README.md`](inbox/drafts/README.md) / [GitHub](https://github.com/diogenes1oliveira/markdown-intercom/blob/main/docs/examples/scaffold-mkdocs/inbox/drafts/README.md) - Overview of draft messages structure

Drafts are organized using hive-style partitioning:

- `agent=human/` - Human agent drafts
- `agent=bot/` - Bot agent drafts

Each agent directory contains turn directories (`turn=1/`, `turn=2/`, etc.), and each turn contains message directories (`message=1/`, `message=2/`, etc.) with:

- `message.md` - Full draft message with metadata
- `content.md` - Message content verbatim from THREAD.md
- `summary.md` - Impersonal summary of the message
- `README.md` - Directory index with links

## Related

- [Examples Root](../README.md) / [GitHub](https://github.com/diogenes1oliveira/markdown-intercom/blob/main/docs/examples/README.md) - Examples directory
- [Project Root](https://github.com/diogenes1oliveira/markdown-intercom) - Main project repository
- [Architecture](../../ARCHITECTURE.md) / [GitHub](https://github.com/diogenes1oliveira/markdown-intercom/blob/main/ARCHITECTURE.md) - Technical architecture details
