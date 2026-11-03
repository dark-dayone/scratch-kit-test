# Template: Feature Spec

Fill this in before any code is written. Copy it into the feature's folder as `spec.md`. If you cannot fill a section, that is a gap to resolve now, not later.

## 1. Summary

One or two sentences: what this feature does and who it is for.

## 2. Why

The problem it solves and what success looks like for the user or client.

## 3. Behaviour with examples

The most important section. Give concrete cases, not descriptions. Each example becomes a test.

| # | Given (input or state) | When (action) | Then (exact expected result) |
| --- | --- | --- | --- |
| 1 | | | |
| 2 | | | |
| 3 | | | |

## 4. Edge cases and failure behaviour

Walk the feature through each question and write down what should happen:

- Empty, missing, very large or malformed input?
- Failure halfway through (network drops, crash, partial save)?
- Two users or processes acting at the same time?
- What happens to existing data?
- Slow, unavailable or wrong responses from an external service?

## 5. Abuse cases (security)

What must happen when someone misuses it:

- Malicious or unexpected input (injection, oversized, wrong type)?
- A user without permission attempts the action?
- Sensitive data: what is stored, logged, shown, and to whom?
- Authentication and authorization rules that apply.

## 6. Non-goals

What this feature must NOT do or include. This stops the agent inventing extra features and complexity.

## 7. Constraints

Performance limits, allowed and forbidden libraries, compatibility needs, data rules, deadlines.

## 8. API contract and analytics events

- API endpoints touched or added (the OpenAPI contract is reviewed and versioned).
- Every analytics event logged, with the exact fields. No personal data in events.

## 9. Acceptance criteria

A short checklist of statements that must all be true for this feature to count as done. Each should be checkable by a test or a clear manual check. These are what the client demo walks through.

- [ ]
- [ ]
- [ ]

## 10. Risk level

Does this touch authentication, money, personal data or permissions? If yes, mark it high risk: it gets a careful human read at review.

## 11. Spec check before coding

- [ ] The agent interviewed me and asked its questions before writing anything
- [ ] The agent restated the spec in its own words and it matches my intent
- [ ] Someone (or another agent) tried to break the spec: where is it ambiguous, where could two developers build different things?
