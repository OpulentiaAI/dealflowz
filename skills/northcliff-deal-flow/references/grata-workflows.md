# Grata Workflows Reference

Use this reference when a Northcliff run uses Grata for proprietary sourcing, similar-company discovery, list management, company enrichment, or bulk enrichment.

This reference is based on the handoff schemas in:

- `Company Search Search-Filters.json`
- `Similar Search Search-Filters.json`
- `Comany Search company-basic.json`
- `Similar Search company-Basic.json`
- `Company Enrichment company-detailed.json`
- `Bulk Company Enrichment.json`
- `Create List.json`
- `Search Lists.json`
- `List Details.json`
- `Modify List.json`
- `Update List Name.json`

## Startup Checks

Before using Grata:

- Check for existing search filters, Grata list UIDs, company UID mappings, enrichment exports, and prior CRM imports.
- Check whether a Grata app connection, API key, export file, or authenticated workflow is available.
- If Grata is inaccessible, do not stop the deal-flow run. Record the blocker and switch to the non-Grata fallback in `company-research.md`.
- Reuse existing lists and filters when they match the sourcing thesis.
- Do not create duplicate lists, duplicate CRM records, or duplicate enrichment runs without a reason.

## Company Search

Use company search for thesis-driven discovery from keywords and filters.

Core input fields:

- `terms_include.groups[].terms`
- `terms_include.groups[].terms_operator`: `any` or `all`
- `terms_include.groups[].terms_depth`: `core` or `mention`
- `terms_include.group_operator`: `any` or `all`
- `terms_exclude`
- `page_token`
- `lists.include` and `lists.exclude`
- `industry_classifications.include` and `.exclude`
- `end_customer`
- `ownership`
- `business_models`
- `is_funded`
- `funding_size`
- `funding_stage`
- `employees_change_time`
- `grata_employees_estimates_range`
- `employees_on_professional_networks_range`
- `employees_change`
- `year_founded`
- `headquarters.include` and `.exclude`

Important filter rules:

- Use `core` terms for what the company actually does.
- Use `mention` terms for weaker signals that should not define the company by themselves.
- Keep `terms_exclude` explicit and thesis-specific.
- Use `lists.exclude` to suppress already reviewed, rejected, or active companies.
- In headquarters filters, state cannot be blank if city is populated. Country must be `United States` for US city/state searches.
- Funding ranges must use Grata's allowed bounds: `0`, `5000000`, `10000000`, `20000000`, `50000000`, `100000000`, `200000000`, `500000000`, `500000001`.
- Employee maximum `100001` means all companies above the minimum.

Company search returns:

- `companies[]`
- `name`
- `company_uid`
- `url`
- `domain`
- `description`
- `count`
- `page_token`

Always store `page_token` when more results may need to be fetched.

## Similar Search

Use similar search when a known target or good example defines the sourcing thesis better than keywords.

Seed fields:

- `domain`
- `company_uid`

If both are specified, the handoff schema says `domain` is referenced first. Use domain when it is known and correct.

Similar search supports the same filters as company search, including terms, lists, industry classifications, end customer, ownership, business models, funding, employees, year founded, and headquarters.

Similar search returns:

- `company`: the seed company
- `results[]`: similar companies with name, company UID, URL, domain, and description
- `count`
- `page_token`

Use similar search after a strong target is found to build lookalike batches, then save results to a named list.

## List Management

Search lists before creating a new list.

List fields:

- `name`
- `list_uid`
- `created_date`
- `updated_date`
- `company_count`

Search lists returns:

- `results[]`
- `count`
- `page`
- `pages`

Create a list when no existing list matches the thesis. Rename a list when the thesis name changes.

Modify list membership in batches. Capture:

- Per-input `processed`
- Matched company domain and UID
- `processed.count`
- `processed.companies`
- `not_processed.count`
- `not_processed.companies`

Treat `not_processed.companies` as a verification failure or review queue. Do not silently drop those companies.

## Enrichment

Use enrichment after basic search results are shortlisted.

