# CLI Tools Reference

Northcliff deal flow uses three agent-native TypeScript CLIs, built in the style of [cli-printing-press](https://github.com/mvanhorn/cli-printing-press). All live under `cli/` in the dealflowz repo and share the same conventions: token-efficient compact output, compound commands, local mirrors for offline queries, and `--json` for raw output.

## Build and Install

```bash
# Grata CLI
cd cli/grata-pp-cli && npm install && npm run build

# Attio CLI
cd cli/attio-pp-cli && npm install && npm run build

# Email CLI
cd cli/email-pp-cli && npm install && npm run build
```

After building, alias or symlink the binaries:

```bash
alias grata-pp-cli="node /path/to/dealflowz/cli/grata-pp-cli/dist/index.js"
alias attio-pp-cli="node /path/to/dealflowz/cli/attio-pp-cli/dist/index.js"
alias email-pp-cli="node /path/to/dealflowz/cli/email-pp-cli/dist/index.js"
```

## Auth

- Grata: `GRATA_API_KEY` env or `--api-key=KEY`. Get a token from Grata admin account settings.
- Attio: `ATTIO_API_KEY` env or `--api-key=KEY`. Get a token from Attio Settings > API tokens.
- Email (Gmail): `GMAIL_ACCESS_TOKEN` env or `--token=TOKEN`. Obtain an OAuth token with `gmail.send` scope from Google OAuth flow.

## grata-pp-cli

Token-efficient CLI for the Grata company search, similar search, enrichment, and list APIs.

### Commands

| Command | Description |
|---------|-------------|
| `search` | Company search by keywords and filters |
| `similar` | Similar-company search by seed domain or company_uid |
| `enrich` | Enrich a single company by domain or company_uid |
| `bulk-enrich` | Bulk enrich multiple companies |
| `lists` | Search existing lists |
| `list-create` | Create a new list |
| `list-modify` | Add or remove companies from a list |
| `sourcing-run` | Compound: search/similar -> enrich -> save to list -> mirror locally |
| `mirror-show` | Read a previously mirrored result set |
| `mirror-list` | List files in the local mirror |

### Compound Command: sourcing-run

The signature printing-press pattern - one call that does what would otherwise take 4-5 separate API round-trips:

```bash
grata-pp-cli sourcing-run \
  --terms="hvac,plumbing" \
  --hq-state=TX \
  --employees=10,200 \
  --list-name="Texas HVAC Targets" \
  --mirror-name=tx-hvac-001
```

Runs a company search, enriches each result, creates (or reuses) a Grata list, adds the companies to it, and saves the full result set to a local mirror file for offline compound queries later.

### Key Search Filters

- `--terms=a,b` - core terms (comma-separated, any-match within group)
- `--exclude=a,b` - exclude terms
- `--employees=10,100` - Grata employee estimate range [min,max]
- `--founded=1970,2018` - year founded range
- `--funding=0,100M` - funding size range (use allowed bounds)
- `--ownership=investor_backed` - ownership filter
- `--business-models=software` - business models
- `--end-customer=b2b,b2c` - end customer types
- `--hq-country=United States` - headquarters country
- `--hq-state=TX` - headquarters state (requires country)
- `--include-lists=uid1,uid2` / `--exclude-lists=uid1,uid2` - list filters
- `--page-token=TOKEN` - pagination token

### Local Mirror

Results saved with `--mirror-name` are stored as JSON under `~/.grata-pp/mirror/` (override with `GRATA_PP_MIRROR` env). Read them back with `mirror-show` without any API calls.

## attio-pp-cli

Token-efficient CLI for the Attio CRM API.

### Commands

| Command | Description |
|---------|-------------|
| `list-objects` | List all objects in the workspace |
| `get-object` | Get details and attributes for one object |
| `list-lists` | List all lists in the workspace |
| `list-records` | List records on an object (paginated) |
| `find-record` | Find a record by ID or attribute filter |
| `create-record` | Create a new record |
| `update-record` | Update (patch) an existing record |
| `delete-record` | Delete a record (destructive, requires --confirm) |
| `list-notes` | List notes attached to a record |
| `create-note` | Create a note on a record |
| `delete-note` | Delete a note (destructive, requires --confirm) |
| `setup-check` | Compound: verify workspace has required Northcliff objects/lists/attributes |
| `ensure-structure` | Compound: inspect -> report missing -> guide creation of required structure |
| `mirror-show` | Read a previously mirrored result set |
| `mirror-list` | List files in the local mirror |

### Compound Commands

#### setup-check

Verifies the workspace has the required Northcliff objects (`companies`, `people`, `deals`), lists (`Northcliff Deal Flow`, `Broker Coverage`), and all required attributes. Returns a structured report of what is present and missing.

```bash
attio-pp-cli setup-check
```

#### ensure-structure

Runs the setup check, then outputs an actionable creation guide listing exactly which objects, attributes, and lists need to be created and how (Attio UI path or REST API endpoint).

```bash
attio-pp-cli ensure-structure --mirror-name=setup-001
```

### Record Operations

```bash
# Find by attribute
attio-pp-cli find-record --object=people --filter=email=john@example.com

# Create with shortcuts
attio-pp-cli create-record --object=companies --name="Acme LLC" --domain=acme.com

# Update with JSON values
attio-pp-cli update-record --object=companies --record-id=rec_123 --values='{"stage":[{"value":"Primary filter"}]}'

# Attach an evidence note
attio-pp-cli create-note --parent-object=companies --parent-record-id=rec_123 --title="Source" --content="Grata search 2024-01-01"
```

### Local Mirror

Results saved with `--mirror-name` are stored as JSON under `~/.attio-pp/mirror/` (override with `ATTIO_PP_MIRROR` env).

## email-pp-cli

Token-efficient CLI for the Gmail API. Used for sending, drafting, and reading emails, including the compound `run-update-email` command for Northcliff process-run update emails.

### Commands

| Command | Description |
|---------|-------------|
| `profile` | Get the authenticated user's profile (email address) |
| `send` | Send an email message |
| `draft` | Create a draft email |
| `draft-send` | Send an existing draft by ID |
| `draft-list` | List drafts |
| `draft-delete` | Delete a draft (destructive, requires --confirm) |
| `messages` | List messages in inbox (with search query) |
| `message` | Get a single message by ID (decodes body) |
| `labels` | List all labels |
| `run-update-email` | Compound: build + send/draft a Northcliff process-run update email |
| `mirror-show` | Read a previously mirrored result set |
| `mirror-list` | List files in the local mirror |

### Compound Command: run-update-email

Builds a Northcliff deal-flow process-update email following the `process-run-email.md` template and sends it (or creates a draft with `--draft`):

```bash
email-pp-cli run-update-email \
  --from=me@northcliff.com \
  --to=team@northcliff.com \
  --company="Acme LLC" \
  --stage="Primary filter" \
  --decision=pass \
  --next-action="Call broker" \
  --work="Grata search,Attio update" \
  --verifications="Attio:record created,Email:verified" \
  --mirror-name=run-001
```

The email body is auto-generated with the standard Northcliff update structure: current status, work completed, system update verification, open items, human review needed, and blocked items.

### Send and Draft

```bash
# Send a simple email
email-pp-cli send --from=me@northcliff.com --to=broker@ib.com --subject="NDA Request" --body="Please find attached..."

# Create a draft for review
email-pp-cli draft --from=me@northcliff.com --to=owner@acme.com --subject="LOI" --body="Draft LOI terms..."

# Search inbox for broker replies
email-pp-cli messages --query="from:broker@ib.com newer_than:7d" --max-results=10

# Read a specific message (body auto-decoded)
email-pp-cli message --id=msg123
```

### Local Mirror

Results saved with `--mirror-name` are stored as JSON under `~/.email-pp/mirror/` (override with `EMAIL_PP_MIRROR` env).

## Testing

All three CLIs have offline and mock-HTTP endpoint test suites that require no API key and no network:

```bash
cd cli/grata-pp-cli && npm run build && npm test   # 10 offline + 18 endpoint = 28 tests
cd cli/attio-pp-cli && npm run build && npm test   # 12 offline + 17 endpoint = 29 tests
cd cli/email-pp-cli && npm run build && npm test   # 9 offline + 13 endpoint = 22 tests
```

Tests verify: arg parsing, filter/body building, endpoint URLs, HTTP methods, auth headers, request bodies, mirror round-trips, destructive confirm guards, compound command call sequences, base64url encoding, and error paths.

## When to Use CLIs vs Composio Connector

- Use `grata-pp-cli` for all Grata operations - it is the primary Grata interface for this skill.
- Use `attio-pp-cli` for Attio record, list, note, and setup operations. The Composio Attio connector (documented in `references/attio-toolkit.md`) remains available as an alternative when a connector-based flow is preferred.
- Use `email-pp-cli` for sending, drafting, and reading emails, including the compound `run-update-email` command for Northcliff process-run update emails.
- Prefer the CLIs for compound operations (`sourcing-run`, `setup-check`, `ensure-structure`, `run-update-email`) that would otherwise require multiple individual API calls.
- Use `--json` when piping output to another tool or when the agent needs the raw API response.
