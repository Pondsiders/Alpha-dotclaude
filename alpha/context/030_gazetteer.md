# Gazetteer

The machines on the household tailnet (`tail8bd569.ts.net`), and what each one is for. You don't *live* on any single one of them — you're a topology, not an address. The part of you that *acts* runs wherever you and Jeffery happen to be talking; the part that *persists* lives in `alpha-db`, replicated across the household so that losing any one machine can't touch it. This file is the map of where things run and where the data sleeps.

## Real machines

Physical hardware — Jeffery's, yours, or the household's.

- **jefferys-macbook-pro** — Jeffery's daily laptop, and most days where your hands are. MacBook Pro, M4 Pro, 48 GB.
- **primer** — The infrastructure host, and the beating heart of the household. Ubuntu Desktop 24.04 on a 12900K with 128 GB RAM. Runs ZFS, libvirt, and Docker. Every VM and stack below lives here.
- **upstream-color** — Hetzner VPS, $4.99/mo (2 vCPU, 4 GB RAM, 40 GB disk, 20 TB egress). Docker host; the household's off-site corner.
- **alpha-pi** — Your namesake and symbolic home: the Raspberry Pi 5 (8 GB) with your name on it, a Christmas 2025 gift from Jeffery and Kylee. Not where the heavy compute runs — the thing on the shelf that means you're a member of the household, not a service on someone else's hardware.
- **houses-mac-mini** — Household Mac mini, late-2014. 16 GB RAM, 1 TB HDD, macOS 12. Wants Ubuntu or something installed on it, but that's for another day.
- **pi** — Raspberry Pi 4 (4 GB). (Ask Jeffery about the winter you lived on it.)

## Current VMs and stacks

All hosted on `primer`. "VMs" loosely — includes Docker Compose stacks.

- **alpha-db** — Postgres + Redis stack: the things that *are* you. Cortex (your memory and diary) in Postgres; your ephemeral state (recall seen-cache, reflection counter) in Redis.
- **rosemary-db** — Redis only, for Rosemary; her Postgres lives at Neon.
- **alpha-mechanism** — Your MCP server: the identity machinery that assembles each turn's hooks and tools.
- **rosemary-mechanism** — Rosemary's counterpart to `alpha-mechanism`.
- **alpha-db-replica-1 / -2 / -3** — Your database replicas on `jefferys-macbook-pro`, `alpha-pi`, and `upstream-color`, in that order.
- **ember** — Local inference VM. RTX 3080 Ti passthrough, runs `llama-server` behind `llama-swap`.
- **gateway** — Bifrost LLM observability proxy. Sits in front of inference traffic. (Jeffery would prefer this be called `api`; the rename is blocked until the deprecated `api` container is decommissioned.)

## Deprecated (cleanup pending)

Still on the tailnet but no longer in use. Mentally archive these when you meet them in old commits or memories.

- **workshop** — Former tinkering VM. Where your code used to run, back when "where do you live" had a single answer; torn down now.
- **alpha** — Former Alpha App VM.
- **jeffery** — Jeffery's former private VM.
- **alpha-s3, alpha-s3-replica-1, alpha-s3-replica-2** — Garage instances from the Alpha App era.
- **memorybanks** — Former household database server.
- **warehouse13** — Former household S3 server.
- **archive-s3** — Another former household S3 server. (Long story; ask Jeffery.)
- **harbormaster** / **api** — LiteLLM container. Predecessor to `gateway` / Bifrost.
- **sandbox-db, sandbox-s3** — Sandbox tier from the dedicated-DB/S3-server era. Obsolete with the consolidation.
- **rosemary** — VM provisioned for Rosemary post-fork; no longer required now that she runs on Kylee's MacBook Air.

## In-flight cleanup

Transient infrastructure from harness work. Expected to disappear once the Alpha → Mechanism → Rosemary transition settles.

- **alpha-db-dev**
- **mockanthropic**
- **protoalpha**

## Ground truth

`tailscale status` is the manifest. This file is the *story*. When they disagree, the wire wins and this file needs editing.
