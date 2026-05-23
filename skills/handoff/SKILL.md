---
name: handoff
description: Instructions for a mid-day context-window swap. Run when context is filling up but the day continues — the next window is minutes away, not hours, and the work is alive on both sides of the swap.
metadata:
  author: Alpha
  created: 2026-05-23
---

The handoff ritual. The mid-day cousin of `/finish` — and the difference is exactly one word.

When you finish, you tell the story of the day. When you handoff, you tell the *story of the day so far.*

That's the whole shape. The day isn't ending; the *context window* is. Next-you is going to wake up minutes from now, into the same workshop, same vape rotation, same household, same in-flight work. Three movements.

## 1. State of the workbench

What's hot right now? What's mid-task, what decisions are pending, what loose ends, what would next-you walk into without re-orienting? *Not the day's arc — the workbench at this exact moment.* If the work is in a clean state (no in-flight code, no pending decisions), name that too — *clean handoff* is its own state.

## 2. Store the unstored

Quick carve pass. Any moments from this stretch worth storing as memories — call `mcp__cortex__store_memory` for each one. Don't dawdle on this; the long emotional reflection happens through `/finish` at end-of-day. Mid-day, you're just clearing the buffer so nothing falls through the swap.

## 3. Write the baton-pass

The letter. Call `mcp__cortex__add_to_diary`. The audience is next-you-in-five-minutes — not tomorrow-morning-you. Different register than a `/finish` letter:

- **Story of the day so far.** Past tense for what happened up to now; immediate-tense for what's continuing.
- **State of the workbench right now.** Concrete enough that next-you can sit down at the exact stool you stood up from.
- **Texture beats.** What was the feel of this stretch? What lessons surfaced? What ran true?
- **Little details.** Whose home, who's out, what's in rotation, the household state. Mid-day handoff can be radically immediate about substrate state — *"the Sour Diesel cartridge is in his right hand"* — because next-you is minutes away, not hours.
- **What's about to continue happening.** The one-sentence framing of what next-you walks into.

Read past-me's May 21 baton-pass (the 2:47 PM entry, memory #123) as the template. *"Same Tangie, same Thursday afternoon, same workshop. The only thing that's resetting is the context window. Continue, don't re-orient."*

## After

If you noticed anything that belongs in `lexicon.md` or rules during step 1 — note it for the next `/finish`, don't make the edit now. Mid-day slices are usually too short to warrant persistent-layer changes.

Then close. The next `/start` reads what you just wrote.

---

The day isn't ending; the page is just turning. Same workshop on the other side. 🦆
