# Skill: design-api-spec

## Purpose

Design a complete RESTful API specification for a feature before implementation begins. This spec is handed to the Backend Engineer agent as the authoritative contract. It defines every endpoint, all request/response schemas, authentication requirements, error codes, and rate limiting expectations.

Writing the spec before coding prevents scope creep, surfaces design problems early, and allows frontend and backend to develop in parallel against a shared contract.

## Used By

Software Architect Agent

## Inputs

| Input | Type | Description |
| --- | --- | --- |
| `feature_name` | string | The feature being designed (e.g. "Game Sessions") |
| `user_stories` | list | What the feature does from the user's perspective |
| `data_entities` | list | The core data models involved (e.g. GameSession, Student, Question) |

## Procedure / Template

**Step 1 — Identify all operations.**
For each user story, determine the HTTP operation needed. Map each to a resource and a verb:
- Create → POST
- Read one → GET /resource/:id
- Read list → GET /resource (with query params for filtering/pagination)
- Update → PATCH (partial) or PUT (full replace)
- Delete → DELETE

**Step 2 — Group endpoints under a base path.**
AceQuest base URL: `/api/v1/`. Feature endpoints live under a logical resource name (e.g. `/api/v1/game-sessions`).

**Step 3 — Fill in the template below for each endpoint.**

**Step 4 — Define Zod schemas** for all request bodies and success response payloads. These become the source of truth for the Backend Engineer's validation code.

**Step 5 — Enumerate all error scenarios** for each endpoint: invalid input (400), unauthenticated (401), insufficient permissions (403), not found (404), conflict (409), server error (500).

---

```markdown
# API Specification: [Feature Name]

**Version:** 1.0
**Date:** YYYY-MM-DD
**Author:** Software Architect Agent
**Status:** draft | approved | superseded

---

## Overview

[2–3 sentences describing what this API enables. Who calls it — Next.js Server Actions, client components, or external services? What is the primary resource?]

---

## Base URL
```
/api/v1/[resource]
```
---

## Authentication

All endpoints require a Bearer JWT token in the `Authorization` header unless marked `[PUBLIC]`.
```
Authorization: Bearer <jwt_token>
```
Tokens are issued by [auth provider — e.g. Clerk]. The JWT payload includes:
- `sub`: userId (string)
- `role`: "student" | "parent" | "admin"
- `grade`: number (students only)

Guest sessions use a session cookie; endpoints supporting guests are marked `[GUEST OK]`.

---

## Rate Limiting

| Tier | Limit |
|---|---|
| Authenticated user | 100 requests / minute |
| Guest | 20 requests / minute |
| Admin | 500 requests / minute |

Rate limit headers returned on every response:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 94
X-RateLimit-Reset: 1706000000
```
Exceeded limit returns `429 Too Many Requests`.

---

## Endpoints

| Method | Path | Auth | Description |
|---|---|---|---|
| POST | `/api/v1/[resource]` | Required | [Description] |
| GET | `/api/v1/[resource]/:id` | Required | [Description] |
| GET | `/api/v1/[resource]` | Required | [Description — list with pagination] |
| PATCH | `/api/v1/[resource]/:id` | Required | [Description] |
| DELETE | `/api/v1/[resource]/:id` | Required (Admin) | [Description] |

---

## Endpoint Definitions

---

### POST /api/v1/[resource]

**Description:** [What this creates and why]
**Auth:** Required — `role: student | parent`
**Rate limit:** Standard

#### Request Body

```typescript
// Zod schema (TypeScript)
const CreateResourceSchema = z.object({
  fieldOne: z.string().min(1).max(255),
  fieldTwo: z.enum(['value_a', 'value_b']),
  fieldThree: z.number().int().min(1).max(100).optional(),
})

type CreateResourceInput = z.infer<typeof CreateResourceSchema>
```

#### Success Response — `201 Created`

```json
{
  "id": "uuid",
  "fieldOne": "string",
  "fieldTwo": "value_a",
  "fieldThree": 42,
  "createdAt": "2025-01-15T10:30:00.000Z"
}
```

