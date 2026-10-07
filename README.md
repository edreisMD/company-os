# Company OS

A small, runtime-independent operating manual for an agent-run company.

Start with one operator and one daily cycle. Roles are modes of work, not a requirement to run separate bots. This repository provides operating procedures, CI templates and a tested local run planner. Scheduling is configured separately by each company.

## Repository boundaries

| Repository | Visibility | Owns |
| --- | --- | --- |
| company-os | Public | Generic roles, rituals, run contract, project brief and release standards |
| landing-kit | Public | Reusable landing-page implementation, design rules and fictional examples |
| company-private | Private | Company mission, priorities, project registry, decisions, run state and provider identifiers |
| Each product | Public or private by project | Product code, public copy, tests and deployment configuration |

Keep private context in a separate checkout. Public repositories receive only explicitly selected product copy and generic improvements. Never copy run logs, company context, credentials or customer data into a public repository. A private repository also must not contain credentials; store references to a secret manager instead.

## Start here

For the engineering implementation, start with [Engineering workflows](engineering/README.md). All scheduled work ends in a proposal; humans approve and merge the exact revision before release.

1. Read [roles](roles.md) and [cadence](cadence.md).
2. Create one project using the [brief](templates/project-brief.md).
3. Configure a runtime using the [run contract](run-contract.md).
4. Ship against the [release standard](standards/release.md).

The first useful system is a complete loop: choose one task, implement it, verify it, publish within configured permissions, record the result, stop. Add another bot only when a measured bottleneck requires simultaneous work or independently credentialed review.

## Inspiration

[gstack](https://github.com/garrytan/gstack) illustrates role-specific software workflows. This project adds an explicit cadence, durable state, and a public/private boundary. It does not include gstack code or claim compatibility with a particular agent runtime.
