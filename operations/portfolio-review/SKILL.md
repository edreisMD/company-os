---
name: portfolio-review
description: Review configured projects serially and select one next role handoff
  while respecting project pauses and shared work limits.
---

## Inputs
The private project registry, pause flags, previous checkpoints and current backlog/checks.

## Workflow
Inspect enabled projects serially. Prioritize incidents, broken checks and review feedback; avoid duplicate implementation PRs. Select at most one next implementation task across the portfolio, then name the role and evidence it needs.
Temporal owns run coordination. A manually invoked legacy cycle must use the shared lock helper in scripts/plan.py and release only its own token. Do not run both schedulers concurrently.

## Output
A private portfolio checkpoint with project, evidence, blocker and next role. This role triages only; it does not collapse planning, implementation, QA and release into one daily bot. Stay quiet when nothing actionable changed.