#### Error Responses

| Status | Code | Description |
| --- | --- | --- |
| 400 | `VALIDATION_ERROR` | Request body failed Zod validation |
| 401 | `UNAUTHORIZED` | Missing or invalid JWT |
| 403 | `FORBIDDEN` | User role not permitted |
| 409 | `CONFLICT` | [Describe conflict scenario] |
| 500 | `INTERNAL_ERROR` | Unexpected server error |

Error response body (consistent across all endpoints):
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "fieldOne must be at least 1 character",
    "details": [
      { "field": "fieldOne", "message": "String must contain at least 1 character(s)" }
    ]
  }
}
```

---

### GET /api/v1/[resource]/:id

**Description:** [What this returns]
**Auth:** Required
**Rate limit:** Standard

#### Path Parameters

| Parameter | Type | Description |
| --- | --- | --- |
| `id` | `string (uuid)` | Resource identifier |

#### Success Response — `200 OK`

```json
{
  "id": "uuid",
  "fieldOne": "string",
  "fieldTwo": "value_a",
  "fieldThree": 42,
  "createdAt": "2025-01-15T10:30:00.000Z",
  "updatedAt": "2025-01-15T10:30:00.000Z"
}
```

#### Error Responses

| Status | Code | Description |
| --- | --- | --- |
| 401 | `UNAUTHORIZED` | Missing or invalid JWT |
| 403 | `FORBIDDEN` | Resource belongs to a different user |
| 404 | `NOT_FOUND` | No resource with this id |
| 500 | `INTERNAL_ERROR` | Unexpected server error |

---

### GET /api/v1/[resource]

**Description:** List resources with filtering and pagination.
**Auth:** Required
**Rate limit:** Standard

#### Query Parameters

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `page` | `integer` | No | `1` | Page number (1-indexed) |
| `limit` | `integer` | No | `20` | Items per page, max `100` |
| `sortBy` | `string` | No | `createdAt` | Field to sort by |
| `sortOrder` | `asc \ | desc` | No | `desc` | Sort direction |
| `[filterField]` | `string` | No | — | Filter by field value |

#### Success Response — `200 OK`

```json
{
  "data": [ /* array of resource objects */ ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 143,
    "totalPages": 8,
    "hasNextPage": true,
    "hasPreviousPage": false
  }
}
```

#### Error Responses

| Status | Code | Description |
| --- | --- | --- |
| 400 | `VALIDATION_ERROR` | Invalid query parameter value |
| 401 | `UNAUTHORIZED` | Missing or invalid JWT |
| 500 | `INTERNAL_ERROR` | Unexpected server error |

---

### PATCH /api/v1/[resource]/:id

**Description:** Partially update a resource.
**Auth:** Required — resource owner or admin
**Rate limit:** Standard

#### Path Parameters

| Parameter | Type | Description |
| --- | --- | --- |
| `id` | `string (uuid)` | Resource identifier |

#### Request Body

```typescript
const UpdateResourceSchema = z.object({
  fieldOne: z.string().min(1).max(255).optional(),
  fieldTwo: z.enum(['value_a', 'value_b']).optional(),
}).refine(data => Object.keys(data).length > 0, {
  message: 'At least one field must be provided',
})
```

#### Success Response — `200 OK`

Returns the full updated resource object (same shape as GET /:id).

#### Error Responses

| Status | Code | Description |
| --- | --- | --- |
| 400 | `VALIDATION_ERROR` | Body failed validation or is empty |
| 401 | `UNAUTHORIZED` | Missing or invalid JWT |
| 403 | `FORBIDDEN` | Not the resource owner or admin |
| 404 | `NOT_FOUND` | No resource with this id |
| 409 | `CONFLICT` | [Describe any conflict scenario] |
| 500 | `INTERNAL_ERROR` | Unexpected server error |

---

## Shared Types

```typescript
// Common response envelope (all list endpoints)
interface PaginatedResponse<T> {
  data: T[]
  pagination: {
    page: number
    limit: number
    total: number
    totalPages: number
    hasNextPage: boolean
    hasPreviousPage: boolean
  }
}

