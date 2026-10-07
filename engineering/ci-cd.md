# CI/CD and human approval

## Pull requests

Run CI on pull_request with contents: read, no deployment secrets, timeouts and concurrency cancellation. Avoid pull_request_target for executing PR code. A fork must never receive deployment credentials. Pin Actions to reviewed immutable revisions. Keep provider-specific credentials and private project targets out of this public framework.

Use templates/github/python-ci.yml for offline Python checks and templates/github/static-ci.yml for a static build. Adapt commands to the actual repo; a successful compile is not a substitute for unit or integration tests. The framework itself runs its planner regression tests. Each project must name its required check contexts only after they have run successfully.

## Approval enforcement

Preferred configuration: require PRs, one human approval, dismiss stale approvals, require passing checks and resolved conversations, disable force pushes and deletion, and do not grant agent bypass. The agent needs its own GitHub identity for a founder review: GitHub does not let a PR author approve their own PR. Never silently weaken this requirement to get a merge through.

When the agent shares the founder's account, the founder must explicitly approve the exact head SHA in the chat and perform the merge. This is a procedural control, not an independent GitHub-enforced approval. Scheduled agents never merge even if the account technically permits it. A separate GitHub App with limited permissions is the next step for enforced separation. Do not create credentials or widen access without the necessary authorization.

Private repository plans may not support branch protection. Record that limitation; do not make private source public or claim a policy document enforces protection. Keep releases human-operated until adequate protection is available.

## Production delivery

After an approved merge, require the test job before deployment. Use an immutable artifact tagged by the merged commit SHA rather than a mutable latest tag. Serialize production deployments without cancelling an in-progress release. Validate service health and one representative user path. Record SHA, artifact digest/version, time, smoke results and previous known-good deployment privately. If a smoke check fails, stop promotion and use the provider's verified rollback procedure; do not improvise destructive changes.

If a provider supports protected environments, use a human-approved production environment and isolate its secrets from PR jobs. GitHub configuration alone cannot enforce approval when the account/plan lacks the necessary features.

## Sites-hosted static pages

Keep source/build checks and human approval before publishing. Preview locally or with a genuine isolated preview; a Sites deployment URL is production. Once the exact source revision is approved, use the Sites hosting workflow for the existing project, preserving its audience. Save/deploy only the pushed approved source, then inspect deployment status and the live page. Do not assume a GitHub push automatically deploys Sites, and do not invent an API credential-based GitHub deployment action.

A GitHub mirror is useful for PRs but is not required for hosting. Until one exists, prepare an isolated local branch, diff and preview, obtain approval of its SHA, then perform the authorized release. The daily frontend agent cannot bypass this by directly publishing.

## Rollout

1. Run each check locally and open a workflow PR.
2. Inspect CI results on that PR; resolve failures before approval.
3. Founder approves and merges workflow changes.
4. Enable branch/environment protections with verified required-check names where supported.
5. Verify a harmless proposal-to-release cycle before permitting automatic production delivery.

Sources: [GitHub protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches), [scheduled tasks](https://learn.chatgpt.com/docs/automations?surface=app).