Basic search fields are enough for triage:

- Company UID
- Name
- Domain
- Grata URL
- Description

Detailed enrichment fields should be mapped when available:

- `company_uid`
- `name`
- `domain`
- `domains`
- `description`
- `is_active`
- `headquarters`
- `locations`
- `revenue_estimates`
- `grata_employee_estimates`
- `employee_location_breakdown`
- `employees_on_professional_networks`
- `employees_growth`
- `primary_phone`
- `primary_email`
- `social_linkedin`
- `social_facebook`
- `social_twitter`
- `social_instagram`
- `social_crunchbase`
- `ownership_status`
- `entity_type`
- `owner`
- `ultimate_owner`
- `ultimate_entity_type`
- `organization_type`
- `year_founded`
- `funding_stage`
- `latest_funding_date`
- `latest_funding_amount`
- `latest_funding_round`
- `total_funding`
- `funding_rounds_count`
- `keywords`
- `end_customer`
- `business_models`
- `classifications`
- `conferences`
- `contacts`
- `url`
- `investors`

Bulk enrichment returns:

- `errors`
- `companies[]`
- Per-company `input`

Capture `errors` even when company results are present.

## CRM Mapping

Map Grata to the deal packet and Attio as follows:

| Grata field | Northcliff field | Confidence |
| --- | --- | --- |
| `company_uid` | Grata company UID | Verified |
| `domain` | Website/domain | Verified after domain match |
| `url` | Grata profile URL | Verified |
| `description` | Business description | Estimated until corroborated |
| `headquarters` or HQ location | Geography | Estimated unless corroborated |
| `revenue_estimates` | Revenue estimate | Estimated |
| `grata_employee_estimates` | Employee estimate | Estimated |
| `employees_growth` | Employee growth | Estimated |
| `primary_phone` | Company phone | Estimated unless direct site match |
| `primary_email` | Company email | Estimated unless direct site match |
| `ownership_status`, `owner`, `ultimate_owner` | Ownership signals | Estimated |
| `business_models` | Business model | Estimated |
| `end_customer` | End customer | Estimated |
| `classifications` | Industry / vertical | Estimated |
| `contacts.contacts[]` | Contact candidates | Estimated until deliverability and role are checked |
| `funding_*`, `investors` | Funding signals | Estimated |

Never map Grata `revenue_estimates` into EBITDA. EBITDA stays `Unknown` unless supplied by broker, owner, CIM, financials, or another credible financial source.

## Northcliff Search Defaults

Use these as starting points, then adjust to the specific thesis:

- Source type: `proprietary`
- Source detail: `Grata`
- Target headquarters: Houston, San Antonio, Austin, or broader Texas only if the user asks for expansion
- Business models: usually `services`, `software_enabled`, `manufacturer`, `distributor`, or other thesis-specific non-broker models
- Exclude business brokers and investment banks unless building broker coverage
- Exclude prior reviewed lists through `lists.exclude`
- Preserve all search filters with the run output

## Verification Gates

Before importing or updating CRM:

- Verify no existing CRM record uses the same domain, company UID, or company name.
- Verify the Grata list exists or was created, and record `list_uid`.
- Verify list modifications by checking processed and not-processed counts.
- Verify enriched records include source domain or `input` for traceability.
- Verify primary filters separately from Grata discovery filters. A company can match a search and still fail Northcliff filters.
- Mark Grata-derived revenue, employee count, ownership, classification, and contact data as estimated unless corroborated.
- Create review tasks for missing EBITDA, years profitable, revenue quality, customer concentration, seller intent, and valuation expectations.

## Completion Output

For Grata runs, include:

- Search type: company search, similar search, enrichment, bulk enrichment, list create, list update, or list search
- Search filter summary and file path when available
- Seed domain or seed company UID for similar search
- List UID and list name
- Result count and page token
- Companies processed and not processed
- Enrichment errors
- CRM records created or updated
- Review tasks created
- Verification evidence for every list, enrichment, and CRM update
