# Skill: Write Unit Test

## Purpose
Define the standard for writing unit tests in AceQuest using Vitest. Every service method, utility function, Zod schema, and React component with logic must have unit tests. Tests must be fast (< 50 ms each), deterministic, and isolated from external dependencies (database, Redis, third-party APIs).

## Used By
- QA Agent
- Backend Engineer Agent
- Frontend Engineer Agent

## Inputs
| Field | Type | Description |
|-------|------|-------------|
| `subject` | string | Module being tested: service class, utility, schema, or component |
| `framework` | `"vitest" \| "react-testing-library"` | Test framework |
| `dependencies` | string[] | External deps to mock: `["prisma", "redis", "razorpay"]` |
| `happyPath` | string | Description of the main success scenario |
| `edgeCases` | string[] | List of edge cases and error scenarios to cover |

## Procedure / Template

### Step 1 — Set Up Vitest Configuration

```typescript
// vitest.config.ts
import { defineConfig } from "vitest/config";
import react from "@vitejs/plugin-react";
import tsconfigPaths from "vite-tsconfig-paths";

export default defineConfig({
  plugins: [react(), tsconfigPaths()],
  test: {
    globals: true,
    environment: "node",   // use "jsdom" for component tests
    setupFiles: ["./src/test/setup.ts"],
    coverage: {
      provider: "v8",
      reporter: ["text", "lcov"],
      thresholds: { lines: 80, functions: 80, branches: 75 },
    },
  },
});
```

### Step 2 — Global Test Setup

```typescript
// src/test/setup.ts
import { vi } from "vitest";

// Mock Prisma globally — override per-test as needed
vi.mock("@/lib/prisma", () => ({
  prisma: {
    quiz: { findUnique: vi.fn(), findMany: vi.fn(), create: vi.fn() },
    quizSubmission: { create: vi.fn() },
    student: { update: vi.fn(), findUnique: vi.fn() },
    $transaction: vi.fn((fn) => fn({})),
  },
}));

// Mock Redis globally
vi.mock("@/lib/redis", () => ({
  redis: {
    get: vi.fn(),
    set: vi.fn(),
    del: vi.fn(),
  },
}));
```

### Step 3 — Unit Test for a Service Method

```typescript
// src/services/__tests__/quiz.service.test.ts
import { describe, it, expect, beforeEach, vi } from "vitest";
import { QuizService } from "../quiz.service";
import { prisma } from "@/lib/prisma";
import { redis } from "@/lib/redis";
import { AppError } from "@/utils/AppError";

const mockQuiz = {
  id: "quiz-123",
  status: "ACTIVE",
  topicId: "topic-456",
  questions: [
    {
      id: "q1",
      options: [
        { id: "opt-a", isCorrect: true },
        { id: "opt-b", isCorrect: false },
      ],
    },
  ],
};

describe("QuizService.submitQuiz", () => {
  let service: QuizService;

  beforeEach(() => {
    vi.clearAllMocks();
    service = new QuizService();
  });

  it("returns score, XP, and badges on valid submission", async () => {
    // Arrange
    vi.mocked(prisma.quiz.findUnique).mockResolvedValue(mockQuiz as any);
    vi.mocked(redis.get).mockResolvedValue(null);   // no duplicate session
    vi.mocked(prisma.$transaction).mockImplementation(async (fn) =>
      fn({
        quizSubmission: { create: vi.fn().mockResolvedValue({ id: "sub-1" }) },
      } as any)
    );

    // Act
    const result = await service.submitQuiz({
      studentId: "student-1",
      quizId: "quiz-123",
      sessionId: "sess-abc",
      answers: [{ questionId: "q1", selectedOptionId: "opt-a", timeTakenMs: 5000 }],
    });

    // Assert
    expect(result.score).toBe(100);
    expect(result.correctCount).toBe(1);
    expect(result.totalCount).toBe(1);
    expect(redis.set).toHaveBeenCalledWith(
      "quiz:session:sess-abc",
      expect.any(String),
      "EX",
      86_400
    );
  });

  it("throws 404 when quiz does not exist", async () => {
    vi.mocked(prisma.quiz.findUnique).mockResolvedValue(null);

    await expect(
      service.submitQuiz({ studentId: "s1", quizId: "bad-id", sessionId: "sess1", answers: [] })
    ).rejects.toMatchObject({ statusCode: 404, code: "QUIZ_NOT_FOUND" });
  });

  it("throws 409 QUIZ_INACTIVE when quiz status is ARCHIVED", async () => {
    vi.mocked(prisma.quiz.findUnique).mockResolvedValue({ ...mockQuiz, status: "ARCHIVED" } as any);

    await expect(
      service.submitQuiz({ studentId: "s1", quizId: "quiz-123", sessionId: "sess1", answers: [] })
    ).rejects.toMatchObject({ statusCode: 409, code: "QUIZ_INACTIVE" });
  });

  it("throws 409 DUPLICATE_SUBMISSION when session already submitted", async () => {
    vi.mocked(prisma.quiz.findUnique).mockResolvedValue(mockQuiz as any);
    vi.mocked(redis.get).mockResolvedValue("existing-submission-id");

    await expect(
      service.submitQuiz({ studentId: "s1", quizId: "quiz-123", sessionId: "sess1", answers: [] })
    ).rejects.toMatchObject({ statusCode: 409, code: "DUPLICATE_SUBMISSION" });
  });

  it("awards 0 score when all answers are wrong", async () => {
    vi.mocked(prisma.quiz.findUnique).mockResolvedValue(mockQuiz as any);
    vi.mocked(redis.get).mockResolvedValue(null);
    vi.mocked(prisma.$transaction).mockImplementation(async (fn) =>
      fn({ quizSubmission: { create: vi.fn().mockResolvedValue({ id: "sub-1" }) } } as any)
    );

    const result = await service.submitQuiz({
      studentId: "s1",
      quizId: "quiz-123",
      sessionId: "sess-new",
      answers: [{ questionId: "q1", selectedOptionId: "opt-b", timeTakenMs: 3000 }],
    });

    expect(result.score).toBe(0);
    expect(result.correctCount).toBe(0);
  });
});
```