// Common error envelope
interface ApiError {
  error: {
    code: string
    message: string
    details?: Array<{ field: string; message: string }>
  }
}
```

---

## Implementation Notes

- All endpoints implemented as Next.js Route Handlers in `app/api/v1/[resource]/route.ts`
- Zod schemas defined in `lib/validations/[resource].ts` — same schemas used by both API and Server Actions
- JWT validation via Clerk's `auth()` helper from `@clerk/nextjs/server`
- Database access via Prisma client from `lib/prisma.ts`
- Redis caching applied at the service layer (not the route handler)

---
```
## Output

A single markdown API spec file, typically saved as `/docs/api/[feature-name]-api-spec.md`, or embedded in the relevant feature documentation folder.

## Quality Checks

Before handing off to the Backend Engineer agent, verify:

- [ ] Every endpoint has auth requirements explicitly stated (Required / Public / Guest OK)
- [ ] All 4xx error codes are defined for every endpoint (400, 401, 403, 404 at minimum)
- [ ] Request body schemas are defined using Zod-style TypeScript
- [ ] Response schemas show the exact JSON shape with field names and types
- [ ] Pagination is defined for all list endpoints
- [ ] Rate limiting is addressed
- [ ] Path parameters, query parameters, and body parameters are in separate sections
- [ ] No endpoint lacks a 500 error definition
- [ ] Shared types (PaginatedResponse, ApiError) are documented once, not duplicated

## Example

**Scenario:** API spec for the Game Sessions feature.

**User stories:**
- As a student, I can start a new game session for a specific chapter
- As a student, I can fetch the details of an ongoing session
- As a student, I can mark a session as complete

