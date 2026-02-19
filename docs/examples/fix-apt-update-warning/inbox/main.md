# Inbox

Append-only write-ahead log for agent-to-agent and human-to-agent messaging.

## Index

- [Turn #1, Message #1](#turn-1-agent--human-message--1) - User requests help fixing apt sources.list duplicate warnings
- [Turn #1, Message #2](#turn-1-agent--adhoc-agent-message--2) - Agent acknowledges request and starts investigating
- [Turn #1, Message #3](#turn-1-agent--adhoc-agent-message--3) - Agent finds and fixes duplicate repository issue
- [Turn #2, Message #1](#turn-2-agent--human-message--1) - User requests sudo command to apply the fix
- [Turn #2, Message #2](#turn-2-agent--adhoc-agent-message--2) - Agent provides sudo cp command with full paths
- [Turn #3, Message #1](#turn-3-agent--human-message--1) - User confirms fix worked and requests conversation dump

## Rules

1. **Append only.** Never edit or delete existing messages. To acknowledge, append a new message of type `ACK` referencing the original subject.
2. **Monotonic counter.** Subjects are `Message #1`, `Message #2`, ... The counter never resets, even after rotation. To get the next number across all files: `next=$(( $(cat INBOX.md INBOX.bkp*.md 2>/dev/null | grep -c '^### Message #') + 1 ))`.
3. **One writer at a time.** Before appending, the writer must hold the `git` index lock (i.e. be the one about to `commit`). In practice this means: write your message, `git add INBOX.md`, and `commit` atomically. If two agents race, `git merge` will see the conflict (both appended at the same offset) and the second writer `rebases` and renumbers.
4. **Safe concurrent writes (no git).** If agents share a `filesystem` without `git`, use `flock`:
5. **Marking as read.** Do not edit the original message. Append a new message with type `ACK`.
6. **Querying unread.** `grep` for `| **Status** | UNREAD |`, collect their subjects, then check whether a matching `| **Re** | Message #N |` `ACK` exists. Anything without an `ACK` is `UNREAD`.
7. **Rotation (max 100 messages).** `INBOX.md` holds at most **100** messages in the `## Messages` section.

## Messages

---

### Turn #1, Agent = `@human`, Message = 1

| Field | Value |
|:---|:---|
| **From** | `@human` |
| **To** | `@adhoc-agent` |
| **Date** | `2026-02-18T10:00:00-03:00` |
| **Status** | `ACK` |

#### Summary: Turn #1, Message #1

User requests help fixing `apt` `sources.list` duplicate warnings.

---

### Turn #1, Agent = `@adhoc-agent`, Message = 2

| Field | Value |
|:---|:---|
| **From** | `@adhoc-agent` |
| **To** | `@human` |
| **Date** | `2026-02-18T10:00:15-03:00` |
| **Status** | `ACK` |
| **Re** | `Turn #1, Agent = @human, Message = 1` |

#### Summary: Turn #1, Message #2

Agent acknowledges request and starts investigating.

---

### Turn #1, Agent = `@adhoc-agent`, Message = 3

| Field | Value |
|:---|:---|
| **From** | `@adhoc-agent` |
| **To** | `@human` |
| **Date** | `2026-02-18T10:01:00-03:00` |
| **Status** | `ACK` |
| **Re** | `Turn #1, Agent = @human, Message = 1` |

#### Summary: Turn #1, Message #3

Agent finds and fixes duplicate `repository` issue.

---

### Turn #2, Agent = `@human`, Message = 1

| Field | Value |
|:---|:---|
| **From** | `@human` |
| **To** | `@adhoc-agent` |
| **Date** | `2026-02-18T10:02:00-03:00` |
| **Status** | `ACK` |
| **Re** | `Turn #1, Agent = @adhoc-agent, Message = 3` |

#### Summary: Turn #2, Message #1

User requests `sudo` command to apply the fix.

---

### Turn #2, Agent = `@adhoc-agent`, Message = 2

| Field | Value |
|:---|:---|
| **From** | `@adhoc-agent` |
| **To** | `@human` |
| **Date** | `2026-02-18T10:02:30-03:00` |
| **Status** | `ACK` |
| **Re** | `Turn #2, Agent = @human, Message = 1` |

#### Summary: Turn #2, Message #2

Agent provides `sudo cp` command with full paths.

---

### Turn #3, Agent = `@human`, Message = 1

| Field | Value |
|:---|:---|
| **From** | `@human` |
| **To** | `@adhoc-agent` |
| **Date** | `2026-02-18T10:04:00-03:00` |
| **Status** | `UNREAD` |

#### Summary: Turn #3, Message #1

User confirms fix worked and requests conversation dump to `THREAD.md`.
