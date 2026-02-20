# Engineering Skills Library

Reusable, step-by-step procedures for AceQuest's engineering agents. Each skill tells an agent exactly *how* to perform a specific task using the AceQuest tech stack.

**Skills are the "how" — agents are the "who".**

---

## Tech Stack Reference

| Layer | Technology |
| --- | --- |
| Frontend | React / Next.js 14+, TypeScript (strict), Tailwind CSS |
| State | React Query (server), Zustand (UI), React Hook Form (forms) |
| Validation | Zod (frontend + backend) |
| Backend | Node.js 20+ LTS, Express.js, TypeScript |
| ORM | Prisma |
| Database | PostgreSQL 15+ |
| Cache | Redis |
| Auth | Auth0 / Clerk |
| Storage | AWS S3 |
| Email | SendGrid |
| Analytics | Mixpanel |
| Testing (FE) | Vitest + React Testing Library + Playwright |
| AI/ML | Python, scikit-learn, TensorFlow/PyTorch (if needed) |
| Design | Figma |

---

## Skill Index

### Architect (`/architect/`)
| Skill | Purpose |
| --- | --- |
| [create-adr.md](./architect/create-adr.md) | Write an Architecture Decision Record |
| [design-api-spec.md](./architect/design-api-spec.md) | Design a RESTful API specification |
| [design-system-architecture.md](./architect/design-system-architecture.md) | Produce a system architecture document |
| [evaluate-tech-stack.md](./architect/evaluate-tech-stack.md) | Compare and choose between technology options |
| [plan-db-schema.md](./architect/plan-db-schema.md) | High-level entity and relationship planning |

### Frontend (`/frontend/`)
| Skill | Purpose |
| --- | --- |
| [create-react-component.md](./frontend/create-react-component.md) | Full component lifecycle: props → implementation → test → Storybook |
| [implement-responsive-layout.md](./frontend/implement-responsive-layout.md) | Mobile-first responsive layout with Tailwind |
| [add-form-with-validation.md](./frontend/add-form-with-validation.md) | React Hook Form + Zod form with error states |
| [optimise-performance.md](./frontend/optimise-performance.md) | Performance optimisation checklist |
| [implement-accessibility.md](./frontend/implement-accessibility.md) | WCAG 2.1 AA implementation guide |

### Backend (`/backend/`)
| Skill | Purpose |
| --- | --- |
| [create-api-endpoint.md](./backend/create-api-endpoint.md) | Route → validation → service → error handling → logging → test |
| [implement-auth-middleware.md](./backend/implement-auth-middleware.md) | JWT verification + role-based access control |
| [add-rate-limiting.md](./backend/add-rate-limiting.md) | Per-route, per-user, per-IP rate limiting with Redis |
| [write-service-layer.md](./backend/write-service-layer.md) | Business logic separation from routes |
| [integrate-third-party.md](./backend/integrate-third-party.md) | External API integration pattern (SendGrid, S3, Mixpanel) |

### Database (`/database/`)
| Skill | Purpose |
| --- | --- |
| [design-prisma-schema.md](./database/design-prisma-schema.md) | Prisma model design with relations, constraints, indexes |
| [write-migration.md](./database/write-migration.md) | Safe migration procedure: schema → SQL review → staging → production |
| [optimise-query.md](./database/optimise-query.md) | Query performance: N+1 fix, indexes, caching, EXPLAIN ANALYSE |
| [seed-database.md](./database/seed-database.md) | Dev/test seeding scripts with deterministic data |
| [design-indexes.md](./database/design-indexes.md) | Index strategy: when to index, composite, partial, monitoring |

### QA (`/qa/`)
| Skill | Purpose |
| --- | --- |
| [write-test-plan.md](./qa/write-test-plan.md) | Test plan template: scope, types, environments, risks |
| [write-unit-test.md](./qa/write-unit-test.md) | Vitest unit test pattern: arrange/act/assert, mocking |
| [write-e2e-test.md](./qa/write-e2e-test.md) | Playwright E2E test with page objects |
| [write-bug-report.md](./qa/write-bug-report.md) | Bug report template with severity and reproduction steps |
| [accessibility-audit.md](./qa/accessibility-audit.md) | WCAG 2.1 AA audit: automated + manual checklist |

### UI/UX (`/ui-ux/`)
| Skill | Purpose |
| --- | --- |
| [create-user-flow.md](./ui-ux/create-user-flow.md) | User flow mapping with Mermaid diagram format |
| [write-design-spec.md](./ui-ux/write-design-spec.md) | Component design specification with states and tokens |
| [conduct-usability-test.md](./ui-ux/conduct-usability-test.md) | Usability test script and synthesis framework |
| [design-for-age-band.md](./ui-ux/design-for-age-band.md) | Age-differentiated design rules (Grades 3-5 vs 6-8) |
| [create-design-system-component.md](./ui-ux/create-design-system-component.md) | Adding a new component to the design system |

### AI/ML (`/ai-ml/`)
| Skill | Purpose |
| --- | --- |
| [design-adaptive-algorithm.md](./ai-ml/design-adaptive-algorithm.md) | Adaptive difficulty algorithm: inputs, state machine, pseudocode |
| [implement-irt-model.md](./ai-ml/implement-irt-model.md) | Item Response Theory implementation guide |
| [build-recommendation-engine.md](./ai-ml/build-recommendation-engine.md) | Next-assessment recommendation logic |
| [calculate-skill-mastery.md](./ai-ml/calculate-skill-mastery.md) | Skill mastery scoring with decay and confidence |
| [design-ab-test.md](./ai-ml/design-ab-test.md) | A/B test design for algorithm variants |
| [evaluate-model.md](./ai-ml/evaluate-model.md) | Model evaluation: metrics, bias checks, fairness |

---

## Skill File Format

```markdown
# Skill: [skill-name]

## Purpose
## Used By
## Inputs
## Procedure / Template / Prompt
## Output
## Quality Checks
## Example
```
