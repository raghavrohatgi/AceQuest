# Skill: Write End-to-End Test

## Purpose
Define how to write reliable, maintainable Playwright end-to-end tests for AceQuest's critical user journeys. E2E tests verify that the full stack — Next.js frontend, Express API, PostgreSQL, Redis — works together from the user's perspective. Focus on high-value flows: student login, quiz completion, XP/badge award, and teacher dashboard.

## Used By
- QA Agent
- Full-Stack Engineer Agent
- CI/CD Agent

## Inputs
| Field | Type | Description |
|-------|------|-------------|
| `userJourney` | string | Description of the scenario, e.g. "Student completes a quiz and earns a badge" |
| `persona` | string | User role and grade, e.g. "Grade 5 student, Aarav" |
| `preconditions` | string[] | Database state required before the test runs |
| `steps` | string[] | Ordered user actions |
| `assertions` | string[] | Observable outcomes to verify |

## Procedure / Template

### Step 1 — Configure Playwright

```typescript
// playwright.config.ts
import { defineConfig, devices } from "@playwright/test";

export default defineConfig({
  testDir: "./e2e",
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 4 : undefined,
  reporter: [["html", { outputFolder: "playwright-report" }], ["list"]],
  use: {
    baseURL: process.env.E2E_BASE_URL ?? "http://localhost:3000",
    trace: "on-first-retry",
    screenshot: "only-on-failure",
    video: "retain-on-failure",
    locale: "en-IN",
    timezoneId: "Asia/Kolkata",
  },
  projects: [
    {
      name: "chromium-desktop",
      use: { ...devices["Desktop Chrome"] },
    },
    {
      name: "mobile-android",
      use: { ...devices["Pixel 5"] },   // represents low-end Android common in India
    },
  ],
  webServer: {
    command: "npm run dev",
    port: 3000,
    reuseExistingServer: !process.env.CI,
  },
});
```

### Step 2 — Page Object Models

```typescript
// e2e/pages/LoginPage.ts
import { Page, Locator } from "@playwright/test";

export class LoginPage {
  readonly emailInput: Locator;
  readonly passwordInput: Locator;
  readonly submitButton: Locator;
  readonly errorMessage: Locator;

  constructor(private readonly page: Page) {
    this.emailInput    = page.getByLabel("Email address");
    this.passwordInput = page.getByLabel("Password");
    this.submitButton  = page.getByRole("button", { name: /log in/i });
    this.errorMessage  = page.getByRole("alert");
  }

  async goto() {
    await this.page.goto("/login");
  }

  async login(email: string, password: string) {
    await this.emailInput.fill(email);
    await this.passwordInput.fill(password);
    await this.submitButton.click();
  }
}
```

```typescript
// e2e/pages/QuizPage.ts
import { Page, Locator } from "@playwright/test";

export class QuizPage {
  constructor(private readonly page: Page) {}

  async goto(quizId: string) {
    await this.page.goto(`/quiz/${quizId}`);
  }

  async selectAnswer(optionText: string) {
    await this.page.getByRole("radio", { name: optionText }).click();
  }

  async clickNext() {
    await this.page.getByRole("button", { name: /next/i }).click();
  }

  async clickSubmit() {
    await this.page.getByRole("button", { name: /submit quiz/i }).click();
  }

  getScore(): Locator {
    return this.page.getByTestId("quiz-score");
  }

  getBadgeUnlocked(name: string): Locator {
    return this.page.getByRole("heading", { name });
  }

  getXPAwarded(): Locator {
    return this.page.getByTestId("xp-awarded");
  }
}
```

### Step 3 — Test Fixtures and Database Seeding

```typescript
// e2e/fixtures/index.ts
import { test as base } from "@playwright/test";
import { LoginPage } from "../pages/LoginPage";
import { QuizPage } from "../pages/QuizPage";
import { seedE2EData, teardownE2EData } from "../helpers/db";

type Fixtures = {
  loginPage: LoginPage;
  quizPage: QuizPage;
  studentCredentials: { email: string; password: string; quizId: string };
};

export const test = base.extend<Fixtures>({
  loginPage: async ({ page }, use) => {
    await use(new LoginPage(page));
  },
  quizPage: async ({ page }, use) => {
    await use(new QuizPage(page));
  },
  studentCredentials: async ({}, use) => {
    const data = await seedE2EData();   // creates a fresh student + quiz in test DB
    await use(data);
    await teardownE2EData(data.studentId);  // cleanup
  },
});

export { expect } from "@playwright/test";
```

```typescript
// e2e/helpers/db.ts
export async function seedE2EData() {
  const res = await fetch("http://localhost:3001/test-helpers/seed", {
    method: "POST",
  });
  return res.json() as Promise<{ email: string; password: string; quizId: string; studentId: string }>;
}

export async function teardownE2EData(studentId: string) {
  await fetch(`http://localhost:3001/test-helpers/teardown/${studentId}`, { method: "DELETE" });
}
```

### Step 4 — Write the E2E Test

```typescript
// e2e/tests/quiz-completion.spec.ts
import { test, expect } from "../fixtures";

