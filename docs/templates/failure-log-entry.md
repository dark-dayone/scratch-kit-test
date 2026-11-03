# Template: Failure Log Entry

One entry per failure, kept in `docs/failure-log.md`. Keep it to a few lines. The log is the evidence the improvement loop runs on, so be consistent about the stage tag.

## How to trace the stage

Work backwards and stop at the first "no":

1. Was the correct behaviour written in the spec? If not, the origin is **Spec**.
2. Did the plan account for it? If not, **Plan**.
3. Did a test cover it, derived from the spec? If not, **Tests**.
4. Did the tests exist and pass wrongly (weak, or copied the code's bug)? **Tests (quality)**.
5. Was it a coding error that tests should have caught, but the slice was too large to review? **Implementation**.
6. Did an automated gate miss it that should have caught it (security scan, dependency check)? **Gates**.
7. Was it visible to a human reviewer who missed or skipped it? **Review**.
8. Did it only break in production, or because of rollout, monitoring or config? **Release**.
9. Reported by a client after delivery? Add **Client-reported** and still trace it to a stage above.

## Entry format

```markdown
### YYYY-MM-DD: short title

- **Project / feature:**
- **Stage of origin:** Spec | Plan | Tests | Tests (quality) | Implementation | Gates | Review | Release
- **How it was found:** test failure | gate | human review | production | client report
- **What happened:**
- **Impact:** low | medium | high, and who was affected
- **What would have prevented it:**
- **Tool and agent involved:** (which tool wrote or reviewed the code)
- **Evidence:** links to the spec, commit, test output or transcript
- **Candidate improvement:** (leave blank until the improvement loop runs)
```

## Reviewing the log

After each project, count entries by stage of origin. Run the improvement loop after every finished project, and also whenever three entries share a stage. Do not decide which stage matters most in advance. Let the log show it, then propose a change through `improvement-proposal.md`.
