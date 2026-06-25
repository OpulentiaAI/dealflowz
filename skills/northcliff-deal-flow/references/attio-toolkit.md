# Attio Toolkit Reference (Composio Connector)

Use this reference when Opulent needs to inspect, create, update, or verify Attio records, objects, lists, or notes through the Composio Attio connector. This is the toolkit Opulent uses to drive Attio setup and configuration end-to-end.

## Invocation Pattern

All tools are invoked through the Composio connector:

```
connector_manage(
  action="execute",
  toolId="ATTIO_FIND_RECORD",
  params={ "object_id": "people", "attributes": { "email": "john@example.com" } }
)
```

- For paginated reads, loop with `offset` / `limit`.
- For filtered queries, prefer `ATTIO_FIND_RECORD` over `ATTIO_LIST_RECORDS`.
- Custom objects from the workspace are accepted wherever an `object_type` / `object_id` is requested.
- Standard object slugs: `people`, `companies`, `deals`, `users`, `workspaces`, plus any custom object types defined in the workspace.

## Tool Index

| # | Tool ID | Name | Mutability |
|---|---------|------|------------|
| 1 | ATTIO_CREATE_NOTE | Create Note | write |
| 2 | ATTIO_CREATE_RECORD | Create Record | write |
| 3 | ATTIO_DELETE_NOTE | Delete Note | destructive |
| 4 | ATTIO_DELETE_RECORD | Delete Record | destructive |
| 5 | ATTIO_FIND_RECORD | Find Record | read-only |
| 6 | ATTIO_GET_OBJECT | Get Object Details | read-only |
| 7 | ATTIO_LIST_LISTS | List Lists | read-only |
| 8 | ATTIO_LIST_NOTES | List Notes | read-only |
| 9 | ATTIO_LIST_OBJECTS | List Objects | read-only |
| 10 | ATTIO_LIST_RECORDS | List Records | read-only |
| 11 | ATTIO_UPDATE_RECORD | Update Record | write |

Treat destructive tools (`ATTIO_DELETE_NOTE`, `ATTIO_DELETE_RECORD`) as off-limits for routine setup. Only use them when explicitly instructed by the user, and always confirm the target record ID first.

## Tool Schemas

### 1. ATTIO_CREATE_NOTE - Create Note

Create a new note attached to a record. Notes can be attached to any object type.

Endpoint: `POST /v2/notes`

```
{
  "parent_object": "people | companies | deals | users | workspaces",
  "parent_record_id": "rec_123abc",
  "title": "Meeting Notes",
  "content": "Discussed project timeline and next steps",
  "created_at": "2023-12-25T10:30:00Z"
}
```

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| parent_object | string | yes | Object slug |
| parent_record_id | string | yes | ID of the record to attach the note to |
| title | string | yes | Note title |
| content | string | yes | Note body |
| created_at | string \| null | no | ISO 8601 timestamp; defaults to now |

### 2. ATTIO_CREATE_RECORD - Create Record

Create a new record on a given object type.

Endpoint: `POST /v2/objects/{object}/records`

```
{
  "object_type": "people",
  "values": {
    "name": [{ "first_name": "John", "last_name": "Doe", "full_name": "John Doe" }],
    "email_addresses": [{ "email_address": "john@example.com" }],
    "foundation_date": [{ "value": "2004-07-29" }],
    "credits_bought": [{ "currency_value": 1000 }]
  }
}
```

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| object_type | string | yes | Standard slug or custom object slug |
| values | object | yes | Attribute values. Currency fields use `currency_value`; most other fields use `value`. |

### 3. ATTIO_DELETE_NOTE - Delete Note

Delete a note by id. Destructive - irreversible.

Endpoint: `DELETE /v2/notes/{note_id}`

```
{ "note_id": "note_123abc" }
```

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| note_id | string | yes | Attio note id |

### 4. ATTIO_DELETE_RECORD - Delete Record

Permanently delete a record. Destructive - irreversible.

Endpoint: `DELETE /v2/objects/{object}/records/{record_id}`

```
{
  "object_type": "companies",
  "record_id": "rec_01H3PQWSN8KZQKM6KX2XS4W8PJ"
}
```

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| object_type | string | yes | Standard slug or custom |
| record_id | string | yes | Attio record id (UUID) |

### 5. ATTIO_FIND_RECORD - Find Record

Look up a record either directly by id, or by querying attributes. Read-only.

