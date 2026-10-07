---
name: project-setup
description: "Prepare a new project\u2019s code repository, private operating context\
  \ and native-platform integration manifest for reviewed activation."
---

## Detailed upstream workflow

This role uses gstack **/setup-deploy**, pinned at `db745675bdf9f575276db2dcd132d3c047218a12` and rendered by upstream's **Codex** generator. Read [the complete workflow](references/gstack/workflow.md), then load its local `sections/` and supporting references as each phase requires. These are imported upstream instructions, not a summary. The original template is preserved as `references/gstack/source.tmpl`; source hashes are recorded in `sources/gstack.files.json`.

Apply the CompanyOS [scheduled execution adapter](../../docs/gstack-runtime.md) before the upstream workflow. The role contract below supplies the target, trigger, allowed changes and required output. If a required input or tool is missing, return a blocked outcome; do not manufacture answers or install/enable integrations. Upstream steps never replace the configured approval boundary.

Apply the upstream technical inspection to the supplied project. Runtime installation, credential changes and resource provisioning remain outside an unattended review cycle.

## Inputs
Project brief, repository visibility, provider choices, domain, account/project identifiers and explicit provisioning scope.

## Workflow
Inspect existing resources and reuse verified identities. Prepare the code repository, separate private context, issue project, CI checks and staging/production configuration. For a frontend project use two environments and immutable artifacts; follow the chosen hosting provider.
Resolve missing destinations, billing limits and domain ownership before provisioning dependent resources. Keep credential material in platform secret stores. Record checks, rollout and rollback. A setup request does not expand access or authorize spending beyond its stated scope.

## Output
A concrete configuration manifest and reviewable infrastructure changes. Mark each connection as verified, pending or blocked. Do not activate schedules or claim a deployment exists until it has been verified.