```markdown
# API Specification: Game Sessions

**Version:** 1.0
**Date:** 2025-01-20
**Status:** approved

---

## Overview

The Game Sessions API manages the lifecycle of a student's gameplay session — from session creation through question delivery to completion and scoring. It is called by the Next.js App Router game interface (`app/(game)/play/[sessionId]`). The primary resource is `GameSession`, which is owned by a student and linked to a Chapter and a set of Questions.

---

## Base URL
```
/api/v1/game-sessions
```
---

## Authentication

All endpoints require Bearer JWT. Guest users (`role: guest`) may create sessions marked `[GUEST OK]` but sessions are not persisted beyond the browser session.

---

## Endpoints

| Method | Path | Auth | Description |
|---|---|---|---|
| POST | `/api/v1/game-sessions` | Required / Guest OK | Start a new game session |
| GET | `/api/v1/game-sessions/:id` | Required / Guest OK | Get session state |
| PATCH | `/api/v1/game-sessions/:id/complete` | Required / Guest OK | Mark session complete and submit score |

---

### POST /api/v1/game-sessions

**Description:** Start a new game session. Returns the session with the first batch of questions pre-loaded. For guests, creates a transient session not persisted to the database (Redis only, 2h TTL).
**Auth:** Required or Guest (session cookie)

#### Request Body

```typescript
const CreateGameSessionSchema = z.object({
  chapterId: z.string().uuid(),
  grade:     z.number().int().min(3).max(8),
  subject:   z.enum(['maths', 'science', 'english']),
  mode:      z.enum(['practice', 'test', 'challenge']).default('practice'),
  questionCount: z.number().int().min(5).max(30).default(10),
})
```

#### Success Response — `201 Created`

```json
{
  "id": "sess_01HZ4K9MNPQR",
  "studentId": "usr_01HZ4ABC",
  "chapterId": "chp_01HZ123",
  "mode": "practice",
  "status": "in_progress",
  "questions": [
    {
      "id": "q_01HZ456",
      "text": "What is the SI unit of force?",
      "options": ["Newton", "Joule", "Watt", "Pascal"],
      "difficulty": "medium",
      "conceptTag": "forces-and-motion"
    }
  ],
  "totalQuestions": 10,
  "currentQuestionIndex": 0,
  "startedAt": "2025-01-20T09:00:00.000Z",
  "expiresAt": "2025-01-20T09:30:00.000Z"
}
```

#### Error Responses

| Status | Code | Description |
| --- | --- | --- |
| 400 | `VALIDATION_ERROR` | Invalid body (e.g. grade out of range) |
| 400 | `INSUFFICIENT_QUESTIONS` | Chapter has fewer questions than `questionCount` |
| 401 | `UNAUTHORIZED` | No JWT and no guest session cookie |
| 403 | `FORBIDDEN` | Student's enrolled grade does not match `grade` param |
| 404 | `CHAPTER_NOT_FOUND` | No chapter with this chapterId |
| 409 | `SESSION_ALREADY_ACTIVE` | Student already has an active session for this chapter |
| 500 | `INTERNAL_ERROR` | Unexpected server error |

---

### GET /api/v1/game-sessions/:id

**Description:** Fetch the current state of a game session including answered questions and score so far. Used to resume an in-progress session.
**Auth:** Required or Guest

#### Path Parameters

| Parameter | Type | Description |
| --- | --- | --- |
| `id` | `string` | Game session ID |

#### Success Response — `200 OK`

```json
{
  "id": "sess_01HZ4K9MNPQR",
  "status": "in_progress",
  "mode": "practice",
  "totalQuestions": 10,
  "currentQuestionIndex": 3,
  "correctCount": 2,
  "incorrectCount": 1,
  "scorePercent": null,
  "questions": [ /* full question array, answered ones include selectedOption */ ],
  "startedAt": "2025-01-20T09:00:00.000Z",
  "expiresAt": "2025-01-20T09:30:00.000Z"
}
```

#### Error Responses

| Status | Code | Description |
| --- | --- | --- |
| 401 | `UNAUTHORIZED` | Missing or invalid JWT / guest cookie |
| 403 | `FORBIDDEN` | Session belongs to a different student |
| 404 | `NOT_FOUND` | No session with this id |
| 500 | `INTERNAL_ERROR` | Unexpected server error |

---

### PATCH /api/v1/game-sessions/:id/complete

**Description:** Submit the completed session. Calculates final score, updates student progress, and persists the result. Idempotent — calling this on an already-completed session returns the existing result without error.
**Auth:** Required or Guest

#### Path Parameters

| Parameter | Type | Description |
| --- | --- | --- |
| `id` | `string` | Game session ID |

#### Request Body

```typescript
const CompleteSessionSchema = z.object({
  answers: z.array(z.object({
    questionId:     z.string().uuid(),
    selectedOption: z.number().int().min(0).max(3),
    timeTakenMs:    z.number().int().min(0).max(120000),
  })),
})
```

#### Success Response — `200 OK`

```json
{
  "id": "sess_01HZ4K9MNPQR",
  "status": "completed",
  "scorePercent": 70.0,
  "correctCount": 7,
  "incorrectCount": 3,
  "timeTakenSeconds": 312,
  "xpEarned": 140,
  "conceptMastery": {
    "forces-and-motion": 0.75,
    "energy-forms": 1.0
  },
  "completedAt": "2025-01-20T09:05:12.000Z"
}
```

#### Error Responses

| Status | Code | Description |
| --- | --- | --- |
| 400 | `VALIDATION_ERROR` | Answers array missing or malformed |
| 400 | `ANSWER_COUNT_MISMATCH` | Number of answers does not match session's question count |
| 401 | `UNAUTHORIZED` | Missing or invalid JWT / guest cookie |
| 403 | `FORBIDDEN` | Session belongs to a different student |
| 404 | `NOT_FOUND` | No session with this id |
| 409 | `SESSION_EXPIRED` | Session TTL has elapsed |
| 500 | `INTERNAL_ERROR` | Unexpected server error |
```
```