### Step 4 — Unit Test for Zod Schema

```typescript
// src/schemas/__tests__/quiz.schema.test.ts
import { describe, it, expect } from "vitest";
import { SubmitQuizBodySchema } from "../quiz.schema";

describe("SubmitQuizBodySchema", () => {
  const validBody = {
    sessionId: "a1b2c3d4-0000-1111-2222-333344445555",
    answers: [
      { questionId: "11111111-1111-1111-1111-111111111111", selectedOptionId: "22222222-2222-2222-2222-222222222222", timeTakenMs: 5000 },
    ],
  };

  it("parses a valid body", () => {
    expect(() => SubmitQuizBodySchema.parse(validBody)).not.toThrow();
  });

  it("rejects empty answers array", () => {
    const result = SubmitQuizBodySchema.safeParse({ ...validBody, answers: [] });
    expect(result.success).toBe(false);
  });

  it("rejects timeTakenMs > 300000", () => {
    const result = SubmitQuizBodySchema.safeParse({
      ...validBody,
      answers: [{ ...validBody.answers[0], timeTakenMs: 999_999 }],
    });
    expect(result.success).toBe(false);
  });

  it("rejects non-UUID questionId", () => {
    const result = SubmitQuizBodySchema.safeParse({
      ...validBody,
      answers: [{ ...validBody.answers[0], questionId: "not-a-uuid" }],
    });
    expect(result.success).toBe(false);
  });
});
```

### Step 5 — React Component Unit Test

```tsx
// src/components/__tests__/ProgressBar.test.tsx
import { render, screen } from "@testing-library/react";
import { describe, it, expect } from "vitest";
import { ProgressBar } from "../ui/ProgressBar";

describe("ProgressBar", () => {
  it("renders with correct aria attributes", () => {
    render(<ProgressBar current={3} total={10} label="Quiz progress" />);
    const bar = screen.getByRole("progressbar");
    expect(bar).toHaveAttribute("aria-valuenow", "3");
    expect(bar).toHaveAttribute("aria-valuemax", "10");
    expect(bar).toHaveAttribute("aria-label", "Quiz progress: 3 of 10");
  });

  it("displays text progress indicator", () => {
    render(<ProgressBar current={7} total={10} />);
    expect(screen.getByText("7/10")).toBeInTheDocument();
  });
});
```

## Output
- `src/services/__tests__/<domain>.service.test.ts`
- `src/schemas/__tests__/<domain>.schema.test.ts`
- `src/components/__tests__/<Component>.test.tsx`
- Coverage report showing >= 80% line coverage for the module

## Quality Checks
- [ ] Each test has exactly one logical assertion (or a small group testing one behaviour)
- [ ] `beforeEach(() => vi.clearAllMocks())` prevents test pollution
- [ ] No real database, Redis, or HTTP calls — all mocked
- [ ] Tests follow AAA pattern: Arrange → Act → Assert
- [ ] Error tests use `expect(...).rejects.toMatchObject({ statusCode, code })`
- [ ] Tests run in < 50 ms each (`vitest --reporter=verbose` to verify)
- [ ] Coverage thresholds enforced in `vitest.config.ts`: 80% lines, 80% functions
- [ ] Test file is co-located with source or in `__tests__` sibling folder

## Example

```bash
$ npx vitest run src/services/__tests__/quiz.service.test.ts
 ✓ QuizService.submitQuiz > returns score, XP, and badges on valid submission (12ms)
 ✓ QuizService.submitQuiz > throws 404 when quiz does not exist (3ms)
 ✓ QuizService.submitQuiz > throws 409 QUIZ_INACTIVE when quiz status is ARCHIVED (2ms)
 ✓ QuizService.submitQuiz > throws 409 DUPLICATE_SUBMISSION (2ms)
 ✓ QuizService.submitQuiz > awards 0 score when all answers wrong (3ms)
 
 Test Files  1 passed (1)
 Tests       5 passed (5)
 Duration    48ms
```
