# Northcliff Workflow Reference

Use this reference for pipeline design, lead routing, stage gates, and required completion behavior.

## Target Model

Use one CRM pipeline with two source paths:

- `Proprietary sourced`: Grata lists, permitted web research, LinkedIn, inbound website, personal network.
- `Broker sourced`: Texas broker outreach, email, LinkedIn, calls, teasers, CIMs.

Shared stages:

1. `New lead`
2. `Data enrichment`
3. `Primary filter review`
4. `Outreach sequence`
5. `Owner or broker replied`
6. `NDA / CIM / financial request`
7. `Financial modeling`
8. `Seller or broker call`
9. `LOI drafting`
10. `Not a target`
11. `Inactive / released lead`

## Core Fields

Company fields:

- Business name
- Website
- Source type: proprietary, broker, inbound, network
- Source detail: Grata, web scrape, LinkedIn, broker name, inbound form, referral
- Revenue estimate
- EBITDA estimate
- Years profitable
- Geography
- Industry / vertical
- Contact name, role, email, phone
- Broker name and broker firm
- Last touch date
- Next touch date
- Stage
- Target status: unknown, target, not target, needs review
- Not-target reason
- NDA status
- CIM status
- Financials status
- Model status
- LOI status

File fields:

- Teaser received
- NDA received
- NDA signed
- CIM received
- Financial statements received
- Model created
- LOI draft created

Broker fields:

- Broker name
- Firm
- Geography
- Vertical focus
- Relationship status: new, contacted, warm, active, inactive
- Last contact date
- Next contact date
- Deals sent
- Deals reviewed
- Deals passed
- Deals advanced

## Event Routing

| Trigger | Automation action | Human review point |
| --- | --- | --- |
| New proprietary company added | Enrich company, contacts, website, geography, estimates | Confirm target fit if data is incomplete |
| New broker added | Start broker outreach cadence and monthly follow-up reminders | Review broker quality and relationship priority |
| Broker sends teaser | Create company record, link broker, request NDA/CIM path | Confirm whether deal is worth NDA/review time |
| Primary filters pass | Move to outreach or engagement stage | Confirm business quality and personal interest |
| Primary filters fail | Move to `Not a target`, record reason, stop sequences | Review only if data confidence is low |
| Outreach reply received | Classify reply, update stage, create next task | Decide tone and next ask |
| No reply after sequence | Create cold-call task, then mark not responsive if no answer | Decide whether to recycle later |
| NDA signed | Request CIM, financials, value expectations, seller financing details | Review legal or process exceptions |
| Financials received | Create mini-model task and pre-fill known fields | Review normalized EBITDA and return profile |
| Model passes return screen | Create seller/broker call prep package | Decide whether to schedule the call |
| Call completed | Extract notes, action items, terms, risks | Decide whether to draft LOI |
| LOI stage reached | Generate first-pass term summary and missing-item checklist | Approve final LOI terms before sending |

## Grata Sourcing Gate

Use this gate before importing proprietary Grata leads to Attio.

Required source evidence:

- Search type: company search or similar search
- Search filter JSON or saved filter summary
- Seed domain or seed `company_uid` for similar search
- Grata list UID if companies were saved to a list
- Result `company_uid`, domain, Grata URL, description, count, and `page_token` when present
- Enrichment timestamp and source file or API response

Search filter controls:

- Use `terms_include.groups` with `terms_operator` and `terms_depth` to separate core keywords from mention-only keywords.
- Use `terms_exclude` for off-thesis, franchise, staffing, broker, investor, or software-only exclusions when applicable.
- Use `lists.include` to continue working an existing list and `lists.exclude` to avoid prior reviewed or rejected companies.
- Use `headquarters.include` for target geography. If city is populated, state must also be populated.
- Use `business_models`, `end_customer`, ownership, funding, employee count, employee growth, year founded, and industry classifications only when they support the thesis rather than overfitting the search.

List workflow:

- Search existing lists before creating a new one.
- Create a list only when no suitable list exists.
- Rename a list when the thesis name changes rather than creating duplicates.
- Modify list membership in batches and record processed and not-processed domains.
- Treat not-processed domains as review items, not silent failures.

Enrichment workflow:

- For search results, first capture basic fields: `company_uid`, name, domain, Grata URL, and description.
- For shortlisted companies, enrich detailed fields: active status, headquarters, locations, revenue estimate, employee estimates, employee growth, primary phone, primary email, social links, ownership status, entity type, owner, ultimate owner, organization type, year founded, funding, keywords, end customer, business models, classifications, conferences, contacts, and investors.
- Bulk enrichment should return an `errors` array and per-company `input`; log both.
- Do not import companies with unresolved domain matching issues until the domain is reviewed.

Expected result: Grata batches enter CRM with traceable search logic, deduplicated list membership, enriched fields, and explicit review items.

## Primary Filter Gate

Check:

- Revenue: $5mm to $25mm
- EBITDA: $1mm to $5mm
- Profitability: 3 or more years
- Geography: Houston, San Antonio, or Austin
- Business quality: manual review

Outcomes:

- `Pass`: revenue, EBITDA, profitability, and geography appear in range.
- `Review`: one or more fields are unknown, but the business may fit.
- `Fail`: confirmed outside target range or geography.

Automation behavior:

- If `Pass`, move to outreach or deal engagement and create the next task.
- If `Review`, assign a human task to confirm fit.
- If `Fail`, move to `Not a target`, log the reason, and release or suppress the lead.

## Proprietary Outreach Gate

Before starting outreach:

- Confirm at least one valid contact path or create a contact research task.
- Sync opens, clicks, replies, bounces, unsubscribes, calls, and notes back to the CRM when available.
- If no reply after sequence, create a cold-call task.
- If still no reply, mark `Not responsive` or `Inactive / released lead` and set a future reactivation date only when appropriate.

Reply classification:

- Positive reply: move to `Owner or broker replied`.
- Referral reply: update contact and continue outreach.
- Not interested: move to `Not a target` or `Inactive`, depending on reason.
- Bad fit: record not-target reason.

## Broker Relationship Gate

Maintain broker coverage separately from company deal flow:

- Link each broker-sourced company to the broker record.
- Track every teaser, email, call, and meeting.
- Create monthly follow-up tasks for warm and active brokers.
- Update deals sent, reviewed, passed, and advanced.

## NDA, CIM, and Financial Collection Gate

Required checklist:

- NDA
- CIM or business overview
- Historical financials
- Revenue quality detail
- Customer concentration detail
- Seller financing expectations
- Valuation expectations

Automation should:

- Generate or send NDA packet only when appropriate.
- Track NDA sent, signed, and countersigned.
- Request CIM, financials, value expectations, seller financing openness, and process timing after NDA completion.
- Create reminders for missing documents.
- Store files in the correct company folder and link them to the CRM.

## Financial Modeling Gate

When financials arrive:

- Create a model task.
- Copy or create a mini-model template.
- Pre-fill company name, source, revenue, EBITDA, and known financing assumptions.
- Flag missing financial items.
- Assign human review for revenue quality, normalized EBITDA, financing needs, and return profile.

Decision outcomes:

- `Returns support next step`: move to seller or broker call.
- `Needs more information`: request missing details.
- `Does not provide returns`: move to `Not a target` with reason.

## Call Gate

Call prep package:

- Call agenda
- Known company facts
- Open diligence questions
- Financial model summary
- Deal terms to discuss
- Value expectation notes
- Seller financing questions

After the call:

- Log transcript or notes.
- Extract action items.
- Update valuation expectations, seller financing, deal terms, and risks.
- Set next stage: more diligence, LOI drafting, not target, or inactive.

## LOI Drafting Gate

When the model and call support an LOI:

- Create an LOI drafting task.
- Pull specific deal terms from the CRM.
- Generate a first-pass LOI term sheet or memo for review.
- Highlight missing purchase price, structure, seller note, earnout, working capital, exclusivity, closing timeline, and diligence conditions.
- Require human approval before sending anything externally.

## Not-Target Gate

Required behavior:

- Update CRM stage to `Not a target`.
- Record not-target reason.
- Preserve communication history.
- Remove from active sequences.
- Release or suppress the lead.
- Set a reactivation date only if the reason is timing-related.

Common reasons:

- Revenue too low or too high
- EBITDA too low or too high
- Not profitable for 3 or more years
- Wrong geography
- Business quality concern
- Poor revenue quality
- Seller expectations too high
- Return profile fails
- No response
- Broker relationship inactive
