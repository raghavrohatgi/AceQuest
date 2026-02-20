# Skill: create-adr

## Purpose

Write an Architecture Decision Record (ADR) when a significant technical decision is made. ADRs capture context, options considered, the decision taken, and consequences. They prevent the same decision from being re-litigated and give future engineers full context on why the codebase is shaped the way it is.

A decision warrants an ADR when it is:
- Costly or difficult to reverse (e.g. choosing a database, auth provider, state management approach)
- Likely to affect multiple engineers or subsystems
- The result of meaningful trade-off analysis between alternatives
- Something a new engineer would otherwise question without context

Trivial decisions (naming a function, choosing an icon library) do not need ADRs.

## Used By

Software Architect Agent

## Inputs

| Input | Type | Description |
| --- | --- | --- |
| `decision_title` | string | Short, noun-phrase title (e.g. "Use Prisma as ORM") |
| `context` | string | The problem or situation forcing a decision |
| `options_considered` | list | At least 2 options, each with a short description |
| `chosen_option` | string | The option selected |
| `rationale` | string | Why this option was chosen over the others |
| `consequences_positive` | list | Benefits and improvements the decision brings |
| `consequences_negative` | list | Trade-offs, costs, and risks accepted |

## Procedure / Template

**Step 1 — Determine the ADR number.**
Look at `/docs/decisions/` and find the highest NNNN prefix. Increment by 1. If no ADRs exist, start at `0001`.

**Step 2 — Create the file.**
Save as `/docs/decisions/NNNN-kebab-case-title.md` (e.g. `0003-use-prisma-as-orm.md`).

**Step 3 — Fill in the MADR template below.**

```markdown
# NNNN — [Decision Title]

**Status:** proposed | accepted | deprecated | superseded by [NNNN]
**Date:** YYYY-MM-DD
**Deciders:** [list of people/agents involved]
**Technical Story:** [ticket/issue reference if applicable]

---

## Context and Problem Statement

[2–4 sentences describing the situation. What problem are we solving? What constraint or opportunity triggered this decision? Be specific — include AceQuest-specific context such as user types (students grades 3–8, parents, guests), scale targets (10K concurrent users), or regulatory context (student data, COPPA-adjacent considerations for Indian minors).]

---

## Decision Drivers

- [Driver 1 — e.g. "Must work within Next.js 14 App Router conventions"]
- [Driver 2 — e.g. "Low operational overhead for a small team"]
- [Driver 3 — e.g. "Must support connection pooling for Vercel serverless environment"]
- [Add as many as are relevant]

---

## Options Considered

### Option A: [Name]
[1–2 sentence description of this option]

**Pros:**
- [Pro 1]
- [Pro 2]

**Cons:**
- [Con 1]
- [Con 2]

---

### Option B: [Name]
[1–2 sentence description of this option]

**Pros:**
- [Pro 1]
- [Pro 2]

**Cons:**
- [Con 1]
- [Con 2]

---

### Option C: [Name] *(if applicable)*
[1–2 sentence description of this option]

**Pros:**
- [Pro 1]

**Cons:**
- [Con 1]

---

## Comparison Table

| Criterion | Option A | Option B | Option C |
|---|---|---|---|
| [Criterion 1] | ✅ / ⚠️ / ❌ | | |
| [Criterion 2] | | | |
| [Criterion 3] | | | |
| [Criterion 4] | | | |

---

## Decision Outcome

**Chosen option:** [Option X], because [one-sentence rationale tying back to decision drivers].

---

## Consequences

### Positive
- [Benefit 1]
- [Benefit 2]

### Negative / Trade-offs
- [Trade-off 1]
- [Trade-off 2]

### Risks and Mitigations
| Risk | Mitigation |
|---|---|
| [Risk 1] | [How we will address it] |
| [Risk 2] | [How we will address it] |

---

## Implementation Notes

[Any notes for the engineer implementing the decision — config snippets, links to docs, things to watch out for.]

---

## References

- [Link 1]
- [Link 2]
```

**Step 4 — Update status.**
When the decision is approved by a human engineer, change `Status: proposed` to `Status: accepted`. When a later ADR supersedes this one, update to `Status: superseded by [NNNN]`.

## Output

A single markdown file at `/docs/decisions/NNNN-kebab-case-title.md`, following the MADR format above, committed to the repository.

## Quality Checks

Before marking the ADR complete, verify all of the following:

- [ ] Decision is specific and irreversible enough to warrant an ADR (not a trivial choice)
- [ ] At least 2 options are considered with explicit pros and cons for each
- [ ] Comparison table covers at least 4 criteria relevant to AceQuest's context
- [ ] Consequences list includes both positive benefits and negative trade-offs (no decision is purely positive)
- [ ] Decision drivers are specific — not generic statements like "it is better"
- [ ] AceQuest-specific context is present (scale, user types, regulatory, cost)
- [ ] Risks and Mitigations table is populated
- [ ] File is named correctly with a sequential NNNN prefix
- [ ] Status is set to `proposed` on creation

## Example

**Scenario:** Choosing between Prisma ORM and raw SQL (node-postgres) for database access.

**File:** `/docs/decisions/0001-use-prisma-as-orm.md`

