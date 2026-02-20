---
planStatus:
  planId: plan-engineering-skills
  title: Engineering Agent Skills Library
  status: draft
  planType: initiative
  priority: high
  owner: raghavrohatgi
  stakeholders: []
  tags:
    - engineering
    - skills
    - agents
    - frontend
    - backend
    - database
    - qa
    - ai-ml
    - architecture
  created: "2026-02-18"
  updated: "2026-02-18T00:00:00.000Z"
  progress: 0
---

# Engineering Agent Skills Library

> **Goal:** Create a comprehensive skills library for all 7 engineering agents in `/agents/engineering/`. Skills live in `/skills/engineering/` and give each agent reusable, step-by-step procedures for their most common tasks.

---

## Context

We already have `/skills/content-creators/` with 12 skills for the content pipeline. We now apply the same pattern to the engineering team. Each engineering agent has a defined role, tech stack, and deliverable type — skills codify exactly *how* to do each task.

---

## Skills to Create

### 1. Software Architect — `/skills/engineering/architect/`

| Skill | Purpose |
|---|---|
| `create-adr` | Write an Architecture Decision Record for a tech choice (format, template, decision criteria) |
| `design-api-spec` | Design a RESTful API specification (endpoints, request/response schemas, error codes, versioning) |
| `design-system-architecture` | Produce a system architecture document (components, data flow, infra diagram spec, scalability notes) |
| `evaluate-tech-stack` | Framework for evaluating and choosing between two technology options (comparison table, trade-offs, recommendation) |
| `plan-db-schema` | High-level data model planning (entities, relationships, cardinality — before handing to Database Engineer) |

---

### 2. Frontend Engineer — `/skills/engineering/frontend/`

| Skill | Purpose |
|---|---|
| `create-react-component` | Step-by-step process: TypeScript props interface → component implementation → Tailwind styling → accessibility → unit test → Storybook story |
| `implement-responsive-layout` | Responsive layout pattern using Tailwind breakpoints, mobile-first approach, grid/flex rules |
| `add-form-with-validation` | React Hook Form + Zod schema → form component → error states → submission handling |
| `optimise-performance` | Checklist: code splitting, lazy loading, React.memo, bundle analysis, image optimisation |
| `implement-accessibility` | WCAG 2.1 AA implementation guide: ARIA attributes, keyboard navigation, focus management, colour contrast checks |

---

### 3. Backend Engineer — `/skills/engineering/backend/`

| Skill | Purpose |
|---|---|
| `create-api-endpoint` | Full flow: route definition → Zod validation → service layer → error handling → Winston logging → test |
| `implement-auth-middleware` | Auth0/Clerk JWT verification middleware, role-based access control (student / parent / teacher / admin) |
| `add-rate-limiting` | Rate limiting setup per route, per user, per IP — with Redis backing |
| `write-service-layer` | Business logic separation from routes: service class pattern, dependency injection, error types |
| `integrate-third-party` | Template for integrating external APIs (SendGrid, S3, Mixpanel): client setup → wrapper → error handling → retry logic |

---

### 4. Database Engineer — `/skills/engineering/database/`

| Skill | Purpose |
|---|---|
| `design-prisma-schema` | Writing Prisma models: field types, relations, constraints, indexes, cascade rules |
| `write-migration` | Safe Prisma migration procedure: schema change → generate → review SQL → test on staging → apply |
| `optimise-query` | Query performance checklist: identify N+1, add indexes, use `select` projections, implement Redis cache, measure with EXPLAIN ANALYSE |
| `seed-database` | Database seeding script pattern for dev/test environments: deterministic data, foreign key ordering |
| `design-indexes` | Index design guide: when to index, composite indexes, partial indexes, index monitoring |

---

### 5. QA Engineer — `/skills/engineering/qa/`

| Skill | Purpose |
|---|---|
| `write-test-plan` | Template: scope, test types, environments, entry/exit criteria, risk areas, schedule |
| `write-unit-test` | Vitest unit test pattern: arrange/act/assert, mocking, edge cases, coverage targets |
| `write-e2e-test` | Playwright E2E test pattern: page objects, selectors, assertions, CI integration |
| `write-bug-report` | Bug report template: title, severity, steps to reproduce, expected vs actual, environment, attachments |
| `accessibility-audit` | WCAG 2.1 AA audit checklist: automated (axe-core), keyboard navigation, screen reader, colour contrast, touch targets |

---

### 6. UI/UX Engineer — `/skills/engineering/ui-ux/`

| Skill | Purpose |
|---|---|
| `create-user-flow` | Step-by-step user flow mapping: entry points, decision nodes, screens, exit points, Mermaid diagram format |
| `write-design-spec` | Design specification document: component anatomy, states (default/hover/active/disabled/error), spacing, colour, typography |
| `conduct-usability-test` | Usability test script template: tasks, observation guide, metrics to capture, synthesis framework |
| `design-for-age-band` | Age-differentiated design rules: Grade 3-5 vs Grade 6-8, touch targets, reading level, colour usage, icon complexity |
| `create-design-system-component` | Adding a new component to the design system: design tokens, variants, accessibility spec, usage do/don't |

---

