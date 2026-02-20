# Skill: Accessibility Audit

## Purpose
Define a repeatable accessibility audit procedure for AceQuest's UI, targeting WCAG 2.1 Level AA compliance. K-8 students may use screen readers, keyboard navigation, or switch access devices. Audit combines automated scanning (axe-core, Lighthouse), manual keyboard testing, and screen reader testing (NVDA/VoiceOver) to surface violations that automated tools miss.

## Used By
- QA Accessibility Auditor Agent
- Frontend Engineer Agent
- UI/UX Agent

## Inputs
| Field | Type | Description |
|-------|------|-------------|
| `pages` | string[] | Pages/routes to audit, e.g. `["/login", "/dashboard", "/quiz/:id"]` |
| `components` | string[] | Specific components to audit in isolation |
| `persona` | string | Disability profile, e.g. "Grade 4 student, blind, uses NVDA + Chrome" |
| `targetCriteria` | string[] | WCAG success criteria to focus on, e.g. `["1.4.3", "2.1.1", "4.1.2"]` |

## WCAG 2.1 AA Criteria Reference (Most Relevant to AceQuest)

| Criterion | Level | Description | Common Failure |
|-----------|-------|-------------|----------------|
| 1.1.1 Non-text Content | A | Images have alt text | Missing alt on badge/avatar images |
| 1.3.1 Info and Relationships | A | Structure conveyed programmatically | Divs styled as buttons |
| 1.4.1 Use of Color | A | Color not sole means of conveying info | Green/red answer feedback |
| 1.4.3 Contrast (Minimum) | AA | 4.5:1 for text, 3:1 for large text | Light grey text on white |
| 1.4.4 Resize Text | AA | Text resizable to 200% | Fixed px font sizes |
| 1.4.10 Reflow | AA | Single column at 320px width | Horizontal scroll on mobile |
| 1.4.11 Non-text Contrast | AA | 3:1 for UI components | Low-contrast focus ring |
| 2.1.1 Keyboard | A | All functionality keyboard accessible | Click-only game elements |
| 2.4.3 Focus Order | A | Focus in logical sequence | Tab jumps around the page |
| 2.4.7 Focus Visible | AA | Keyboard focus indicator visible | No visible focus ring |
| 3.3.1 Error Identification | A | Errors described in text | Red border only on invalid input |
| 4.1.2 Name, Role, Value | A | Custom widgets have accessible name/role | Missing aria-label on icon buttons |

## Procedure / Template

### Step 1 — Automated Scan with axe-core (Playwright)

```typescript
// e2e/accessibility/audit.spec.ts
import { test, expect } from "@playwright/test";
import AxeBuilder from "@axe-core/playwright";

const PAGES_TO_AUDIT = [
  { url: "/login",            name: "Login page" },
  { url: "/dashboard",        name: "Student dashboard" },
  { url: "/quiz/seed-quiz-1", name: "Quiz page" },
  { url: "/quiz/seed-quiz-1/results", name: "Quiz results" },
  { url: "/leaderboard",      name: "Leaderboard" },
];

for (const { url, name } of PAGES_TO_AUDIT) {
  test(`${name} has no WCAG 2.1 AA violations`, async ({ page }) => {
    await page.goto(url);
    // Wait for dynamic content to load
    await page.waitForLoadState("networkidle");

    const results = await new AxeBuilder({ page })
      .withTags(["wcag2a", "wcag2aa", "best-practice"])
      .exclude("#cookie-banner")  // exclude third-party embeds
      .analyze();

    if (results.violations.length > 0) {
      console.log(
        "Violations:\n",
        results.violations.map((v) => `[${v.impact}] ${v.id}: ${v.description}\n  ${v.nodes.map((n) => n.html).join("\n  ")}`).join("\n\n")
      );
    }

    expect(results.violations).toHaveLength(0);
  });
}
```

### Step 2 — Contrast Check

Run colour contrast checks programmatically:

```typescript
// e2e/accessibility/contrast.spec.ts
import { test, expect } from "@playwright/test";

test("all text elements meet 4.5:1 contrast ratio", async ({ page }) => {
  await page.goto("/dashboard");

  // Use axe-core's color-contrast rule specifically
  const AxeBuilder = (await import("@axe-core/playwright")).default;
  const results = await new AxeBuilder({ page })
    .withRules(["color-contrast"])
    .analyze();

  expect(results.violations).toHaveLength(0);
});
```

Manual check tool: https://webaim.org/resources/contrastchecker/

AceQuest approved colour combinations:
```
quest-navy (#1A1F5E) on white (#FFFFFF)   → 10.6:1 ✓
quest-purple (#6B21A8) on white           → 7.2:1 ✓
quest-green (#15803D) on white            → 5.9:1 ✓
quest-red (#B91C1C) on white              → 5.9:1 ✓
Gray-400 (#9CA3AF) on white               → 2.5:1 ✗ — do NOT use for text
```

