---
name: northcliff-deal-flow
description: Guides Northcliff Capital deal sourcing, Grata company search, enrichment, list workflows, and Attio CRM tracking for lower-middle-market acquisition leads. Use when researching companies, checking existing system work, connecting needed apps, sending process-update emails, broker-sourced teasers, enrichment, primary filter scoring, outreach, NDA or CIM collection, financial modeling prep, seller calls, LOI drafting support, not-target handling, or building verification and completion gates for deal-flow automations.
---

# Northcliff Deal Flow

Use this skill to move Northcliff acquisition opportunities through research, scoring, CRM tracking, and diligence gates without losing evidence, next steps, or human review points.

## Startup Check

Run this check every time the skill is used, before new research, imports, or CRM updates:

1. Check the current system for existing work: local files, prior research folders, current workspace artifacts, known CRM exports, email/thread context, saved packets, models, docs, and earlier notes related to the company, broker, contact, or deal.
2. Reuse and reconcile existing work before creating anything new. Prefer updating the current record, packet, model, or note over creating a duplicate.
3. Identify required apps and data connections for the requested task, such as Attio, email, calendar, file storage, web research, spreadsheets, or document tooling.
4. Check whether each needed app connection, connector, MCP server, API key, or CLI is already available in the active environment.
5. If a needed connection is missing, create or initiate the connection using the available app/connector/plugin setup flow. If the environment cannot create it directly, stop before live writes and return the exact missing connection, required permission, and next setup step.
6. Record what was found, reused, connected, or blocked in the completion packet.

## Load References

- Read `references/northcliff-workflow.md` for stages, field requirements, gate logic, and not-target handling.
- Read `references/company-research.md` when discovering, enriching, or scoring companies.
- Read `references/grata-workflows.md` when using Grata company search, similar search, enrichment, bulk enrichment, or list management.
- Read `references/attio-tracking.md` when designing or updating Attio objects, lists, fields, automations, app connections, tasks, or API syncs, and any time Attio setup or configuration is required.
- Read `references/attio-toolkit.md` when invoking the Composio Attio connector to inspect, create, update, or verify Attio records, lists, objects, or notes.
- Read `references/cli-tools.md` when using the grata-pp-cli, attio-pp-cli, or email-pp-cli TypeScript CLIs for Grata search/enrichment/list operations, Attio record/list/note operations, email send/draft/read operations, or compound commands (sourcing-run, setup-check, ensure-structure, run-update-email).
- Read `references/process-run-email.md` when sending, drafting, or verifying run-update emails.
- Use `scripts/validate_gate_packet.py` when a structured gate packet exists or when you need to test whether a deal has enough data to advance.

## Operating Rules

- Opulent drives Attio setup and configuration. Before any deal-flow run writes to Attio, Opulent inspects the workspace, ensures the required objects, lists, attributes, and relationships exist, verifies each change with a read-after-write check, and records every configuration action in the completion packet. Do not wait for the user to manually configure Attio. Use `attio-pp-cli setup-check` and `attio-pp-cli ensure-structure` to verify and guide setup. See `references/attio-tracking.md` for the required structure and setup procedure, `references/attio-toolkit.md` for the Composio Attio connector tools, and `references/cli-tools.md` for the CLIs.
- Prefer the grata-pp-cli, attio-pp-cli, and email-pp-cli TypeScript CLIs (under `cli/` in the dealflowz repo) for Grata, Attio, and email operations. They are agent-native, token-efficient, and support compound commands that collapse multiple API calls into one. Build them with `npm run build` in each CLI directory. See `references/cli-tools.md` for full command reference.
- Treat the CRM as the system of record for companies, brokers, contacts, communications, files, stages, and next actions.
- Prefer Grata for structured proprietary sourcing when accessible, but do not block research if Grata is unavailable. Use any permitted source path that can produce evidence and confidence labels.
- Never mark a company investable only from automation. Use automation to enrich, draft, classify, and prepare review.
- Preserve source evidence. Every material claim should have a source, confidence, and date.
- Distinguish `Verified`, `Estimated`, and `Unknown` values. Do not fill unknown revenue, EBITDA, profitability, geography, or seller intent with guesses.
- Stop active outreach before setting `Not a target` or `Inactive`.
- Require a next task, next touch date, or closed status before considering any lead complete.
- Do not perform live CRM, email, file, or calendar writes until the relevant app connection is confirmed.
- Verify every system update with a read-after-write check or equivalent evidence before reporting it as complete.

## Workflow

1. Identify the source path: proprietary, broker, inbound, or network.
2. Determine the current stage and the next required gate.
3. Complete the startup check and app connection check.
4. Plan the work: list the missing fields, documents, people, and decisions.
5. Research with the Plan -> Research -> Synthesize pattern from `references/company-research.md`; if Grata is inaccessible, use the non-Grata sourcing fallback in that reference.
6. Update or propose CRM changes using the Attio model in `references/attio-tracking.md`.
7. Apply the gate rules in `references/northcliff-workflow.md`.
8. Verify each system update: CRM records, tasks, notes, files, calendar events, emails, models, and local artifacts.
9. Send or draft a process-run update email using `references/process-run-email.md`.
10. Produce a completion packet with status, evidence, open risks, required human review, and next action.

## Deal Packet Shape

Use this structure for outputs, imports, or validation packets:

```json
{
  "company": "Example Services LLC",
  "source_type": "proprietary",
  "stage": "Primary filter review",
  "target_status": "needs review",
  "fields": {
    "website": {"value": "https://example.com", "confidence": "Verified", "source": "company website"},
    "revenue_estimate": {"value": 12000000, "confidence": "Estimated", "source": "data provider"},
    "ebitda_estimate": {"value": 2500000, "confidence": "Estimated", "source": "broker teaser"},
    "years_profitable": {"value": 4, "confidence": "Verified", "source": "seller email"},
    "geography": {"value": "Austin, TX", "confidence": "Verified", "source": "company website"}
  },
  "evidence": [],
  "documents": [],
  "tasks": [],
  "human_review": []
}
```

## Verification Gates

Before advancing a stage, verify:

- Required fields for the next gate are present or explicitly marked `Unknown`.
- Evidence supports each positive filter decision.
- A human review item exists for business quality, revenue quality, normalized EBITDA, valuation expectation, seller psychology, or LOI terms when those judgments are relevant.
- Attio tracking fields, stage, status, linked broker/contact records, and tasks are internally consistent.
- Any disqualification includes a not-target reason, stopped sequence, communication history, and reactivation date only when timing-related.
- Every claimed system update has verification evidence: record ID, task ID, file path, commit hash, email message ID, API response, or a reread snapshot.

When a JSON packet is available, run:

```bash
python3 /Users/jeremyalston/.codex/skills/northcliff-deal-flow/scripts/validate_gate_packet.py path/to/packet.json
```

## Completion Packet

End every substantive run with:

- `Current stage`: the CRM stage now supported by the evidence.
- `Decision`: pass, review, fail, inactive, or needs more information.
- `Evidence used`: concise list of sources and confidence.
- `CRM updates`: fields, links, tasks, files, and stage changes to write.
- `Existing work checked`: files, records, threads, packets, or exports found and reused.
- `Connections`: apps/tools confirmed, connected, or blocked.
- `System update verification`: each update made, how it was verified, and any failed verification.
- `Run update email`: sent, drafted, skipped, or blocked; include recipient, subject, and message ID when available.
- `Human review`: decisions automation must not make.
- `Next action`: one owner, one due date or trigger, and one expected output.
