# Template: Client Handover

One per client project, completed before go-live and saved in `docs/handover.md`. Blanks marked `___` are business decisions to fill in per client. This is not a legal document and is not legal advice.

## 1. Project

- **Client:**
- **Project and version delivered:**
- **Demo date:**
- **Confirmation email from client saved at:** (path or link, next to the spec)

## 2. What was accepted

Link to the approved spec. The demo walked through each acceptance criterion in it.

## 3. How it is installed and run

- **Web:** hosted on Render (API and database) and Vercel (Next.js). Hosting cost paid by: `___` (client directly / passed through).
- **Android app:** installed by us from a versioned, checksummed APK. Install checklist: (link to `docs/install-checklist.md`).
- **Backups and restore:** point-in-time recovery on the database. Restore tested on: `___`.
- **Signing key location:** (where the key is kept; never the key itself).

## 4. Support option chosen

- [ ] **Option A, free-fix period:** `___` days from the confirmation email. Covers defects (the software does not do what the accepted spec says) and urgent security fixes. New features, spec gaps and change requests are quoted separately.
- [ ] **Option B, ongoing maintenance:** `___` per month. Covers defect fixes, dependency and security updates, backup and monitoring checks, and agreed response times. New features are quoted separately.

Response times: urgent outage `___`, defect `___`, question `___`.

## 5. How to report a problem

Client reports by WhatsApp or phone to: `___`. We log every report as an issue the same day, acknowledge it with a reference, and message a summary after any call.

## 6. Change requests

Priced as fixed quotes agreed before work starts. Small-change allowance (if any): `___`. A quote states what is included, the price and the date, and work starts when the client approves by reply.

## 7. Responsibilities

- **Us:** the application, the backend, the updates described above.
- **Client:** device security (operating system updates, who has access to the devices), keeping devices in working order, supplying accurate information.
- **Remote support method agreed:** `___`

## 8. Analytics and personal data

What is logged (analytics events and error reports), where it is stored (PostHog region: `___`), and who can see it.

## 9. Sign-off

Date handed over: `___`
