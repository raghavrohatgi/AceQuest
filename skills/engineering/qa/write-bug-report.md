# Skill: Write Bug Report

## Purpose
Define the standard template and procedure for filing actionable bug reports in AceQuest's issue tracker. A good bug report enables any engineer to reproduce the issue independently, understand its severity/impact on K-8 students, and prioritise it correctly without needing to follow up with the reporter.

## Used By
- QA Agent
- Any Engineer who discovers a defect
- Support Agent (escalating user-reported issues)

## Inputs
| Field | Type | Description |
|-------|------|-------------|
| `title` | string | Short, specific description of the defect |
| `severity` | `"P0" \| "P1" \| "P2" \| "P3"` | Impact level (see priority matrix below) |
| `component` | string | Affected area: `frontend/quiz`, `backend/auth`, `adaptive-engine`, etc. |
| `environment` | string | Where the bug was observed: `production`, `staging`, `local` |
| `reproducibilityRate` | string | `"Always" \| "Intermittent (X/10)" \| "Once"` |
| `affectedUsers` | string | Description of who is impacted, e.g. "All Grade 3 students in Hindi quizzes" |

## Priority Matrix

| Priority | Criteria | Example | SLA |
|----------|----------|---------|-----|
| P0 — Critical | Data loss, security breach, all users blocked | Login broken for all students | Fix in 2 hours |
| P1 — High | Core feature broken for a user segment | Quiz submission failing for Grade 5 | Fix in 24 hours |
| P2 — Medium | Feature degraded but workaround exists | Badge not awarded after 100% score | Fix in 1 sprint |
| P3 — Low | Minor cosmetic or edge case | XP counter animation stutters on iOS 14 | Fix when bandwidth allows |

## Procedure / Template

### Bug Report Template

---

**Title:** [Component] Short description of the defect

**Priority:** P{0-3}
**Severity:** {Critical / High / Medium / Low}
**Component:** {frontend/quiz | backend/auth | adaptive-engine | database | payments}
**Environment:** {Production / Staging / Local}
**Reproducibility:** {Always | Intermittent (X/10) | Once}

---

### Summary
One paragraph explaining what is broken, what was expected, and who is affected.

---

### Steps to Reproduce
1. Log in as a Grade 5 student (`student.g5.1@acequest.in` / `AceQuest@dev123`)
2. Navigate to `/quiz/3f7a1b2c-...`
3. Answer all 10 questions
4. Click "Submit Quiz"
5. Observe the result

---

### Actual Behaviour
The quiz submission spinner appears indefinitely. No score, XP, or badge is shown. The network tab shows a `500 Internal Server Error` from `POST /api/v1/quizzes/:id/submit`.

---

### Expected Behaviour
The results page should load within 3 seconds showing:
- Score percentage
- XP awarded
- Any badges unlocked

---

### Evidence
- **Screenshot / Video:** `[attach file]`
- **Network request/response:**
```json
POST /api/v1/quizzes/3f7a1b2c/submit
Status: 500
Response:
{
  "success": false,
  "meta": { "code": "INTERNAL_ERROR" },
  "timestamp": "2025-06-01T10:30:00Z"
}
```
- **Browser console errors:**
```
TypeError: Cannot read properties of undefined (reading 'correctCount')
    at QuizService.gradeAnswers (quiz.service.ts:87)
```
- **Server logs (if accessible):**
```
[ERROR] 2025-06-01T10:30:00Z quiz.submitted — TypeError: Cannot read properties of undefined
  at QuizService.gradeAnswers (/app/src/services/quiz.service.ts:87:30)
  studentId: student-uuid-123
  quizId: 3f7a1b2c-...
```

---

### Environment Details
- **Browser / OS:** Chrome 124 on Android 13 (Pixel 6a)
- **App version / commit:** v2.3.1 / `abc1234`
- **User account:** `student.g5.1@acequest.in`
- **Quiz ID:** `3f7a1b2c-1234-5678-abcd-ef0123456789`
- **Session ID:** `a1b2c3d4-0000-1111-2222-333344445555`

---

### Root Cause Hypothesis (if known)
The `gradeAnswers` method at line 87 dereferences `question.options` without checking if `options` is included in the Prisma query. When `questions` are fetched without `include: { options: true }`, `options` is `undefined`.

---

### Impact Assessment
- **Users affected:** All students attempting to submit any quiz
- **Data integrity:** No submissions saved during the outage period
- **Revenue impact:** Subscription renewals blocked if parents can't see progress
- **Workaround:** None available to users

---

### Acceptance Criteria for Fix
- [ ] `POST /api/v1/quizzes/:id/submit` returns `200` with score, XP, and badges
- [ ] Unit test added: `QuizService.gradeAnswers` handles questions array from Prisma include
- [ ] No regression on existing submission tests
- [ ] Fix deployed and verified on staging before production push

---

## Example Reports by Category

### Frontend Rendering Bug (P2)

```markdown
**Title:** [frontend/leaderboard] XP totals displayed in incorrect locale format (commas vs Indian numbering)

**Priority:** P2
**Component:** frontend/leaderboard
**Environment:** Production

**Summary:** XP values > 10,000 are formatted as "10,000" using Western numbering instead of "10,000" 
(same in this case) but values > 100,000 show as "100,000" instead of "1,00,000" 
per the Indian numbering system expected by our users.

**Steps to Reproduce:**
1. Log in as a student with > 1,00,000 XP
2. View the leaderboard

**Actual:** 100,000 XP
**Expected:** 1,00,000 XP

**Fix hint:** Use `number.toLocaleString("en-IN")` not `toLocaleString("en-US")`
```

### Performance Bug (P2)

```markdown
**Title:** [backend/leaderboard] Grade 5 leaderboard API takes >3s on production

**Priority:** P2 (degrades to P1 if > 5s)
**Component:** backend/leaderboard
**Environment:** Production

**Evidence:**
- Datadog APM: p99 latency = 3.8 s for GET /api/v1/leaderboard?gradeLevel=5
- Explain analyze: Seq Scan on 85,000 students rows — missing index on gradeLevel+totalXP

**Acceptance Criteria:**
- [ ] p99 < 500 ms after composite index added
- [ ] Index created CONCURRENTLY to avoid downtime
```

## Output
- Filled bug report filed in GitHub Issues (or Linear/Jira per team convention)
- Labels applied: `bug`, `priority:P{n}`, `component:<name>`
- Assigned to responsible engineer or team
- Linked to any related E2E test that should detect this regression

## Quality Checks
- [ ] Title follows `[component] short description` format
- [ ] Steps to reproduce are numbered and reproducible by anyone on the team
- [ ] Actual vs Expected clearly distinguished
- [ ] Evidence attached: screenshot, network request/response, logs
- [ ] Root cause hypothesis included where known
- [ ] Acceptance criteria defined so the engineer knows when the fix is complete
- [ ] Severity and affected user count documented for prioritisation
- [ ] No personally identifiable student data (PII) in the report — use anonymised IDs
