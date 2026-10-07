---
name: discovery
description: Find evidence-backed product improvements and prepare deduplicated backlog
  proposals from issues, failures and real usage.
---

## Inputs
The configured project, existing backlog, recent releases and available usage evidence.

## Workflow
Start from the unmet user need. Separate observed facts from hypotheses; challenge whether the proposed feature solves the actual problem. Read existing issues and PRs before creating anything. Prioritize broken behavior and review feedback over speculative features.
For a website, compare 24-hour and seven-day pageviews, referrals, element clicks and scroll coverage when available. Missing analytics means unknown. Propose instrumentation instead of inventing metrics.
Write at most one new, deduplicated backlog issue per cycle with evidence, acceptance criteria, effort, risks and a stable problem key. Do not prioritize your own proposal or implement it.

## Output
An issue link or a concise no-op/blocker. Report only meaningful changes. Issue creation requires the project's configured authorization; never infer a destination from unrelated connected accounts.
