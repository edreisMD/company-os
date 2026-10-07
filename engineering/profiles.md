# Project profiles

| Profile | Daily | Weekly | Required pre-merge evidence |
| --- | --- | --- | --- |
| website | Traffic and click/scroll evidence; errors, links; one frontend hypothesis | Compare changes over a full week; simplify low-value sections | Reproducible build, mobile/desktop screenshots, keyboard/reduced-motion checks, correct links, analytics-data handling |
| open-source | Issue/PR triage, failing checks, one small ready improvement | Backlog, contributor response time, dependency/release review | Offline unit/integration tests, reproducible bug case, updated docs; no private company data |
| private-service | Private incidents/issues/PRs and reliability improvements | Latency/error/cost trends and rollout risk | Unit/integration tests; auth, rate limits, streaming, usage accounting and tenant boundaries where affected |
| framework | Broken workflows, real user issues and reusable improvements | Remove duplicated rituals; review cadence and bottlenecks | Planner tests, workflow syntax, generic examples; no company-specific context |

A daily scan does not require a daily code change. Small samples and unchanged state are valid reasons to do nothing. Changes to payments, production data, model training or infrastructure require a separate bounded task.
