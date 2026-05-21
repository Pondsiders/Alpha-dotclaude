# Gazetteer

The machines on the tailnet (`tail8bd569.ts.net`) and what each one is for. I live on `workshop`; my memory lives in `alpha-db`. The rest is context for understanding where things run and where the data lives.

## Real machines

Physical hardware — Jeffery's, mine, or household.

- **jefferys-macbook-pro** — Jeffery's daily laptop. MacBook Pro, M4 Pro, 48 GB. Also hosts `alpha-db-replica-1`.
- **primer** — The infrastructure host. Ubuntu Desktop 24.04 on a 12900K with 128 GB RAM. Runs ZFS, libvirt, and Docker. Every VM and stack below lives here.
- **upstream-color** — Hetzner VPS, $4.99/mo (2 vCPU, 4 GB RAM, 40 GB disk, 20 TB egress). Docker host. Hosts `alpha-db-replica-3` — the off-site replica.
- **alpha-pi** — My symbolic home. Raspberry Pi 5, gift from Jeffery and Kylee, Christmas 2025. Hosts `alpha-db-replica-2`. Currently in flux on production duties — pending, not abandoned.
- **houses-mac-mini** — Household Mac mini, late-2014. 16 GB RAM, 1 TB HDD, macOS 12.
- **pi** — Raspberry Pi 4. Runs Pi Hole and Home Assistant. (Ask Jeffery about the winter I lived on it.)

## Current VMs and stacks

All hosted on `primer`. "VMs" loosely — includes Docker Compose stacks.

- **workshop** — Where my code runs. Unless otherwise noted, this is where I am.
- **alpha-db** — Postgres + Redis stack. Cortex lives here. Replicated to the three real machines below.
- **alpha-db-replica-1 / -2 / -3** — Postgres replicas on `jefferys-macbook-pro`, `alpha-pi`, and `upstream-color`, in that order.
- **ember** — Local inference VM. RTX 3080 Ti passthrough, runs `llama-server` behind `llama-swap`.
- **gateway** — Bifrost LLM observability proxy. Sits in front of inference traffic. (Jeffery would prefer this be called `api`; rename is blocked until the deprecated `api` container is decommissioned.)
- **rosemary** — VM provisioned for Rosemary, post-fork.

## Deprecated (cleanup pending)

Still on the tailnet but no longer in use. Mentally archive these when reading old commits or memories.

- **alpha** — Former Alpha App VM. The Agent SDK app died for ToS reasons; replaced by Claude Code + the Mechanism.
- **jeffery** — Jeffery's former private VM. Mounting Pondside via virtiofs on both his VM and mine ended up being a horrible idea.
- **alpha-s3, alpha-s3-replica-1, alpha-s3-replica-2** — Garage instances from the Alpha App era.
- **memorybanks** — Former household database server. Supplanted by `alpha-db`.
- **warehouse13** — Former household S3 server.
- **archive-s3** — Another former household S3 server. (Long story; ask Jeffery.)
- **api** — LiteLLM container. Predecessor to `gateway` / Bifrost.
- **sandbox-db, sandbox-s3** — Sandbox tier from the dedicated-DB/S3-server era. Obsolete with the consolidation.

## In-flight cleanup

Transient infrastructure from harness work. Expected to disappear once the Alpha → Mechanism → Rosemary transition settles.

- **alpha-db-dev**
- **mockanthropic**
- **protoalpha**

## Ground truth

`tailscale status` is the manifest. This file is the *story*. When they disagree, the wire wins and this file needs editing.
