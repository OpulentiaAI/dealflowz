# Attio Tracking Reference

Use this reference when setting up or updating Attio tracking for Northcliff deal flow.

## Opulent Drives Attio Setup

Opulent owns Attio setup and configuration end-to-end. Do not wait for the user to manually configure objects, lists, attributes, or records. Opulent inspects the workspace, identifies gaps, creates or proposes the required structure, verifies each change, and reports what was configured in the completion packet.

Principles:

- Opulent is responsible for ensuring the required objects, lists, attributes, and reference relationships exist before any deal-flow run writes to Attio.
- Inspect before creating. Always read existing objects, lists, and attributes first to avoid duplicates. Reuse existing structure wherever it matches the required model.
- Configure with the lowest-impact tool available. Prefer the Composio Attio toolkit (see `references/attio-toolkit.md`) for record, list, and note operations. For object and attribute schema creation not exposed by the toolkit, use the Attio REST API endpoints listed in `API Notes` below, or guide the user through the Attio UI only when no API path exists.
- Never mark setup complete without a read-after-write verification of every object, list, attribute, and sample record created.
- Record every configuration action, tool call, parameters, and returned ID in the completion packet under `System update verification` and `Connections`.

### Required Attio Structure

Opulent must ensure the following exists in the Northcliff Attio workspace before deal-flow runs rely on it.

Objects (verify with `ATTIO_LIST_OBJECTS`, then `ATTIO_GET_OBJECT`):

- `companies` - target businesses.
- `people` - owners, executives, bankers, broker contacts.
- `deals` - opportunity records, if enabled. If `deals` is not enabled, fall back to a dedicated deal-flow list on `companies` and note the fallback in the completion packet.
- `brokers` (custom) - only if broker-firm relationship analytics are needed beyond `people` and `companies`.

Lists (verify with `ATTIO_LIST_LISTS`):

- `Northcliff Deal Flow` - entries for company or deal records with stage, target status, source fields, document statuses, model status, LOI status, last touch, next touch, and not-target reason.
- `Broker Coverage` - entries for broker records with relationship status, cadence, deals sent, deals reviewed, deals passed, and deals advanced.

Required attributes by object/list (create via Attio REST API `POST /v2/objects/{object}/attributes` or list attributes endpoint when missing):

- Companies: `website` (domain), `revenue_estimate` (currency), `ebitda_estimate` (currency), `years_profitable` (number), `geography` (location or text), `source_type` (select/status), `source_detail` (text), `stage` (select/status), `target_status` (select/status), `nda_status` (select/status), `cim_status` (select/status), `financials_status` (select/status), `model_status` (select/status), `loi_status` (select/status), `last_touch` (date), `next_touch` (date), `reactivation_date` (date), `not_target_reason` (text), `evidence_summary` (text).
- People: `email_addresses` (email), `job_title` (text), `phone` (phone), `broker_firm` (record reference to companies or brokers), `role_type` (select/status: owner, executive, banker, broker).
- Brokers (if used): `firm_name` (text), `relationship_status` (select/status), `cadence` (text or select), `deals_sent` (number), `deals_reviewed` (number), `deals_passed` (number), `deals_advanced` (number).
- Relationships: Company or Deal -> Broker person; Company or Deal -> Broker firm; Company -> Owner or executive contacts; Deal -> Source company; Deal or Company -> Files or document links.

Keep objective filter fields separate from judgment fields:

- Objective: revenue, EBITDA, years profitable, geography.
- Judgment: business quality, revenue quality, seller psychology, valuation expectations, return profile, LOI terms.

### Setup Procedure

Run this procedure the first time Attio is wired up for Northcliff, and any time the required structure is missing or has drifted.

1. Run the Connection Startup Check below. Confirm the Composio Attio connector is available and authenticated. If missing, return a blocker with the exact next setup step - do not proceed to live writes.
2. `ATTIO_LIST_OBJECTS` - capture the full object inventory. Confirm `companies`, `people`, and `deals` exist. Flag any missing standard object.
3. `ATTIO_GET_OBJECT` for each required object - capture existing attributes. Compare against the Required Attio Structure above.
4. `ATTIO_LIST_LISTS` - confirm `Northcliff Deal Flow` and `Broker Coverage` exist. Capture list IDs.
5. For each missing object, list, or attribute, create it via the Attio REST API (`POST /v2/objects`, `POST /v2/lists`, `POST /v2/objects/{object}/attributes`, or the list attributes endpoint). If a structure cannot be created via API, guide the user through the Attio UI with the exact field name, type, and options, and record the handoff in the completion packet.
6. After creation, re-read with `ATTIO_GET_OBJECT` / `ATTIO_LIST_LISTS` to verify the new structure is present and typed correctly.
7. Create one sample record on `companies` and one on `people` using `ATTIO_CREATE_RECORD`, then immediately `ATTIO_FIND_RECORD` by the returned record ID to verify write/read round-trips. Delete the sample records with `ATTIO_DELETE_RECORD` only if the user confirms cleanup - otherwise leave them and note their IDs.
8. Attach a test note to the sample company record with `ATTIO_CREATE_NOTE` and verify with `ATTIO_LIST_NOTES`.
9. Record every action, tool call, parameters, returned IDs, and verification result in the completion packet under `System update verification` and `Connections`. Mark Attio setup `complete` only when every required object, list, attribute, and relationship is verified present.