test.describe("Student completes a quiz", () => {
  test("should display score, XP, and badge after full quiz submission", async ({
    page,
    loginPage,
    quizPage,
    studentCredentials,
  }) => {
    // Step 1 — Login
    await loginPage.goto();
    await loginPage.login(studentCredentials.email, studentCredentials.password);
    await expect(page).toHaveURL("/dashboard");
    await expect(page.getByRole("heading", { name: /welcome back/i })).toBeVisible();

    // Step 2 — Navigate to quiz
    await quizPage.goto(studentCredentials.quizId);
    await expect(page.getByRole("heading", { name: /Mathematics – Grade 5/i })).toBeVisible();

    // Step 3 — Answer all questions (fixture quiz has 3 questions, all answered correctly)
    await quizPage.selectAnswer("Option A");
    await quizPage.clickNext();

    await quizPage.selectAnswer("Option A");
    await quizPage.clickNext();

    await quizPage.selectAnswer("Option A");
    await quizPage.clickSubmit();

    // Step 4 — Verify results page
    await expect(page).toHaveURL(/\/quiz\/.*\/results/);
    await expect(quizPage.getScore()).toContainText("100");
    await expect(quizPage.getXPAwarded()).toContainText("XP");

    // Step 5 — Verify badge unlock (if seeded quiz triggers first-quiz badge)
    await expect(quizPage.getBadgeUnlocked("First Quiz!")).toBeVisible();
  });

  test("should prevent submitting the same quiz session twice", async ({
    page,
    loginPage,
    quizPage,
    studentCredentials,
  }) => {
    await loginPage.goto();
    await loginPage.login(studentCredentials.email, studentCredentials.password);

    // Submit once
    await quizPage.goto(studentCredentials.quizId);
    await quizPage.selectAnswer("Option A");
    await quizPage.clickSubmit();
    await expect(page).toHaveURL(/\/results/);

    // Attempt to access quiz again and submit
    await quizPage.goto(studentCredentials.quizId);
    await expect(
      page.getByText(/already completed/i)
    ).toBeVisible();
  });

  test("login with wrong password shows error message", async ({ loginPage, page }) => {
    await loginPage.goto();
    await loginPage.login("nonexistent@acequest.in", "wrongpassword");

    await expect(loginPage.errorMessage).toBeVisible();
    await expect(loginPage.errorMessage).toContainText(/invalid email or password/i);
    await expect(page).toHaveURL("/login");  // did not navigate away
  });
});
```

### Step 5 — Accessibility Assertions in E2E

```typescript
// e2e/tests/accessibility.spec.ts
import { test, expect } from "@playwright/test";
import AxeBuilder from "@axe-core/playwright";

test("dashboard has no automatically detectable accessibility violations", async ({ page }) => {
  await page.goto("/login");
  await page.fill('[name="email"]', "student.g5.1@acequest.in");
  await page.fill('[name="password"]', "AceQuest@dev123");
  await page.click('button[type="submit"]');
  await page.waitForURL("/dashboard");

  const results = await new AxeBuilder({ page })
    .withTags(["wcag2a", "wcag2aa"])
    .analyze();

  expect(results.violations).toHaveLength(0);
});
```

### Step 6 — Visual Regression (optional)

```typescript
test("quiz results page matches visual snapshot", async ({ page }) => {
  // ... navigate to results page
  await expect(page).toHaveScreenshot("quiz-results.png", { maxDiffPixels: 100 });
});
```

## Output
- `playwright.config.ts` — Playwright configuration
- `e2e/pages/` — Page Object Model files
- `e2e/fixtures/index.ts` — custom test fixtures
- `e2e/tests/<feature>.spec.ts` — test files
- HTML test report generated after each CI run

## Quality Checks
- [ ] Page Object Model used — no raw selectors in test bodies
- [ ] Tests are isolated: each uses a freshly seeded database state
- [ ] Cleanup runs in fixture teardown even if the test fails
- [ ] No `page.waitForTimeout()` — use `expect().toBeVisible()` or `page.waitForURL()` instead
- [ ] Selectors prefer ARIA roles and labels (`getByRole`, `getByLabel`) over CSS selectors
- [ ] Tests retry 2 times in CI (`retries: 2`) to handle flakiness
- [ ] Playwright traces captured on first retry for debugging
- [ ] Axe accessibility check included for critical pages
- [ ] Mobile viewport tested (`devices["Pixel 5"]`) — AceQuest primary device target

## Example

```bash
$ npx playwright test e2e/tests/quiz-completion.spec.ts

Running 3 tests using 3 workers

  ✓ [chromium] Student completes a quiz > should display score, XP, and badge (8.2s)
  ✓ [chromium] Student completes a quiz > should prevent duplicate submission (4.1s)
  ✓ [chromium] Student completes a quiz > login with wrong password shows error (2.8s)

  3 passed (11.3s)
```