### 7. AI/ML Engineer — `/skills/engineering/ai-ml/`

| Skill | Purpose |
|---|---|
| `design-adaptive-algorithm` | Document an adaptive difficulty algorithm: inputs, state machine, decision logic, pseudocode, edge cases |
| `implement-irt-model` | Item Response Theory implementation guide: 1PL/2PL/3PL model selection, parameter estimation, ability scoring |
| `build-recommendation-engine` | Next-assessment recommendation logic: skill graph, prerequisite validation, difficulty matching, diversity injection |
| `calculate-skill-mastery` | Skill mastery calculation: rolling window, threshold logic, confidence intervals, decay over time |
| `design-ab-test` | A/B test design for algorithm variants: hypothesis, sample size, metrics, success criteria, guardrail metrics |
| `evaluate-model` | Model evaluation framework: train/test split, metrics (MAE, accuracy, AUC), bias checks, demographic fairness |

---

## Directory Structure After Creation

```
/skills/
├── content-creators/          ← already done (12 skills)
│   ├── README.md
│   ├── pdf-to-markdown.md
│   ├── chapter-ingest.md
│   └── ... (10 more)
│
└── engineering/
    ├── README.md              ← index + skill format guide
    ├── architect/
    │   ├── create-adr.md
    │   ├── design-api-spec.md
    │   ├── design-system-architecture.md
    │   ├── evaluate-tech-stack.md
    │   └── plan-db-schema.md
    ├── frontend/
    │   ├── create-react-component.md
    │   ├── implement-responsive-layout.md
    │   ├── add-form-with-validation.md
    │   ├── optimise-performance.md
    │   └── implement-accessibility.md
    ├── backend/
    │   ├── create-api-endpoint.md
    │   ├── implement-auth-middleware.md
    │   ├── add-rate-limiting.md
    │   ├── write-service-layer.md
    │   └── integrate-third-party.md
    ├── database/
    │   ├── design-prisma-schema.md
    │   ├── write-migration.md
    │   ├── optimise-query.md
    │   ├── seed-database.md
    │   └── design-indexes.md
    ├── qa/
    │   ├── write-test-plan.md
    │   ├── write-unit-test.md
    │   ├── write-e2e-test.md
    │   ├── write-bug-report.md
    │   └── accessibility-audit.md
    ├── ui-ux/
    │   ├── create-user-flow.md
    │   ├── write-design-spec.md
    │   ├── conduct-usability-test.md
    │   ├── design-for-age-band.md
    │   └── create-design-system-component.md
    └── ai-ml/
        ├── design-adaptive-algorithm.md
        ├── implement-irt-model.md
        ├── build-recommendation-engine.md
        ├── calculate-skill-mastery.md
        ├── design-ab-test.md
        └── evaluate-model.md
```

**Total: 36 skill files + 1 README = 37 files**

---

## Skill File Format

Every skill follows the same structure (matching the content-creators pattern):

```markdown
# Skill: [skill-name]

## Purpose
What this skill does and why it exists.

## Used By
Which agent(s) invoke this skill.

## Inputs
What information must be provided.

## Procedure / Prompt / Template
The exact steps, prompt text, or template.

## Output
What the skill produces (file, schema, document).

## Quality Checks
How to verify the skill ran correctly.

## Example
A worked example showing inputs → outputs.
```

---

## Priority Order for Creation

| Priority | Agent | Skills | Why |
|---|---|---|---|
| 🔴 P0 | **Backend** | `create-api-endpoint`, `write-service-layer`, `implement-auth-middleware` | Unblocks all API development |
| 🔴 P0 | **Database** | `design-prisma-schema`, `write-migration`, `optimise-query` | Unblocks data layer |
| 🔴 P0 | **Frontend** | `create-react-component`, `add-form-with-validation` | Unblocks UI build |
| 🟡 P1 | **QA** | `write-unit-test`, `write-e2e-test`, `write-bug-report` | Needed once building starts |
| 🟡 P1 | **AI/ML** | `design-adaptive-algorithm`, `implement-irt-model`, `calculate-skill-mastery` | Needed for the core diagnostic engine |
| 🟡 P1 | **Architect** | `create-adr`, `design-api-spec`, `design-system-architecture` | Guides all engineering decisions |
| 🟢 P2 | **UI/UX** | All 5 | Supplement existing mockup workflow |
| 🟢 P2 | **Frontend** | `implement-accessibility`, `optimise-performance` | Polish after core is built |

---

## Notes

- Each skill should include the actual AceQuest tech stack (React/Next.js, Node/Express, PostgreSQL/Prisma, Vitest/Playwright) — not generic templates
- Skills should cross-reference each other where relevant (e.g. `create-api-endpoint` references `design-prisma-schema`)
- The AI/ML skills are unique — they produce algorithms and pseudocode, not just code patterns
- Skills for the AI/ML agent should reference the IRT and adaptive learning goals from the agent definition

---

## Related Documents

- [`agents/engineering/`](../agents/engineering/) — the 7 agent definitions these skills serve
- [`skills/content-creators/README.md`](../skills/content-creators/README.md) — pattern to follow
- [`engineering-standards/`](../engineering-standards/) — existing frontend/backend standards to incorporate into skills
