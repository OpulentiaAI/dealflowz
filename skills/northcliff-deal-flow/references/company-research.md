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
- For proprietary sourcing, decide whether the run needs Grata company search, similar search from a seed company, list membership work, enrichment, or bulk enrichment. Load `grata-workflows.md` for the exact workflow when Grata is accessible.
- If Grata is inaccessible, continue with permitted alternative sources instead of stopping. Record Grata as blocked and use the non-Grata fallback below.

Research:

- Start with the company's own website, filings, submitted forms, teaser, CIM, or direct communication when available.
- Use Grata structured data when available for company discovery, company UID, domain, description, revenue estimate, employee estimate, locations, ownership, classifications, contacts, funding, keywords, and similar-company leads.
- If Grata is unavailable, source data from any permitted path: company website, search engine results, LinkedIn or other professional profiles, Secretary of State or business registry data, licensing databases, Google Maps or local directories, industry directories, conference exhibitor lists, trade association member lists, job postings, press releases, news, broker emails, teasers, CIMs, inbound forms, CRM exports, spreadsheets, prior research notes, file storage, email threads, and manual user-provided lists.
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

- Grata company UID
- Website
- Headquarters geography
- Business description
- Industry keywords
- Business model
- End customer
- Key contacts
- Contact email and phone
- Revenue range
- EBITDA estimate if available
- Employee estimate and employee growth if available
- Years profitable if available
- Ownership signals
- Funding signals
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

## Grata Research Pattern

For Grata-sourced proprietary leads:

1. Start with a saved or newly built search filter, including terms, exclusions, headquarters, business model, end customer, ownership, funding, employee, and list include/exclude filters.
2. Capture `company_uid`, `domain`, `url`, `description`, `count`, and `page_token` from search results.
3. Use similar search when a seed company or domain defines the target pattern better than keywords. Prefer `domain` over `company_uid` when both are present because the handoff schema says domain is referenced first.
4. Create or reuse a Grata list for each sourcing thesis or batch. Track `list_uid`, name, company count, created date, and updated date.
5. Enrich short-listed companies before CRM import. Use bulk enrichment for batches and single-company enrichment for one-off reviews or deeper diligence.
6. Map Grata output into the CRM packet with confidence:
   - `Verified`: Grata domain, company UID, Grata profile URL, and direct company website facts once corroborated by the company site.
   - `Estimated`: Grata revenue estimates, employee estimates, employee growth, funding estimates, and inferred classifications.
   - `Unknown`: EBITDA, years profitable, revenue quality, seller psychology, and valuation expectations unless supplied by a teaser, CIM, owner, broker, or financials.
7. Preserve the Grata source filter, list UID, page token, enrichment date, and any not-processed list results for auditability.

## Non-Grata Fallback Pattern

Use this when Grata is unavailable, incomplete, or not the best source for the requested lead type.

1. Mark Grata status as `blocked`, `unavailable`, or `not used`, with the reason.
2. Search existing work first: CRM exports, prior packets, notes, spreadsheets, local folders, email threads, and file storage.
3. Build a source stack suited to the target:
   - Company identity: company website, domain registration clues, business registry, local directories.
   - Geography: company site contact page, headquarters page, business registry, maps, local directories.
   - Industry and business model: company site, service pages, case studies, job postings, industry directories, trade associations.
   - Contacts: company leadership page, LinkedIn/professional profiles, email signatures, broker notes, conference speaker pages.
   - Revenue or size: teaser/CIM/financials first, then credible databases, employee counts, hiring signals, locations, and public claims as estimates.
   - Ownership/funding: company site, press releases, investor pages, Crunchbase-like sources, SEC or state filings where relevant.
4. Capture exact source URLs, file paths, thread references, or document names for every material field.
5. Mark unsupported values as `Unknown`. Use `Estimated` for inferred size, revenue, employee count, ownership, or classification.
6. Create CRM review tasks for fields that Grata would normally help fill but remain unresolved.
7. In the completion packet, include `Sourcing fallback used` with sources searched, fields filled, fields still unknown, and why Grata was not used.

## Output Format

For each company, return:

- Company name
- Grata company UID when available
- Website
- Source type and source detail
- Grata source filter or list UID when applicable
- Non-Grata fallback sources when Grata was not used or did not cover the field
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
- Confirm Grata revenue estimates are not treated as EBITDA.
- If Grata was unavailable, confirm the fallback source stack is documented and every non-Grata estimate is labeled `Estimated` or `Unknown`.
- Confirm geography is headquarters or relevant operating market, not a random service area.
- Confirm Grata location filters use country plus state when city is populated.
- Confirm paginated Grata searches capture the `page_token` when more results may exist.
- Confirm no proprietary outreach begins for contacts with no lawful or valid contact path.
- Confirm the not-target reason is specific when the company fails.