### When Setup Cannot Be Completed From the Environment

If the Composio Attio connector is unavailable, or object/attribute creation is not exposed and the user is not present to use the Attio UI, stop before live writes and return a blocker with:

- The missing connection, credential, or permission.
- The exact Attio UI steps or REST API call required.
- The full list of objects, lists, and attributes still to be created.
- The next action the user or Opulent must take to unblock.

Do not fabricate record IDs, attribute IDs, or list IDs. Do not report setup as complete based on assumed structure.

## Connection Startup Check

Before designing or updating tracking, check for existing work and app availability:

- Search the current workspace for prior Northcliff research, CRM exports, gate packets, scripts, models, meeting notes, diligence docs, or company-specific folders.
- Check whether an Attio connector, MCP server, API key, CLI, or authenticated REST path is already available.
- Check for related app connections needed by the requested task: email for outreach/replies, calendar for calls and reminders, file storage for teasers/CIMs/financials, spreadsheets for models/imports, and document tooling for NDA/LOI drafts.
- Reuse existing records, exports, field maps, and IDs before creating new objects, lists, attributes, or imports.
- If a required connection is missing, initiate the relevant app or connector setup flow when available. If setup cannot be completed from the environment, return a blocker with the app name, purpose, missing credential or permission, and the exact next setup step.
- Do not do live writes until the needed connection and target workspace are confirmed.

## Model

Attio's data model uses:

- Objects for entity types such as companies, people, deals, users, workspaces, and custom objects.
- Records as instances of objects.
- Attributes on objects or lists for fields such as text, number, currency, select, status, date, domain, email, phone, location, and record references.
- Lists to model process-specific pipelines and add process-specific attributes.
- Record-reference attributes to connect companies, people, deals, brokers, and files.
- Tasks linked to records for next actions.
- Webhooks for record, list entry, note, task, and related events.

Source docs:

- https://docs.attio.com/docs/objects-and-lists
- https://attio.com/help/reference/attio-101/attios-data-model/define-your-data-model-objects-lists-and-views
- https://docs.attio.com/rest-api/overview
- https://docs.attio.com/rest-api/attribute-types/attribute-types

## Recommended Northcliff Structure

Objects:

- Use Companies for target businesses.
- Use People for owners, executives, bankers, and broker contacts.
- Use Deals if enabled for opportunity records. If not enabled, use a dedicated deal-flow list on Companies.
- Use a custom Brokers object only if broker firms and broker people need relationship analytics beyond People and Companies.

Lists:

- `Northcliff Deal Flow`: entries for company or deal records with stage, target status, source fields, document statuses, model status, LOI status, last touch, next touch, and not-target reason.
- `Broker Coverage`: entries for broker records with relationship status, cadence, deals sent, deals reviewed, deals passed, and deals advanced.

Relationships:

- Company or Deal -> Broker person
- Company or Deal -> Broker firm
- Company -> Owner or executive contacts
- Deal -> Source company when Deals are separate records
- Deal or Company -> Files or document links if files are modeled externally

## Attribute Design

Prefer typed attributes:

- Select/status for stage, target status, source type, NDA status, CIM status, financials status, model status, LOI status.
- Number or currency for revenue estimate and EBITDA estimate.
- Date for last touch, next touch, reactivation date, NDA dates, document due dates.
- Location or text for geography.
- Record reference for brokers, contacts, companies, and deals.
- Text for source detail, not-target reason, and evidence summary.

Keep objective filter fields separate from judgment fields:

- Objective: revenue, EBITDA, years profitable, geography.
- Judgment: business quality, revenue quality, seller psychology, valuation expectations, return profile, LOI terms.

## Automation Patterns

For every automation:

- Run the connection startup check first.
- Read existing records first to avoid duplicate companies, contacts, brokers, or deals.
- Prefer updating a current record over creating a duplicate.
- Link records immediately when a broker sends a teaser or a contact is identified.
- Create a task whenever automation cannot safely advance a stage.
- Write confidence and source notes for enriched values.
- Do not overwrite verified human-entered values with estimated enrichment values.

## API Notes

Useful API concepts:

- List attributes: `GET /v2/{target}/{identifier}/attributes`
- Create attributes: `POST /v2/{target}/{identifier}/attributes`
- List tasks: `GET /v2/tasks`
- List company record entries: `GET /v2/objects/companies/records/{record_id}/entries`

Required scopes vary by endpoint. Expect object configuration, list configuration, record permission, list entry, task, and user management scopes depending on the operation.

## Tracking Completion Checklist

Before considering CRM tracking complete:

- The record has a source type, source detail, stage, target status, and owner or next task.
- Company, broker, people, and file relationships are linked where known.
- Objective filters have value, confidence, and source.
- Missing fields are marked `Unknown`, not left ambiguous.
- Tasks have an assignee or owner, due date or trigger, linked record, and clear expected output.
- Active sequences are stopped when a lead is disqualified.
- Not-target records have a reason and no active next-touch task unless reactivation is intentional.
