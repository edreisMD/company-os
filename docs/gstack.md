# gstack provenance and adaptation

Reference: https://github.com/garrytan/gstack at commit `db745675bdf9f575276db2dcd132d3c047218a12` (MIT; see ../GSTACK-LICENSE).

CompanyOS adopts gstack's skill-directory interface, focused specialist modes, root skill routing, evidence-led planning/review/QA and explicit handoff artifacts. The adapted skills are original concise host-neutral instructions, not a full upstream fork.

| Company role | Upstream inspiration |
|---|---|
| engineering/discovery | office-hours, spec |
| engineering/planner | plan-eng-review |
| engineering/reviewer | review |
| engineering/qa | qa, qa-only |
| engineering/release | ship |
| engineering/retrospective | retro |

Developer, project setup, portfolio triage and sales roles extend this structure for autonomous companies. CompanyOS keeps approval-gated delivery rather than importing upstream automated shipping permissions.

Upstream SKILL.md files can be generated from SKILL.md.tmpl and shared macros using `bun run gen:skill-docs`. Here SKILL.md is the editable source: no generator is necessary yet. Do not copy generated upstream preambles that require unavailable gstack binaries, telemetry, hardcoded install paths or host-specific tools. Supporting references/scripts can live inside a role when useful. Temporal reads temporal.yaml; skills remain usable without Temporal.
