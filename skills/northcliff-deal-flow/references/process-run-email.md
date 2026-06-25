# Process Run Email Reference

Use this reference when a Northcliff deal-flow run needs to send, draft, or verify a process-update email.

## Trigger

Prepare a run-update email when:

- A run creates or changes CRM records, tasks, notes, files, calendar events, emails, models, or local artifacts.
- A run advances or blocks a deal stage.
- A run finds missing app connections or permissions.
- The user asks for process updates, auditability, or verification of system updates.

If the user has not provided recipients, draft the email and mark sending as blocked until a recipient is known. Do not guess recipients.

## Email Connection Check

Before sending:

1. Check whether an email app connection, connector, MCP server, API key, or authenticated CLI is already available.
2. Confirm the sending account and recipient list.
3. Confirm whether the environment allows direct sending. If not, create a draft when possible.
4. If no email connection is available, return a blocker with the missing app, purpose, required permission, and next setup step.
5. Do not send externally unless the requested workflow, user instruction, or established environment policy authorizes sending.

## Update Verification Log

Build a verification log before composing the email.

For each system update, capture:

- `System`: Attio, email, calendar, file storage, spreadsheet, document, local repo, or other app.
- `Action`: created, updated, linked, moved stage, added task, stored file, sent email, committed file, or skipped.
- `Target`: company, contact, broker, task, file, model, document, calendar event, or message.
- `Identifier`: record ID, task ID, file path, commit hash, message ID, event ID, or API endpoint.
- `Verification`: read-after-write snapshot, API response, file existence check, diff, status output, or sent-message receipt.
- `Result`: verified, failed, blocked, skipped, or needs review.

Do not state that an update was completed unless it has verification evidence.

## Email Shape

Use this structure:

```text
Subject: Northcliff deal-flow update: [Company or run name] - [decision/status]

Hi [Name],

Here is the update from the latest Northcliff deal-flow run.

Current status:
- Stage:
- Decision:
- Next action:

Work completed:
- ...

System update verification:
- [System] [action] [target]: verified by [evidence]

Open items:
- ...

Human review needed:
- ...

Blocked items:
- ...
```

Keep the email concise. Include enough verification detail for auditability, but avoid dumping raw logs unless the user asks.

## Sending Workflow

1. Complete the main deal-flow work and gate checks.
2. Build the completion packet.
3. Build the update verification log.
4. Draft the email from verified facts only.
5. Send the email if recipients, sending account, permission, and email connection are confirmed.
6. After sending, verify delivery or creation status by checking message ID, sent folder, API response, or draft ID.
7. Add email status to the completion packet:
   - `sent`: include recipients, subject, message ID, and verification method.
   - `drafted`: include draft ID or file path and the reason it was not sent.
   - `blocked`: include missing connection, recipient, permission, or approval.
   - `skipped`: include why the run did not require an email.

## Completion Standard

A process-run email workflow is complete only when:

- The email body matches the verified run facts.
- All system updates in the email have verification evidence.
- Any unverified or failed updates are labeled as blocked, failed, or needs review.
- The sent/draft/blocked status is recorded in the completion packet.
