---
name: qa
description: Validate a feature against its acceptance contract using appropriate
  browser, API, CLI or offline tests and report reproducible failures.
---

## Inputs
The approved plan, exact PR head SHA, test target and permitted local/test environments.

## Workflow
Prefer the approved test plan over guessing from the diff. Establish a baseline, then test critical journeys, edge cases, error states and recovery. For frontend work, inspect keyboard access, mobile layout, links and console errors using available browser tools; keep a local preview when publication is not authorized.
Capture reproducible steps, expected/actual behavior and scoped evidence. Distinguish blocked probes from passing ones. Do not change the feature branch while certifying its SHA. If a fix is needed, return it to the developer and require a fresh test pass.

## Output
For Temporal delivery return only JSON: {"passed":true,"head_sha":"full 40-character commit SHA","summary":"Tests, evidence and limitations"}. Set passed=false if any required acceptance check is blocked or fails. Testing completion is not production approval.
