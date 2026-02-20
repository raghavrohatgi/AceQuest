# Skill: write-test-plan

## Purpose

Write a structured test plan for a feature before testing begins. A test plan defines the scope of testing, the types of tests needed, the environments tests will run in, entry and exit criteria, risk areas, and a schedule. It is written before any test cases are created and serves as the shared contract between the QA Engineer Agent, the Frontend/Backend Engineer Agents, and the Architect Agent.

A test plan answers three questions: **What will we test? How will we test it? What must be true before we ship?**

## Used By

QA Engineer Agent

## Inputs

| Input | Type | Description |
| --- | --- | --- |
| `feature_name` | string | Kebab-case name of the feature (e.g. `game-session`, `parent-dashboard`) |
| `user_stories` | list | Each story in "As a [user type], I want to [action] so that [outcome]" format |
| `user_types_involved` | list | One or more of: `student`, `parent`, `teacher`, `guest` |
| `known_risk_areas` | list | Parts of the feature that are complex, uncertain, or involve sensitive data |

## Procedure / Template

**Step 1 — Determine the document path.**
Save to `/docs/qa/test-plan-[feature-name].md`. If the `/docs/qa/` directory does not exist, create it.

**Step 2 — Fill in the template below.**

```markdown
# Test Plan: [Feature Name]

**Version:** 1.0
**Date:** YYYY-MM-DD
**Author:** QA Engineer Agent
**Feature Owner:** [Frontend/Backend/Full-stack Engineer Agent]
**Status:** Draft | In Review | Approved

---

## 1. Overview

[2–4 sentences describing what is being tested. Explain the feature's purpose in plain language, who uses it, and what it enables them to do. Include AceQuest-specific context: which grade bands are affected, whether student data is involved, and whether this is a new feature or a change to an existing one.]

---

## 2. Scope

### 2.1 In Scope

- [List every capability, screen, or user action that will be tested]
- [Be specific — "Student can submit an MCQ answer and see correct/incorrect feedback" not just "MCQ answers"]

### 2.2 Out of Scope

- [List what will NOT be tested and why — e.g. "Payment flows — covered by a separate test plan", "Admin portal — not part of this release"]

---

## 3. User Types

| User Type | Role in This Feature | Priority |
|---|---|---|
| Student | [describe] | High / Medium / Low |
| Parent | [describe or "N/A"] | High / Medium / Low |
| Teacher | [describe or "N/A"] | High / Medium / Low |
| Guest | [describe or "N/A"] | High / Medium / Low |

Every user type listed as High or Medium must have at least one test case.

---

## 4. Test Environments

| Environment | URL / Access | Purpose | Data State |
|---|---|---|---|
| Local (dev) | `http://localhost:3000` | Unit and integration tests | Seeded test data |
| Staging | `https://staging.acequest.in` | E2E tests, exploratory testing | Anonymised copy of production |
| Production | `https://acequest.in` | Smoke tests after deploy only | Live data — read-only |

**Test data strategy:** All test accounts created in staging use the prefix `test-` (e.g. `test-student-grade5@acequest.in`). Test data is created via API in `beforeAll` hooks and deleted in `afterAll` hooks. No manual test data in staging.

---

## 5. Test Types and Coverage Targets

| Test Type | Tool | Coverage Target | Who Writes It |
|---|---|---|---|
| Unit | Vitest + React Testing Library | 60% of test effort; 90%+ on business logic functions | QA Engineer Agent |
| Integration | Vitest + Supertest | 30% of test effort; all API endpoints covered | QA Engineer Agent |
| End-to-End | Playwright | 10% of test effort; all critical user journeys | QA Engineer Agent |
| Exploratory | Manual (QA Agent guided) | All risk areas explored | QA Engineer Agent |
| Accessibility | axe-core + manual VoiceOver | All screens meet WCAG 2.1 AA | QA Engineer Agent |
| Performance | Lighthouse CI | Core Web Vitals: LCP <2.5s, CLS <0.1 | Frontend Engineer Agent |

---

## 6. Test Cases Summary

| ID | Description | Type | Priority | Status |
|---|---|---|---|---|
| TC-001 | [Description of test case] | Unit / Integration / E2E | P0 / P1 / P2 / P3 | Not Started |
| TC-002 | [Description of test case] | Unit / Integration / E2E | P0 / P1 / P2 / P3 | Not Started |

*Full test cases are in the individual test files. This table is the summary view for tracking.*

---

## 7. Entry Criteria

Testing begins only when ALL of the following are true:

- [ ] Feature is deployed to staging environment
- [ ] All P0 and P1 bugs from the previous release are resolved
- [ ] Unit tests for the feature pass in CI (0 failures)
- [ ] API endpoints are documented and available in Postman/OpenAPI spec
- [ ] Test data seeding script is ready and verified
- [ ] Design spec is available for visual verification

---

## 8. Exit Criteria

Testing is complete and the feature is approved for production release when ALL of the following are true:

