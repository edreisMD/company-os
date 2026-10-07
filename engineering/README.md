# Engineering operating system

One daily operator, three modes: triage, implementation, review. A weekly review adjusts priorities. Deterministic CI runs for every pull request. Human approval precedes merging and production release.

## Delivery loop

1. Observe: inspect open issues, PRs, failing checks and available production evidence.
2. Triage: deduplicate before creating an issue. Record problem, evidence, acceptance criteria and priority. P0 outages/security first; P1 broken core behavior; P2 useful improvements; P3 exploratory ideas. Never manufacture activity.
3. Select: finish or unblock the existing implementation PR before starting another. Maximum one active implementation PR per project, one new issue per project per daily run, and one implementation task across the portfolio per run.
4. Build: use an isolated checkout/branch from the real default branch. Never edit a user's dirty checkout. Implement the smallest useful change; include regression evidence and documentation.
5. Review: compare the final diff against acceptance criteria; run relevant tests; inspect dependencies, permission changes and private data. Self-review is not an independent human approval.
6. Propose: open a draft PR with exact test results, screenshots when relevant, risks, rollback and commit SHA. Request the founder's decision. Never approve your own PR, manufacture an approval or merge automatically.
7. Release: after explicit approval of the current revision, a human merges. CI/CD builds that merged revision, deploys the resulting immutable artifact, checks the live result and records the previous artifact for rollback. Changed code invalidates previous approval.

The initial scheduled agent stops at step 6. Deployment commands run only in a separately authorized release operation. This restriction also applies to direct pushes, Sites publishing and production branches named something other than main.

## Files

- [Daily prompt](prompts/daily.md), [weekly prompt](prompts/weekly.md)
- [Project profiles](profiles.md): website, open source, private service and framework
- [CI/CD](ci-cd.md): trust boundaries, branch approval and release contracts
- [Analytics](analytics.md): evidence and click/scroll reporting
- [Registry example](../templates/project-registry.example.json)
- [Planner](../tools/plan.py): validates the private registry and prints a bounded run plan

Runtime: a scheduled agent runs the prompts; GitHub Actions runs deterministic checks. No model key is needed for these CI checks. Local scheduled work requires an available machine and app; it is not an always-on cloud worker. A different runtime can reuse these prompts and registry.

## Local operation

Run `python tools/plan.py plan /path/to/private/projects.json --cadence daily` (or `weekly`). Claim the shared lock with `python tools/plan.py claim /path/to/private/state/lock.json`; save the returned token. Release with `python tools/plan.py release /path/to/private/state/lock.json TOKEN`. A pre-existing lock fails closed even after 60 minutes. Before removing a stale lock, verify the earlier run has stopped; the recorded PID belongs to the short-lived claim command and is not proof that the agent finished. This lock supports one local host, not a distributed scheduler.
