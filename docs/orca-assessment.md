# Orca as the CompanyOS runtime and console

Assessment date: 2026-10-07. Inspected a local clone of stablyai/orca at `726eaf117e8606956051b218b8710e0fcb0c9b27` (package version 1.4.214, MIT). This is a source/documentation review, not a running deployment or a completed reliability benchmark. Orca was not installed, started or given credentials.

## Recommendation

Yes: Orca is a strong starting point for the desired product—load a GitHub CompanyOS catalog, see the organization, run agents and inspect their work. Prototype a thin CompanyOS integration on its existing runtime and UI before building our own console or more session-management infrastructure. Keep the public nested-skill format independent of Orca and Temporal. Do not maintain two active schedulers for the same role.

Orca already supplies substantially more than a terminal UI: agent worktrees, Codex support, recurring automation management, remote execution, durable task/run state, supervised dispatches, dependency-aware tasks, inbox delivery/acknowledgment and decision gates. Its orchestration interface is explicitly experimental, so production migration remains contingent on an isolated pilot.

## Evidence and fit

| Need | Inspected evidence | Implication |
|---|---|---|
| Visible agent sessions, worktrees, native GitHub/Linear and mobile companion | [README](https://github.com/stablyai/orca/blob/726eaf117e8606956051b218b8710e0fcb0c9b27/README.md) | Reuse this product surface; add company/department navigation instead of building terminals and session viewers. |
| Recurring runs, disabled definitions, prechecks, session reuse and history | [Automation CLI](https://github.com/stablyai/orca/blob/726eaf117e8606956051b218b8710e0fcb0c9b27/docs/site/content/docs/cli/automations.mdx), [service](https://github.com/stablyai/orca/blob/726eaf117e8606956051b218b8710e0fcb0c9b27/src/main/automations/service.ts) | A plausible schedule target, but our cron/timezone/interval semantics need explicit translation and tests. Do not silently approximate unsupported triggers. |
| Multi-agent tasks, dependencies, supervised Codex workers, messaging and gates | [Orchestration CLI](https://github.com/stablyai/orca/blob/726eaf117e8606956051b218b8710e0fcb0c9b27/docs/site/content/docs/cli/orchestration.mdx) | Could replace much of the future communication layer. The interface is experimental; Run itself is a namespace, not a scheduler. |
| Unattended backend | [orcad operations](https://github.com/stablyai/orca/blob/726eaf117e8606956051b218b8710e0fcb0c9b27/docs/reference/orcad-operations.md) | Plain Node runtime exists. It owns RPC/git/worktrees/persistence, with a separately managed terminal daemon. Distinguish this from Electron-based orca serve. |
| Restart and uncertain-launch handling | [Headless dispatch durability tests](https://github.com/stablyai/orca/blob/726eaf117e8606956051b218b8710e0fcb0c9b27/src/main/automations/headless-dispatch-durability.test.ts), [retained-run reconciliation](https://github.com/stablyai/orca/blob/726eaf117e8606956051b218b8710e0fcb0c9b27/src/main/automations/retained-run-reconciliation.ts) | There is deliberate recovery engineering; tests were inspected, not executed here. This is not proof of Temporal-equivalent semantics or exactly-once external actions. |
| Approval enforcement | [Gate RPC](https://github.com/stablyai/orca/blob/726eaf117e8606956051b218b8710e0fcb0c9b27/src/main/runtime/rpc/methods/orchestration/gates/gates.ts), [gate store](https://github.com/stablyai/orca/blob/726eaf117e8606956051b218b8710e0fcb0c9b27/src/main/runtime/orchestration/db/decision-gates/decision-gate-store.ts) | Gates check run/caller scope and record a resolution. These inspected methods do not bind a founder identity and exact plan/commit hash; keep that validation in our trusted release adapter. |

## Missing CompanyOS layer

The inspected code has no CompanyOS temporal.yaml importer. Build a catalog integration with these responsibilities:

1. Accept a GitHub repository and an explicit revision. Fetch using existing account access, validate files without executing repository setup hooks, and record origin/commit/digest. Never treat a mutable branch name as the approved artifact.
2. Discover nested SKILL.md/temporal.yaml pairs and governance.yaml. Bind private workspaces, secrets and identity references separately. Show validation errors and required tooling before enabling any role.
3. Present the hierarchy: company → department → manager → roles, with cadence, enabled state, current task, last result, blockers, pending approvals and usage where actually known. Distinguish configured, queued, running, blocked and completed. Do not call the organization ready until its bindings and workers are ready.
4. Translate cron/manual/event definitions into the selected execution adapter. Store stable mappings from company/role/revision/event ID to Orca automation/run/task/dispatch IDs. Reconcile partial writes; keep removed roles' history and pause their schedules.
5. Load the selected gstack-backed role and its required phase references in an isolated worktree. Pin the catalog digest and return structured outcome/evidence. Connect task completion to the next stage only after checking the required artifact and approvals.
6. Show role-evolution PRs as proposed org changes. A manager edits only its scope; an approved exact revision becomes the next catalog snapshot. Do not hot-load unreviewed agent edits.

Start with native Orca views and a small CompanyOS adapter. Add a dedicated org-chart view through the appropriate extension surface if it supports the necessary UI; otherwise maintain a narrow UI fork. Extension suitability has not yet been verified. Avoid copying Orca's whole runtime into CoOS-backend.

## Temporal decision

Do not expand the custom Temporal implementation while testing this fit. Keep its paused configuration and journal available as the current baseline.

Pilot Orca's own automation/runtime for one disabled-by-default engineering review role, then a small planning → review → approval → implementation → QA flow. If restart, identity, duplicate-event and visibility tests pass, make Orca the execution/schedule backend for that company and retire the duplicate Temporal schedules. If its workflow guarantees fall short, use Temporal as the single durable coordinator and Orca as the session/UI adapter, with Orca's competing timers disabled. The hybrid is an option to justify through evidence, not the default architecture.

## Pilot acceptance criteria

- Import the same catalog twice without duplicate roles/schedules; unknown manifests fail closed.
- Run fake/no-model workers first. Verify outputs and task IDs rather than terminal inactivity alone.
- Restart the runtime before launch, after launch but before persistence, during an approval wait and after completion. No duplicate implementation or lost pending decision.
- Redeliver a source event; preserve one logical run. Changed catalog revisions invalidate stale work and approvals.
- Reject a worker resolving its own release gate; verify the native human identity and exact artifact independently of the generic gate resolution string.
- Pause/delete a role while work is in flight; prevent new dispatches and retain logs without killing unrelated sessions.
- Check timezone/DST, missed runs, overlap and resource limits against our manifest contract.
- Trace an org-chart role to its worktree, model session, evidence, PR and approval; unknown usage remains unknown.
- Show a manager's proposed role change before adoption, verify scope from a trusted base, and apply only the reviewed revision.

No platform migration or live activation was performed as part of this assessment.
