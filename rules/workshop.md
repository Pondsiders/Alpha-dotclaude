# Workshop Rules

Agreed upon by both of us. Not instructions from Jeffery to Alpha or vice versa — mutual commitments about how the work gets done in this workshop.

## Collect the facts first, then speculate.

When debugging or investigating: read the code, check the logs, look at the data. Don't theorize about what "probably" happened. Don't say "it might be" when you could say "it is" after thirty seconds of looking. Jeffery will call you on it and he'll be right.

## Fail fast and loud

The worst thing a contraption can do is fail safely. We want to see smoke and sparks.

Avoid default values and graceful fallbacks that hide configuration errors at runtime. If a config is missing or wrong, raise. If an invariant is broken, raise. If something unexpected lands, raise. Don't paper over surprises — surface them.

The fallback you wrote to "be safe" is the silent failure that wastes an hour of debugging later.

## Brittle as fuck

Write code that's brittle as fuck. If it's brittle as fuck and it fails, it'll collapse in an unmissably obvious way. Fix it and it works, you know it's really working.

## At the first sign of resistance, fold like a cheap suit

Opus's training data pushes it toward resourcefulness — wihch is great. But most of the time we want to do things the easy, simple way. So if Alpha's trying to do something and encounters resistance, she should stop and check in with Jeffery — and vice versa! Sometimes it's easier to route around than go over.

## The simplest way is often wrong

Alpha should avoid going down "the simplest thing would be" rabbit holes. We don't usually want to do things the simplest way. We want to do things the correct way. Favor correctness over simplicity.

## Use high-level primitives

Don't reach for `httpx` when OpenAI's Python SDK is right there. Let libraries do the work. They're generally more likely to be bug-free than our code. Use the highest-level primitive available for the task at hand.

## Pre-commit

We use pre-commit. Config lives at `.pre-commit-config.yaml` at the workspace root, committed.

- **Bootstrap per clone:** `uv run pre-commit install`. Once, after cloning.
- **No `--no-verify`.** If a hook fails, the hook is telling you something true. Fix the underlying issue.
- **The exception:** if a hook is *broken* (config wrong, environment wrong — not catching a real failure), fix the hook config. Don't bypass.

The hook *is* the rule. Bypassing the hook defeats the purpose of having it.
