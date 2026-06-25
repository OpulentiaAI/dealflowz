# Company Research Reference

Use this reference when discovering, enriching, scoring, or preparing outreach for companies.

## Depth Modes

Choose depth based on the user's ask:

| Mode | Use for | Research budget |
| --- | --- | --- |
| `quick` | Screening many leads | Homepage, search snippets, one corroborating source |
| `deep` | Deciding whether to outreach or request documents | Homepage, relevant site pages, people/contact search, external corroboration |
| `deeper` | Call prep, diligence prep, or LOI support | Full source review, documents, financial context, risks, and counterparty details |

## Plan -> Research -> Synthesize

Plan:

- State the stage and decision the research must support.
- List missing fields before searching.
- Define the pass, review, and fail conditions.

Research:

- Start with the company's own website, filings, submitted forms, teaser, CIM, or direct communication when available.
- Use external sources to corroborate geography, ownership, industry, leadership, and contact details.
- Do not infer product, industry, revenue quality, or customer type from design, tech stack, tone, or generic marketing language.
- If a source is inaccessible or thin, record `Unknown` rather than filling a guess.

Synthesize:

- Write concise factual findings.
- Attach confidence to each material field: `Verified`, `Estimated`, or `Unknown`.
- Separate evidence from judgment.
- Produce a gate recommendation and the exact missing items.

## Enrichment Fields

Always try to fill:

- Website
- Headquarters geography
- Business description
- Industry keywords
- Key contacts
- Contact email and phone
- Revenue range
- EBITDA estimate if available
- Years profitable if available
- Ownership signals
- Existing communication history

## Fit Scoring

Use the primary filters from `northcliff-workflow.md`:

- Revenue in range
- EBITDA in range
- Profitability history in range
- Geography in target metros
- Business quality requires human review

Recommended scoring:

- `Pass`: all objective filters are supported by evidence.
- `Review`: at least one objective filter is unknown and no confirmed disqualifier exists.
- `Fail`: a confirmed objective disqualifier exists.

Do not let a high-quality narrative override confirmed filter failure. Put that company in `Not a target` or `Inactive` unless the user explicitly asks for an exception list.

## Output Format

For each company, return:

- Company name
- Website
- Source type and source detail
- One-sentence business description
- Field table with value, confidence, and source
- Primary filter result
- Outreach angle or reason to stop
- CRM updates
- Human review items
- Next action

## Anti-Hallucination Checks

Before finalizing:

- Confirm the company description came from a concrete source.
- Confirm revenue and EBITDA values are direct, estimated, or unknown.
- Confirm geography is headquarters or relevant operating market, not a random service area.
- Confirm no proprietary outreach begins for contacts with no lawful or valid contact path.
- Confirm the not-target reason is specific when the company fails.