Endpoints: `GET /v2/objects/{object}/records/{record_id}` and `POST /v2/objects/{object}/records/query`

```
{
  "object_id": "people",
  "record_id": "f3b2962b-febb-4e01-8431-f7ffb4d87e5e",
  "attributes": { "email": "john@example.com" },
  "limit": 500,
  "offset": 0
}
```

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| object_id | string | yes | Object slug |
| record_id | string \| null | no | If supplied, fetches by id (mutually exclusive with attributes search) |
| attributes | object \| null | no | Attribute filter, e.g. `{"email": "..."}` |
| limit | integer \| null | no | 1-1000, default 500 (search mode only) |
| offset | integer \| null | no | Pagination offset, default 0 (search mode only) |

### 6. ATTIO_GET_OBJECT - Get Object Details

Return all attributes and properties for an object type. Read-only.

Endpoint: `GET /v2/objects/{object_id}`

```
{ "object_id": "people" }
```

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| object_id | string | yes | Standard slug or custom id |

### 7. ATTIO_LIST_LISTS - List Lists

Return every list in the Attio workspace, sorted as in the sidebar. Read-only. Requires `list_configuration:read` scope.

Endpoint: `GET /v2/lists`

No parameters.

### 8. ATTIO_LIST_NOTES - List Notes

List notes for a given record, newest first. Read-only.

Endpoint: `GET /v2/notes?parent_object=...&parent_record_id=...`

```
{
  "parent_object": "people",
  "parent_record_id": "92446133-64cf-4f83-bca9-594ca2f8da57",
  "limit": 50
}
```

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| parent_object | string | yes | Object slug |
| parent_record_id | string | yes | Record id |
| limit | integer \| null | no | 1-100, default 50 |

### 9. ATTIO_LIST_OBJECTS - List Objects

List every system-defined and user-defined object in the workspace. Read-only.

Endpoint: `GET /v2/objects`

No parameters.

### 10. ATTIO_LIST_RECORDS - List Records

List records on a given object type, oldest first (creation order). For complex filtering, use `ATTIO_FIND_RECORD`. Read-only.

Endpoint: `GET /v2/objects/{object}/records`

```
{
  "object_type": "companies",
  "limit": 20,
  "offset": 0
}
```

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| object_type | string | yes | Standard slug or custom. Verify existence with `ATTIO_LIST_OBJECTS` on 404. |
| limit | integer \| null | no | 1-500, default 20 |
| offset | integer \| null | no | Pagination offset, default 0 |

### 11. ATTIO_UPDATE_RECORD - Update Record

Patch an existing record - only the supplied fields change. Use `currency_value` for currency fields, `value` for most others.

Endpoint: `PATCH /v2/objects/{object}/records/{record_id}`

```
{
  "object_type": "people",
  "record_id": "92446133-64cf-4f83-bca9-594ca2f8da57",
  "values": {
    "name": [{ "first_name": "Jane", "last_name": "Smith", "full_name": "Jane Smith" }],
    "job_title": [{ "value": "Senior Developer" }],
    "last_credit_purchase": [{ "value": "2025-07-28" }],
    "credits_bought": [{ "currency_value": 1400 }]
  }
}
```

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| object_type | string | yes | Standard slug or custom |
| record_id | string | yes | Attio record id |
| values | object | yes | Partial attribute values; PATCH semantics (omitted fields untouched) |

## Setup Workflow Using the Toolkit

When Opulent drives Attio setup, use this ordering:

1. `ATTIO_LIST_OBJECTS` - confirm which objects already exist (`companies`, `people`, `deals`, custom `brokers`).
2. `ATTIO_GET_OBJECT` per object - inspect existing attributes before creating new ones.
3. `ATTIO_LIST_LISTS` - confirm whether `Northcliff Deal Flow` and `Broker Coverage` lists already exist.
4. Only after confirming gaps, create missing records/lists/attributes via the Attio UI or API (the Composio toolkit exposes record, note, and list reads plus record/note writes; object and attribute configuration may require the Attio UI or REST API directly - see attio-tracking.md for the configuration endpoints).
5. `ATTIO_FIND_RECORD` / `ATTIO_LIST_RECORDS` - read-after-write verification for every create/update.
6. `ATTIO_CREATE_NOTE` - attach evidence notes (source, confidence, date) to the relevant record.

Record every tool call, its parameters, and the returned record/list/note ID in the completion packet under `System update verification`.
