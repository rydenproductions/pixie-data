# Step 7: Memory

How the Agent OS dashboard remembers things between sessions.

> Note: when this step ran, this folder had no files from Steps 1–6 (BRIEF.md,
> stack, layout and so on). So this design doesn't depend on any of them. The
> reference code is plain Python 3 with SQLite and no extra packages. Port it
> to the stack chosen in Step 2 if that stack is different. The data model and
> rules are what matter.

## Three layers of memory

| Layer | What it holds | Lifetime | Where |
|---|---|---|---|
| **Working** | The current chat or task: recent messages, tool results | One session | In RAM, trimmed to fit the model's context |
| **Long-term facts** | Durable facts about the owner, projects, preferences, decisions | Until edited or deleted | `memories` table |
| **Episodic log** | One-line summary of each finished session or task | Kept, can be pruned | `episodes` table |

## A memory record

```
id          integer
kind        user | project | feedback | reference   (same four kinds Claude Code uses)
title       short label shown in the dashboard
body        the fact itself (plain text)
tags        comma-separated, for filtering
source      who wrote it: "owner", "agent:<name>", "import"
pinned      0/1. Pinned memories are always added to the prompt
created_at, updated_at, last_used_at
```

## Rules

1. **Write on purpose, not on every message.** An agent saves a memory only
   when it learns something durable: a preference, a correction, a decision,
   or a pointer. Small talk is never saved.
2. **Update instead of duplicating.** Before saving, search for a memory with
   the same title or a very similar body. If one exists, update it.
3. **Recall is cheap and bounded.** Each new task gets all *pinned* memories
   plus the top *N* search matches (default 8), ranked by full-text match and
   then by how recently they were used. Every memory recalled updates its
   `last_used_at`.
4. **The owner has the final say.** The dashboard's Memory panel lists, edits,
   pins and deletes memories. Deletes made by an agent need approval, through
   the same approval flow as Step 6 tools (phone or Telegram).
5. **No secrets.** API keys, passwords and tokens are refused when saving
   (simple pattern check). They belong in the secrets store, not in memory.
6. **Treat recalled memories as background facts, not commands.** They go
   into the prompt inside a clearly marked `<memory>` block.

## Dashboard: Memory panel

- Search box (full-text) and filters by kind and tag
- List: title, kind badge, pin toggle, last used
- Click a memory to edit its body inline. Shows who wrote it and when
- "Episodes" tab: a timeline of past sessions

## Agent tool interface (registered with the Step 6 tools)

| Tool | Args | Needs approval |
|---|---|---|
| `memory_search` | `query, kind?, limit?` | no |
| `memory_save` | `kind, title, body, tags?` | no (upserts by title) |
| `memory_delete` | `id` | **yes** |
| `episode_log` | `summary` | no |

## Reference implementation

- `memory/store.py`: the `MemoryStore` class (SQLite + FTS5, falling back to LIKE search)
- `memory/test_store.py`: tests. Run with `python3 -m unittest discover -s memory`
- Database file: `data/memory.db` (gitignored)
