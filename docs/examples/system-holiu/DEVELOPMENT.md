# Development Notes

## What We've Learned So Far

### Communication Protocol Evolution

This project started as an experiment in prompt engineering for README creation, but evolved into documenting a **markdown-based communication protocol** for AI agents and humans.

**Key Learnings:**

1. **File-based communication channels** - Using markdown files (chat.md, THREADS.md) as the primary interface for agent-to-human and agent-to-agent communication
2. **WAL-style documentation** - Write-Ahead Log approach: append-only, never modify existing content
3. **Session boundaries** - Each distinct conversation context (different agents, tools, time periods) should be its own Session #N
4. **Turn-based structure** - Clear turn numbering and timestamps make conversations reproducible and queryable
5. **Git as persistence layer** - Each turn can be a commit, creating a natural audit trail

### Project Structure

- **THREADS.md** - Main conversation log (WAL-style, append-only)
- **README.md** - Project overview and entry point
- **SLIPUPs.md** - Mistakes and learnings documentation
- **reports/** - Session-specific reports and suggestions
- **DEVELOPMENT.md** - This file (development notes and learnings)
- **ROADMAP.md** - Future plans and goals

### Prompt Engineering Insights

1. **Emoji feedback buttons** - Simple, interactive way to collect initial user feedback without complex infrastructure
2. **Early stage warnings** - Clear communication about project status (no DNS yet, work in progress)
3. **Documentation-first approach** - Building documentation alongside the project helps clarify goals and track progress
4. **Iterative refinement** - Protocol evolved through multiple sessions, learning from mistakes (SLIPUPs)

### Technical Patterns

- **Markdown as interface** - Simple, human-readable, git-friendly
- **Git commits as turns** - Natural versioning and history
- **Session isolation** - Each conversation session is self-contained
- **Retroactive documentation** - Updating protocol docs while maintaining historical accuracy

### Challenges Encountered

1. **Session boundary confusion** - Initially mixed sessions; learned to recognize distinct conversation contexts
2. **Protocol evolution** - Balancing retroactive updates with historical accuracy
3. **File naming** - Started with THREAD.md, evolved to THREADS.md for clarity
4. **Feedback collection** - Exploring different strategies (GitHub Issues, emoji buttons, etc.)

### Current State

- ✅ Basic README.md with emoji feedback buttons
- ✅ THREADS.md documenting prompt engineering sessions
- ✅ Session-based organization (ChatGPT, Cursor Agent)
- ✅ WAL-style append-only documentation
- ✅ Reports directory for session-specific outputs

### Next Steps

See [ROADMAP.md](ROADMAP.md) for detailed future plans.
