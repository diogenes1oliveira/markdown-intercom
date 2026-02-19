# Roadmap

## Moonshot Goal 🚀

**Deploy to GitHub Pages an MkDocs website** with:

- **Nice navigation** - Clean, intuitive site structure
- **Queryable by multiple dimensions:**
  - **Date** - Filter conversations by when they happened
  - **Hierarchical tags** - Multi-level categorization system
  - **Role** - Filter by participant (human, ChatGPT, Cursor Agent, etc.)
  - **Hour** - Time-based filtering
  - **Subjects** - Topic-based organization
  - **Prompt engineering lessons** - Curated learnings and insights

**Technical approach:**
- MkDocs for static site generation
- GitHub Pages for hosting
- Custom plugins/themes for query interface
- Markdown parsing and metadata extraction

## Plutoshot Goal 🌌

**DuckDB WASM embedded interface** in HTML (like Hugging Face's model explorer):

### Core Architecture

- **Single static page** - Everything in one HTML file
- **Service Worker** - Emulate Cloudflare Workers functionality
- **Worker.js** - Background processing
- **DuckDB WASM** - In-browser SQL database for querying conversations
- **ts-rest** - Type-safe REST client (can be used as-is)

### Use Cases

1. **Conversation exploration** - Interactive querying of THREADS.md data
   - SQL queries over conversation history
   - Real-time filtering and aggregation
   - Visualizations of prompt engineering patterns

2. **Whisper transcriptions** - User-submitted audio transcriptions
   - **GitHub Actions builder** - Automated transcription pipeline
   - **Phone integration** - Easy transcription file submission from mobile devices
   - Store transcriptions alongside conversations

3. **Pre-TLS latency world** - Return to end-to-end encryption without TLS overhead
   - Explore low-latency communication patterns
   - Document lessons for modern distributed systems
   - Research into TCP-level encryption strategies

### Technical Stack (Plutoshot)

- **Frontend:** HTML + Service Worker + DuckDB WASM
- **Backend:** Static files + Service Worker (no server needed)
- **API:** ts-rest for type-safe client/server communication
- **Storage:** IndexedDB via DuckDB WASM
- **Deployment:** Single static HTML file (can be hosted anywhere)

## Implementation Phases

### Phase 1: Foundation ✅
- [x] Basic README.md
- [x] THREADS.md structure
- [x] Session organization
- [x] Emoji feedback buttons

### Phase 2: Documentation (Current)
- [ ] Complete DEVELOPMENT.md
- [ ] Complete ROADMAP.md
- [ ] Expand THREADS.md with more sessions
- [ ] Add more detailed SLIPUPs

### Phase 3: MkDocs Setup
- [ ] Initialize MkDocs project
- [ ] Configure GitHub Pages deployment
- [ ] Design navigation structure
- [ ] Create custom theme/plugins for querying

### Phase 4: Query Interface
- [ ] Parse THREADS.md into structured data
- [ ] Extract metadata (date, role, tags, subjects)
- [ ] Build query UI components
- [ ] Implement filtering and search

### Phase 5: DuckDB Integration (Plutoshot)
- [ ] Embed DuckDB WASM
- [ ] Set up Service Worker
- [ ] Create single-page HTML interface
- [ ] Implement SQL query interface
- [ ] Add visualization components

### Phase 6: Advanced Features (Plutoshot)
- [ ] Whisper transcription integration
- [ ] GitHub Actions builder
- [ ] Mobile submission interface
- [ ] Research documentation on pre-TLS encryption

## Tags & Classification System

Based on the gist structure, conversations will be classified by:

- **Session** - Numbered sessions (#1, #2, #3...)
- **Turn** - Numbered turns within sessions
- **Timestamp** - ISO 8601 format timestamps
- **Role** - `human`, `ChatGPT`, `Cursor Agent`, `GUI Agent`, etc.
- **Subject** - Topics discussed (README creation, protocol design, etc.)
- **Tags** - Hierarchical tags (e.g., `protocol/communication`, `ui/feedback`, `deployment/github-pages`)

## Success Metrics

- **Moonshot:** Fully queryable MkDocs site deployed to GitHub Pages
- **Plutoshot:** Working DuckDB WASM interface with Service Worker
- **Documentation:** Complete prompt engineering lessons report
- **Adoption:** Other projects using similar markdown-based communication patterns
