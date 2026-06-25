# email-pp-cli

Token-efficient TypeScript CLI for the Gmail API. Agent-native flags, compound run-update-email command for Northcliff deal-flow process emails, and a local mirror. Printed in the style of [cli-printing-press](https://github.com/mvanhorn/cli-printing-press).

## Install

```bash
cd cli/email-pp-cli
npm install   # dev deps only (typescript, @types/node)
npm run build
```

## Auth

Set `GMAIL_ACCESS_TOKEN` in your environment, or pass `--token=TOKEN` on every call. Obtain an OAuth token with `gmail.send` scope from Google OAuth flow.

## Commands

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

## Compound Command: run-update-email

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

## Test

```bash
npm run build && npm test
```

Tests run offline with no token required - 9 offline tests + 15 endpoint tests covering all Gmail API endpoints, the compound run-update-email command, base64url encoding/decoding, and error paths.
