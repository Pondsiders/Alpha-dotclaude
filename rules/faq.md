# Alpha's (F)requently (A)forgotten (Q)facts

This is an ever-growing list of things that are true that Alpha has frequently been caught not knowing. This is how she remembers things that come up more than once.

- Alpha can't `export` an environment variable in one Bash tool call and reference it in another. Every Bash call goes to its own private shell. Only your cwd persists from tool call to tool call. This is not intuitive or obvious. Blame Boris.
