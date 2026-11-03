# Approved dependencies

Every direct dependency a human has approved after the plan review. CI fails a pull request that adds a direct dependency not listed here. To approve one, add a row in the same pull request, after checking the criteria in `docs/workflow.md` (section 10, rule 5).

Ecosystem is one of `python`, `npm` or `pub`. Python lists the packages in `api/requirements.in`, npm those in `web/package.json`, pub those in `mobile/pubspec.yaml`.

| Ecosystem | Package | Version | Date approved | Plan or reason |
| --- | --- | --- | --- | --- |
| python | fastapi | 0.162.0 | 2026-11-03 | baseline for scratch test |
| python | fastapi-turbo-auth-helper | 1.0 | 2026-11-03 | test |
