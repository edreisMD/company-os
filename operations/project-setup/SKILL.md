---
name: project-setup
description: "Prepare a new project\u2019s code repository, private operating context\
  \ and native-platform integration manifest for reviewed activation."
---

## Inputs
Project brief, repository visibility, provider choices, domain, account/project identifiers and explicit provisioning scope.

## Workflow
Inspect existing resources and reuse verified identities. Prepare the code repository, separate private context, issue project, CI checks and staging/production configuration. For a frontend project use two environments and immutable artifacts; follow the chosen hosting provider.
Resolve missing destinations, billing limits and domain ownership before provisioning dependent resources. Keep credential material in platform secret stores. Record checks, rollout and rollback. A setup request does not expand access or authorize spending beyond its stated scope.

## Output
A concrete configuration manifest and reviewable infrastructure changes. Mark each connection as verified, pending or blocked. Do not activate schedules or claim a deployment exists until it has been verified.
