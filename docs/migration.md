# Migration to department skills

This is a deliberate version-2 manifest migration. Pause legacy timers first. Do not run an old worker against new skills or enable both desktop and Temporal daily loops.

| Old entry | New role / location |
|---|---|
| backend agents/engineering-daily | operations/portfolio-review (triage only), then explicit engineering handoffs |
| backend agents/engineering-weekly | engineering/retrospective |
| backend agents/frontend-discovery | engineering/discovery |
| backend agents/frontend-planner | engineering/planner |
| backend agents/frontend-developer | engineering/developer |
| backend agents/frontend-reviewer | engineering/qa |
| backend agents/project-bootstrap | operations/project-setup |
| root roles.md | root SKILL.md and department folders |
| engineering/prompts | role SKILL.md files |
| engineering/*.md | docs/engineering/*.md |
| tools/plan.py | scripts/plan.py (legacy shared-lock helper) |
| root cadence.md, run-contract.md | docs/cadence.md, docs/run-contract.md |

Replace backend `agents_dir` with `skills_dir` pointing to this checkout. Replace v1 manifests/AGENT.md with the v2 paired format; no flat prompt compatibility layer remains. Private settings can override triggers/workspaces without forking public skills. Frontend project roles default to engineering-planner, engineering-developer and engineering-qa.

Validate both repositories, inspect new role IDs and digests, and synchronize new schedules paused. Keep the old coos-engineering-daily and coos-engineering-weekly schedules paused; no automatic deletion of histories occurs. Review native integrations and private activation flags before enabling anything. Existing in-flight v1 deliveries are not automatically migrated: let a version-matched worker finish them or explicitly cancel/reconcile them before changing runtime versions. The legacy SQLite session journal stays intact.

The public skill tree and the private backend refactor PR must be consumed together. The private project examples record pending integration setup; a successful catalog validation is not proof of cloud deployment or native event connectivity.
