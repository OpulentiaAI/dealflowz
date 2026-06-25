# Attio Tracking Reference

Use this reference when setting up or updating Attio tracking for Northcliff deal flow.

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
