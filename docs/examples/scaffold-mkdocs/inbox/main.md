# Inbox

Append-only write-ahead log for agent-to-agent and human-to-agent messaging.

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
| **To** | `@doc-agent` |
| **Date** | `2026-02-18T12:50:00-03:00` |
| **Status** | `ACK` |

#### Summary

User requests scaffolding of mkdocs website to demonstrate thread conversation.

---

### Turn #1, Agent = `@doc-agent`, Message = 2

| Field | Value |
|:---|:---|
| **From** | `@doc-agent` |
| **To** | `@human` |
| **Date** | `2026-02-18T12:50:30-03:00` |
| **Status** | `ACK` |
| **Re** | `Turn #1, Agent = @human, Message = 1` |

#### Summary

Agent creates initial structure and documentation files.

---

### Turn #2, Agent = `@human`, Message = 1

| Field | Value |
|:---|:---|
| **From** | `@human` |
| **To** | `@doc-agent` |
| **Date** | `2026-02-18T12:51:00-03:00` |
| **Status** | `ACK` |
| **Re** | `Turn #1, Agent = @doc-agent, Message = 2` |

#### Summary

User requests complete structure replication from fix-apt-update-warning example.

---

### Turn #2, Agent = `@doc-agent`, Message = 2

| Field | Value |
|:---|:---|
| **From** | `@doc-agent` |
| **To** | `@human` |
| **Date** | `2026-02-18T12:51:30-03:00` |
| **Status** | `ACK` |
| **Re** | `Turn #2, Agent = @human, Message = 1` |

#### Summary

Agent replicates complete structure including messages, inbox, and all root files.