- [ ] All P0 bugs are resolved and re-verified
- [ ] All P1 bugs are resolved or have an approved workaround
- [ ] Unit test coverage ≥ 90% on business logic, ≥ 70% on UI components
- [ ] All E2E tests pass in CI against staging
- [ ] 0 axe-core accessibility violations
- [ ] Lighthouse performance score ≥ 90 on mobile (staging)
- [ ] All user types listed as High priority have at least one passing E2E test
- [ ] Test plan is updated with final status for each test case

---

## 9. Risk Areas and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| [Risk description] | High / Medium / Low | High / Medium / Low | [Specific mitigation action] |
| Student data not saved on session timeout | Medium | High | Test explicit session timeout scenario; verify DB write on partial completion |
| Offline/flaky network on student device | High | Medium | Test with Chrome DevTools network throttling; add offline state handling |
| [Add risk areas specific to this feature] | | | |

---

## 10. Bug Severity Matrix

| Severity | Label | Definition | Release Impact |
|---|---|---|---|
| P0 | Blocker | Data loss, security vulnerability, or blocks ALL users from using the feature | Blocks release. Fix immediately. |
| P1 | Critical | Core feature broken for most users; no acceptable workaround | Blocks release unless approved exception. |
| P2 | Major | Feature works but produces incorrect results for some users, or UX is significantly degraded | Must fix in the next sprint. Does not block release if P0/P1 are clear. |
| P3 | Minor | Visual or cosmetic issue; no functional impact | Logged for backlog. Does not block release. |

---

## 11. Schedule

| Milestone | Target Date | Owner |
|---|---|---|
| Test plan approved | YYYY-MM-DD | QA Engineer Agent |
| Unit and integration tests written | YYYY-MM-DD | QA Engineer Agent |
| E2E tests written | YYYY-MM-DD | QA Engineer Agent |
| Exploratory testing on staging | YYYY-MM-DD | QA Engineer Agent |
| Accessibility audit complete | YYYY-MM-DD | QA Engineer Agent |
| All exit criteria met | YYYY-MM-DD | QA Engineer Agent |
| Feature approved for production | YYYY-MM-DD | Feature Owner |

---

## 12. Assumptions and Dependencies

- [e.g. "Auth0 authentication is working on staging"]
- [e.g. "Question bank API returns data in the correct format"]
- [e.g. "Staging database has at least 50 questions per subject/grade combination"]
```

**Step 3 — Review the plan against quality checks before sharing.**

## Output

A single markdown file at `/docs/qa/test-plan-[feature-name].md`.

## Quality Checks

Before marking the test plan complete, verify all of the following:

- [ ] Exit criteria are measurable and objective — "0 P0 bugs" not "all bugs fixed"
- [ ] Risk areas include at least one item covering student data safety (data loss, incorrect save, privacy)
- [ ] Every user type listed as High or Medium priority has at least one test case in Section 6
- [ ] P0 bugs are explicitly stated to block release
- [ ] Coverage targets are specified numerically per test type
- [ ] Entry criteria include staging deployment — tests do not start on a feature that isn't deployed
- [ ] Exit criteria include accessibility (axe violations = 0)
- [ ] Schedule has a realistic date for each milestone (not all on the same day)
- [ ] Out of scope items are explicit so there is no ambiguity about what this plan does not cover

## Example

**Scenario:** Test plan for the Game Session feature.

**Feature overview:** Students in Grades 3–8 select a subject and game type, answer a series of MCQ questions, and see their results (score, XP earned, skill progress) at the end.

**User types involved:** Student (primary). Parent can view session results in the Parent Dashboard (separate feature, out of scope here).

**Known risk areas:**
- Student session data (answers, score, XP earned) not saved correctly when the app crashes or the student closes the browser mid-game
- XP calculation double-counting if a student submits the same answer twice due to network retry
- Session timer running out on the last question — answers submitted in the final second may not be recorded

**Example test cases table (Section 6 extract):**

| ID | Description | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| TC-001 | Student can start a Fractions game from the Math subject screen | E2E | P0 | Not Started |
| TC-002 | Each question in the session returns a new, non-repeated question | Unit | P1 | Not Started |
| TC-003 | Correct answer increments score by the configured points value | Unit | P0 | Not Started |
| TC-004 | Session results (score, XP, time) are persisted to DB after session ends | Integration | P0 | Not Started |
| TC-005 | Session data is saved when student closes browser mid-game (beforeunload) | Integration | P0 | Not Started |
| TC-006 | XP is not double-counted on network retry of answer submission | Integration | P0 | Not Started |
| TC-007 | Student cannot submit an answer after the timer reaches 0 | Unit | P1 | Not Started |
| TC-008 | Results screen shows correct score, XP earned, and grade | E2E | P1 | Not Started |
| TC-009 | Game play screen has 0 axe-core accessibility violations | E2E | P1 | Not Started |
| TC-010 | Game session screen is usable with keyboard-only navigation | Manual | P1 | Not Started |

**Key exit criterion for this plan:** The student data-loss scenario (TC-005) must pass before release. If a student plays 10 questions and closes the browser after question 9, the system must record their progress up to and including question 9.