```markdown
# 0001 — Use Prisma as ORM

**Status:** accepted
**Date:** 2025-01-15
**Deciders:** Raghav Rohatgi, Software Architect Agent
**Technical Story:** Initial tech stack selection

---

## Context and Problem Statement

AceQuest needs a database access layer for PostgreSQL. The team is small (2–3 engineers), working primarily in TypeScript, and will iterate on the schema frequently during the early product phase. We need something that enables fast schema changes, provides type safety end-to-end, and does not require deep PostgreSQL expertise to use safely. The application will eventually serve up to 10K concurrent users, so the solution must be compatible with connection pooling in a serverless/edge deployment (Vercel + Supabase or RDS).

---

## Decision Drivers

- TypeScript-first: type safety from database to API response is a priority
- Fast schema iteration: schema will change frequently in early phases
- Small team: cannot maintain complex raw SQL migrations manually
- Serverless deployment: must work with Vercel serverless functions (connection pooling via PgBouncer or Prisma Accelerate)
- Readable queries: engineers unfamiliar with SQL should still be productive

---

## Options Considered

### Option A: Prisma ORM
Prisma is a TypeScript-first ORM with a declarative schema file, auto-generated type-safe client, and a built-in migration system.

**Pros:**
- Fully typed query builder — TypeScript errors catch schema mismatches at compile time
- Declarative `schema.prisma` file is a single source of truth for the data model
- `prisma migrate dev` handles migration generation and application
- Prisma Studio gives a visual data browser without additional tooling
- Active ecosystem, good Next.js integration

**Cons:**
- Abstraction layer means some complex queries are harder to express than raw SQL
- Prisma Client is not designed for edge runtime without Prisma Accelerate
- Bundle size is non-trivial for serverless cold starts
- Complex aggregations sometimes require `$queryRaw`

---

### Option B: node-postgres (pg) with raw SQL
Direct PostgreSQL driver. Write SQL strings manually, handle migrations with a tool like `db-migrate` or `flyway`.

**Pros:**
- Zero abstraction — full SQL expressiveness
- Lighter bundle size
- No vendor lock-in

**Cons:**
- No type safety without additional code generation (e.g. `pgtyped`)
- Engineers must write and maintain SQL migration files manually
- Higher risk of SQL injection without discipline
- Schema changes require updating TypeScript interfaces separately — drift is common
- Steeper onboarding for engineers not expert in SQL

---

### Option C: Drizzle ORM
A newer lightweight TypeScript ORM that is closer to SQL syntax, with edge-compatible runtime.

**Pros:**
- Excellent edge/serverless performance, smaller bundle
- SQL-like syntax is more familiar to SQL-comfortable developers
- Type-safe

**Cons:**
- Smaller community and ecosystem than Prisma
- Migration tooling less mature
- Less documentation and fewer examples for Next.js App Router specifically
- Team has no prior experience with Drizzle

---

## Comparison Table

| Criterion | Prisma | raw pg | Drizzle |
|---|---|---|---|
| TypeScript type safety | ✅ Auto-generated | ⚠️ Manual via pgtyped | ✅ Schema-defined |
| Migration tooling | ✅ Built-in | ⚠️ Separate tool | ⚠️ Less mature |
| Serverless / Vercel support | ⚠️ Needs Accelerate | ✅ Native | ✅ Native |
| Team familiarity | ✅ High | ⚠️ Medium | ❌ Low |
| Schema-as-code | ✅ schema.prisma | ❌ No | ✅ TypeScript schema |
| Complex query support | ⚠️ $queryRaw fallback | ✅ Full SQL | ✅ SQL-like |

---

## Decision Outcome

**Chosen option:** Prisma ORM, because it provides TypeScript-first type safety and a built-in migration system that matches the small team's need for fast, safe schema iteration without deep SQL expertise.

---

## Consequences

### Positive
- Schema changes are captured in version-controlled `schema.prisma` — the entire team reads one file to understand the data model
- TypeScript compilation catches query/schema mismatches before they reach production
- `prisma migrate dev` makes local development frictionless
- Prisma Studio available for quick data inspection during development

### Negative / Trade-offs
- Complex aggregations (e.g. rolling performance averages across StudentGameSession) require dropping down to `$queryRaw` — these must be reviewed carefully for SQL injection
- Prisma Client adds ~500KB to serverless bundle; must use Prisma Accelerate or connection pooling proxy if deploying to Vercel edge functions
- Prisma abstractions can make query performance less obvious — need `queryEvent` logging in development to catch slow queries

### Risks and Mitigations
| Risk | Mitigation |
|---|---|
| Cold start latency on Vercel serverless | Use Prisma Accelerate or PgBouncer; singleton client pattern in Next.js |
| N+1 queries from inexperienced use | Code review checklist item; `optimise-query` skill documents patterns |
| `$queryRaw` SQL injection | Parameterised queries only; lint rule to flag template literal `$queryRaw` |

---

## Implementation Notes

Use the singleton pattern to prevent multiple Prisma Client instances in Next.js hot-reload:

```typescript
// lib/prisma.ts
import { PrismaClient } from '@prisma/client'

const globalForPrisma = globalThis as unknown as { prisma: PrismaClient }

export const prisma =
  globalForPrisma.prisma ??
  new PrismaClient({
    log: process.env.NODE_ENV === 'development' ? ['query', 'error', 'warn'] : ['error'],
  })

if (process.env.NODE_ENV !== 'production') globalForPrisma.prisma = prisma
```

Add `DATABASE_URL` and `DIRECT_URL` to `.env` when using Prisma Accelerate:
```
DATABASE_URL="prisma://accelerate.prisma-data.net/?api_key=..."
DIRECT_URL="postgresql://user:pass@host:5432/acequest"
```

In `schema.prisma`:
```prisma
datasource db {
  provider  = "postgresql"
  url       = env("DATABASE_URL")
  directUrl = env("DIRECT_URL")
}
```

---

## References

- [Prisma Docs — Next.js](https://www.prisma.io/docs/orm/more/help-and-troubleshooting/nextjs-help)
- [Prisma Accelerate](https://www.prisma.io/data-platform/accelerate)
- [MADR Template](https://adr.github.io/madr/)
```
```