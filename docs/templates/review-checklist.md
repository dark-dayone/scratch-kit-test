# Template: Human Review Checklist

Use at stage six, after the automated gates have passed. Review scales with risk: every change gets Part 1, and anything touching authentication, money, personal data or permissions also gets Part 2. Read for architecture and intent, not syntax. Real test results outrank any AI opinion.

## Part 1: Every change

- [ ] The change matches the spec: each acceptance criterion maps to a test that passes
- [ ] The tests were written from the spec, and committed before the implementation
- [ ] The tests assert real behaviour (not just that code runs, and not copied from buggy code)
- [ ] The slice is small enough that I understand what it does and why
- [ ] Nothing was built that the spec lists as a non-goal
- [ ] No new dependency appeared without my approval, and each one exists, is current and trusted
- [ ] No secrets, keys or credentials in code, logs, config or test data
- [ ] Error handling is sensible: failures are handled, not swallowed
- [ ] The structure fits the plan: no surprise files, layers or patterns
- [ ] The agent's summary matches what the diff and tests actually show
- [ ] A review note is saved in the feature folder: approved or rejected, and why

## Part 2: High-risk areas (auth, money, personal data, permissions)

- [ ] Every action checks that the caller is allowed to do it, on the server side
- [ ] Input is validated and handled safely (no injection, no unsafe queries or commands)
- [ ] Sensitive data is minimised, protected, and not written to logs or error messages
- [ ] Money logic is correct on edge cases: rounding, retries, partial failures, duplicates
- [ ] Abuse cases from the spec each have a test
- [ ] Failure halfway through leaves data in a safe, consistent state
- [ ] I read the actual code for these parts, not only the summary
- [ ] A second tool reviewed it as an extra opinion, and I weighed its findings

## Part 3: Before merge

- [ ] All required checks are green on the final commit
- [ ] Rollback is possible and I know how
- [ ] If anything failed or surprised me, a failure log entry is written with its stage of origin

## Rule of thumb

If I cannot explain what a change does in a couple of sentences, it is too big or too unclear. Send it back and ask for a smaller slice, instead of approving it.
