# attio-pp-cli

Token-efficient TypeScript CLI for the Attio CRM API. Agent-native flags, compound setup-check and ensure-structure commands, and a local mirror for offline compound queries. Printed in the style of [cli-printing-press](https://github.com/mvanhorn/cli-printing-press).

## Install

```bash
cd cli/attio-pp-cli
npm install   # dev deps only (typescript, @types/node)
npm run build
```

The binary is `dist/index.js`. Symlink or alias it:

```bash
alias attio-pp-cli="node $(pwd)/dist/index.js"
```

## Auth

Set `ATTIO_API_KEY` in your environment, or pass `--api-key=KEY` on every call. Get a token from Attio Settings > API tokens.

## Commands

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

## Compound Commands

### setup-check

Verifies the workspace has the required Northcliff objects (`companies`, `people`, `deals`), lists (`Northcliff Deal Flow`, `Broker Coverage`), and all required attributes. Returns a structured report of what's present and missing.

```bash
attio-pp-cli setup-check
```

### ensure-structure

Runs the setup check, then outputs an actionable creation guide listing exactly which objects, attributes, and lists need to be created and how (Attio UI path or REST API endpoint).

```bash
attio-pp-cli ensure-structure --mirror-name=setup-001
```

## Local Mirror

Results saved with `--mirror-name` are stored as JSON under `~/.attio-pp/mirror/` (override with `ATTIO_PP_MIRROR` env). Read them back with `mirror-show` without any API calls.

## Output

Compact agent-friendly output by default. Pass `--json` for raw JSON.

## Test

```bash
npm run build && npm test
```

Tests run offline with no API key required - they verify arg parsing, mirror round-trips, destructive confirm guards, and error paths.
