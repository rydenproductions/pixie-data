---
kind: project
status: In progress
created: 2026-11-03
updated: 2026-11-22
---
# Pixie build
**Goal:** Build my own Agent OS dashboard, step by step  
**Status:** In progress
## Plan
- [x] Step 1: Purpose (BRIEF.md)
- [x] Step 2: Stack
- [x] Step 3: Layout
- [x] Step 4: Look
- [x] Step 5: Models
- [x] Step 6: Tools
- [x] Step 7: Memory
- [ ] Step 8 (paste from prompt pack)
- [ ] Add get_settings and propose_set_model tools to Pixie: allow-listed targets (Claude Code settings.json, Hermes config.yaml, dashboard chat model) and model names, Yes/Cancel confirm card showing old and new values, backup before edit, change log, restart only the affected service.
- [ ] Run `python3 -m unittest discover -s memory` to confirm the tests pass, then commit Step 7
- [ ] Restore or re-add BRIEF.md and the Step 2-6 files to this folder so later steps can build on them
- [ ] Connect the memory tools (search/save/delete/log) to the Step 6 tools and approval flow, and build the Memory panel
- [ ] Add get_settings and propose_set_model tools to Pixie: allow-list of targets and model names in a config file (Claude Code ~/.claude/settings.json, Hermes ~/.hermes/config.yaml, dashboard chat model), Yes/Cancel confirm card showing old and new value, backup before edit, change log, restart only the affected service.
## Revisions
- 2026-11-19: Claude Code (needs you): Step 8 (paste from prompt pack) — Fable requires usage credits. Switch to another model, or manage usage credits at https://claude.ai/settings/usage?from=cc_cli_limit_message, to continue.
- 2026-11-19: Claude Code: Step 7: Memory — I wrote the Memory design (docs/07-memory.md) and a working SQLite memory store with 7 tests (memory/store.py, memory/test_store.py). I couldn't run the tests or commit because Python and git commands needed approval, so the code is checked by reading only. The folder had no files from Steps 1-6, so I used plain Python and SQLite and said in the doc it can be ported.
- 2026-11-03: Project started
## Notes and decisions
- Dark + hot pink theme, Next.js, SQLite, Claude model router
- Approved: Step 7: Memory
- Voice is working.
- Phone approval works.
- Telegram approval works.
- Approved: Step 7: Memory

_This note is a copy written by Pixie. Edit the project in Pixie's Projects tab._