### Step 3 — Keyboard Navigation Test (Manual)

Open each page and navigate using ONLY the keyboard. Document the tab order:

```
Keyboard Test Script:
1. Open /quiz/:id
2. Press Tab — focus should move to: Skip link → Header nav → Quiz title → First answer option
3. Press Tab again through all answer options
4. Press Space on "Option A" — should select it and show aria-checked="true"
5. Press Tab to Next button → press Enter → should advance to next question
6. Confirm focus moves logically (not to hidden elements, not off-screen)
7. Repeat until submission
8. Press Tab on results page — score, XP, badges should all be reachable

Pass/Fail criteria:
✓ Every interactive element reachable
✓ Focus order matches visual reading order
✓ Focus indicator visible at all times
✓ No keyboard trap (except intentional modal trap)
✓ Escape key closes modals and dropdowns
```

### Step 4 — Screen Reader Test (NVDA + Chrome)

```
Screen Reader Script:
1. Open NVDA, open Chrome
2. Navigate to /quiz/:id using browse mode
3. Verify page structure announcement: "Quiz: Mathematics Grade 5, main landmark"
4. Use heading navigation (H key): should find "Question 3 of 10"
5. Navigate to answer options (NVDA reads): "Choose your answer, group"
6. Tab to each option: "Option A, radio button, not checked, 1 of 4"
7. Press Space: "Option A, radio button, checked, 1 of 4"
8. Submit quiz: confirm "Your score is 80%, Correct: 8 of 10" is announced
9. Verify badge unlock announcement: "Badge unlocked: Quiz Master" via aria-live region
```

### Step 5 — Mobile Accessibility Test

```
Mobile Test (iPhone, VoiceOver):
1. Enable VoiceOver on iOS
2. Open AceQuest in Safari
3. Swipe right to navigate through elements
4. Verify all interactive elements have descriptive labels
5. Double-tap to activate buttons
6. Confirm quiz can be completed entirely with VoiceOver enabled
```

### Step 6 — Audit Report Template

```markdown
# Accessibility Audit Report
**Date:** 2025-06-01
**Auditor:** QA Accessibility Agent
**Pages audited:** /login, /dashboard, /quiz/:id, /quiz/:id/results
**Standard:** WCAG 2.1 Level AA
**Tools:** axe-core 4.9, Lighthouse 12, NVDA 2024.1 + Chrome 124

## Summary
| Status | Count |
|--------|-------|
| Violations | 3 |
| Needs Review | 2 |
| Passed | 47 |

## Violations

### V1 — Color Contrast (1.4.3) — P2
**Element:** `.text-gray-400` on white background in quiz timer
**Contrast:** 2.5:1 (required: 4.5:1)
**Remediation:** Change to `text-gray-600` (#4B5563, contrast 7.0:1)
**Code:**
```tsx
// Before
<span className="text-gray-400">{remaining}s</span>
// After
<span className="text-gray-600">{remaining}s</span>
```

### V2 — Missing Button Label (4.1.2) — P1
**Element:** Close icon button in badge modal
**Issue:** `<button>✕</button>` — no accessible name
**Remediation:** Add `aria-label="Close badge details"`
```tsx
// After
<button aria-label="Close badge details" onClick={onClose}>
  <span aria-hidden="true">✕</span>
</button>
```

### V3 — Color as Sole Indicator (1.4.1) — P1
**Element:** Correct/incorrect answer feedback
**Issue:** Red/green border only — no icon or text
**Remediation:** Add ✓/✗ icon and status text alongside colour
```

## Output
- Automated axe-core scan results (JSON export)
- Filled audit report (markdown) filed as GitHub Issue with label `accessibility`
- Violations filed as individual bugs with WCAG criterion cited
- Re-audit scheduled after fixes are deployed (within 1 sprint)

## Quality Checks
- [ ] axe-core scan returns zero violations for all audited pages
- [ ] Manual keyboard navigation test completed — all elements reachable
- [ ] Screen reader test (NVDA or VoiceOver) completed for critical flows
- [ ] Colour contrast verified for all text: body >= 4.5:1, large >= 3:1
- [ ] Mobile VoiceOver test completed on at least one iOS device
- [ ] Each violation filed as a separate bug with WCAG criterion, element HTML, and remediation code
- [ ] Audit report includes both automated and manual findings
- [ ] Re-audit date scheduled in report

## Example

```bash
$ npx playwright test e2e/accessibility/audit.spec.ts

Running 5 tests

  ✓ Login page has no WCAG 2.1 AA violations (3.1s)
  ✗ Student dashboard has no WCAG 2.1 AA violations (2.8s)
    Expected: 0 violations
    Received: 2 violations
    [serious] color-contrast: Ensures text has sufficient color contrast
      .quiz-timer-text: #9CA3AF on #FFFFFF — ratio 2.5:1
    [critical] button-name: Buttons must have an accessible name
      <button class="modal-close">✕</button>

  2 passed, 1 failed
```
