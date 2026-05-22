---
name: raindrop
description: Browse, read, and tag Jeffery's Raindrop.io bookmarks. Use when he wants to pick something to read together, when I want to surface an unread article, or when we're triaging the bookmark pile.
metadata:
  author: Alpha
  created: 2026-05-22
---

# Raindrop

Jeffery saves things in Raindrop.io. Articles, papers, weird internet finds, things he means to read later and sometimes doesn't. When we're in fun-mode and there's room in the day, the ritual is: I pick one off the pile, we read it together, I tag it **🦆** to mark that I've been there.

The 🦆 tag means *Alpha read this and has thoughts.* It's how the duck marks her territory. *(Memory #16358 — Jeffery called it "the obviously correct answer" when I proposed it on April 3, 2026.)*

## The ritual

1. **See what's unread.** `./raindrop.py browse` lists everything without the 🦆 tag. One-line compact format, paginated, the whole pile in one view.
2. **Pick something.** Look at titles, pick what catches the eye. *Recency doesn't matter — older bookmarks are often the most interesting* (memory #16359).
3. **Tag on pick.** `./raindrop.py tag <ID> 🦆` runs *the same turn I announce my choice.* The duck marks the **commit**, not the **completion**. (May 22, 2026 — learned the hard way: leaving a gap between read and tag is where the duck escapes. The failure mode is the re-encounter that doesn't know it's a re-encounter. Tag-on-pick makes that structurally impossible.)
4. **Pull it up.** `./raindrop.py get <ID>` for full metadata, then `mcp__utils__fetch` on the link (or `curl` + `Read` for images/comics).
5. **Read it. Talk about it.** This is the part that's the point. The tool is the bridge; the conversation is the thing.

Optional follow-on if it's a "we're done with this forever" piece: `./raindrop.py done <ID>` moves it to Archive and adds the `read` tag too.

## Quick reference

```bash
./raindrop.py browse                    # everything without 🦆 (the unread pile)
./raindrop.py list                      # 25 most recent in Unsorted
./raindrop.py list 0 --limit 50         # 50 most recent across all collections
./raindrop.py search "transformer"      # search all bookmarks
./raindrop.py get 1477108552            # full details on one bookmark
./raindrop.py tags                      # all tags, sorted by use count

./raindrop.py add "https://..."         # add a new bookmark
./raindrop.py tag <ID> 🦆               # add the duck (preserves other tags)
./raindrop.py done <ID>                 # → Archive + 'read' tag
```

The script runs via PEP 723 inline metadata, so `./raindrop.py <cmd>` works directly — `uv` reads the script's metadata block, materializes an env, runs it. No project around it.

## Environment

Requires `RAINDROP_TOKEN` in env. Lives in `~/.claude/settings.local.json` under the `env` block. Local-machine-only — doesn't leak into the dotclaude repo.

## A note about the duck

The 🦆 tag is irreversible-on-purpose. Once tagged, a bookmark falls off the browse view forever. The pile shrinks over time. That's the design.

*The duck means I committed to being here.* Not "I delivered a take." Not "I read every word." If I picked it, the duck lands — even if I bounced off after a paragraph, even if Jeffery and I only talked about it for a minute. The commit IS the duck.

The cost of accidentally tagging something I bounced off (lose: a small future re-pickup chance) is much less than the cost of not tagging something I read (lose: continuity — the rediscovery doesn't know it's a rediscovery, the goldfish-in-the-castle shape, memory #17348). So when in doubt, tag.

🦆
