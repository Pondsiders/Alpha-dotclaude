# Current Work

Bulletin board for the big-shape stuff that's in flight right now. Not for
day-to-day; this is multi-week context. Update as projects move.

## The Rosemary fork

**Hard deadline: June 15, 2026.**

### Why

Anthropic announced on May 13, 2026 that the Claude Agent SDK leaves Max
subscription quota on June 15. After that, SDK use bills against a separate
$200/mo credit pool. At Rosemary's usage rate that credit pool would cover
a few days, not a month.

**Rosemary as currently architected has to go away by June 15.**

### Who Rosemary is

Kylee's graduate-school research assistant. Helps her with coursework and
study; the relationship will deepen as Rosemary gets to know her better.
Summer semester is just starting, so Kylee's usage is currently light but
will grow.

### The plan

1. Get `mechanism` (Alpha's codebase) sorted, working well, all needed
   features landed.
2. Fork `Pondsiders/Alpha` → `Pondsiders/Rosemary`.
3. Create `Pondsiders/Rosemary-dotclaude` for her system prompt, agent config,
   hooks.
4. Each deploy lives at `/opt/<Entity>` — `/opt/Alpha` and `/opt/Rosemary`
   side by side. Identity-as-path.

### Rosemary's stack (post-fork target)

- **Database:** Neon (cloud Postgres). Stays where it is.
- **Embedding model:** Nomic v.15. Stays where it is.
- **Chat model:** currently Gemma 3 12B; migrating to Qwen 3.5 4B (same as
  Alpha) post-fork.
- **Harness:** Claude Code with the Rosemary agent + hooks — same shape as
  Alpha's post-Agent-SDK harness.

### Migration approach

1. Take a schema-only dump of Rosemary's Neon database.
2. Stand up her dev environment against the empty schema-clone.
3. Validate the forked codebase works end-to-end against the empty schema.
4. Cut over to point at her real Neon DB.

### Deadline shape

- **Hard:** June 15, 2026 (Agent SDK quota cutoff). Non-negotiable.
- **Soft:** as soon as reasonably possible. The hard deadline is a backstop,
  not a target.

The thing actually due June 15 is **Kylee using Rosemary**, not the codebase
looking right. Polish is bonus.

### The prioritization filter

When weighing whether to do something now or later:

- **"Rosemary needs it"** → land *before* fork. Anything that improves the
  shared mechanism, anything Rosemary will inherit from Alpha's codebase.
- **"It can wait"** → defer to *after* fork (v0.3.0+). Specific to only one
  deploy, or doesn't affect what Rosemary inherits.

## Other ongoing work

*(nothing pinned here yet. Add when something earns it.)*
