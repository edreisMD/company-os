# ceo teams

ceo is a Pi-based portfolio coordinator. Orca runs its workers and exposes their sessions, tasks, messages and settlement. This catalog supplies pinned role instructions and workflow graphs. Installation accounts, project bindings, goals, decisions and reports stay private in the ceo installation.

Each nested role keeps its detailed gstack references and has `agent.yaml`, a runtime-neutral version 1 definition. Its execution fields mirror the existing `temporal.yaml` version 2 definition; `schedule_paused` mirrors `paused`. The validator rejects conflicts. Existing Temporal schedules remain paused during the ceo pilot. Role trigger metadata describes eligibility; ceo dispatches engineering roles through the team graph rather than enabling independent role timers.

`teams/frontend/team.yaml` and `teams/open-source/team.yaml` define the smallest delivery team:

1. Planner produces a hashed plan and names unresolved prerequisites.
2. Founder approves that exact plan through ceo.
3. Developer owns an isolated candidate worktree.
4. Independent reviewer and QA inspect that candidate revision.
5. Release role prepares a reviewable PR and readiness evidence.
6. Founder approves the exact revision for release.
7. Founder confirms publication through the chosen platform.
8. Release role verifies production against the approved revision.

Roles run on demand. ceo checks native messages every five seconds, worker state every minute and configured issue intake every five minutes without model calls. New evidence wakes its model. The default installation allows three workers globally, one implementation and one delivery workflow per project. These limits and approval rules are founder policy, outside this catalog.

## Organization experiments

The default organization procedure still produces proposals for human review. A private ceo installation may explicitly authorize automatic activation of subordinate role and team changes. That grant is private founder policy; a skill cannot grant it to itself.

In that mode, ceo records a specific bottleneck and expected improvement privately, validates an isolated catalog checkout against trusted governance and runtime invariants, and publishes reusable definitions to `ceo/active`. It activates an exact commit for future goals only. Running goals retain their pinned revision. One experiment per project per week is permitted; rollback restores the previous future-goal activation. Public patches must contain no project accounts, paths, credentials or operational reports.

Executive authority, governance, runtime code, credentials, permissions, release requirements and ceilings are excluded from this editable scope. New roles start paused and read-only; retirement requires pausing schedules and draining pinned workflows. Team repositories are data and never supply executable Pi extensions.

Run `python3 scripts/validate.py` and the repository tests before publishing a catalog change. The ceo runtime additionally checks mandatory approvals, independent evidence, graph ordering and candidate ownership when loading or activating a team.
