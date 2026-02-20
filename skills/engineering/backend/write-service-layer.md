# Skill: Write Service Layer

## Purpose
Define how to write a service-layer class for AceQuest's Express backend. The service layer is the single source of business logic — it sits between controllers (HTTP) and repositories/Prisma (data). Every non-trivial domain operation (score calculation, XP award, badge unlock, adaptive next-question selection) must live here, never in a controller or a route.

## Used By
- Backend Engineer Agent
- Full-Stack Engineer Agent
- AI/ML Agent (for calling adaptive-engine service methods)

## Inputs
| Field | Type | Description |
| --- | --- | --- |
| `domain` | string | Domain name, e.g. `quiz`, `student`, `badge` |
| `operations` | string[] | List of operations the service must expose |
| `dependencies` | string[] | Other services or repositories this service depends on |
| `transactional` | boolean | Whether any operations require database transactions |

## Procedure / Template

### Step 1 — Define the Service Interface

```typescript
// src/services/interfaces/IQuizService.ts
import { QuizSubmission, QuizResult } from "../types/quiz";

export interface IQuizService {
  submitQuiz(input: QuizSubmission): Promise<QuizResult>;
  getQuizById(quizId: string): Promise<Quiz>;
  getNextAdaptiveQuestion(studentId: string, topicId: string): Promise<Question>;
}
```

### Step 2 — Implement the Service Class

```typescript
// src/services/quiz.service.ts
import { prisma } from "../lib/prisma";
import { redis } from "../lib/redis";
import { IQuizService } from "./interfaces/IQuizService";
import { BadgeService } from "./badge.service";
import { XPService } from "./xp.service";
import { AdaptiveEngineService } from "./adaptiveEngine.service";
import { AppError } from "../utils/AppError";
import { logger } from "../utils/logger";

export interface QuizSubmission {
  studentId: string;
  quizId: string;
  sessionId: string;
  answers: Array<{
    questionId: string;
    selectedOptionId: string;
    timeTakenMs: number;
  }>;
}

export interface QuizResult {
  score: number;
  correctCount: number;
  totalCount: number;
  xpAwarded: number;
  badgesUnlocked: string[];
  nextQuestion?: { id: string; difficulty: number };
}

export class QuizService implements IQuizService {
  constructor(
    private readonly badgeService: BadgeService = new BadgeService(),
    private readonly xpService: XPService = new XPService(),
    private readonly adaptiveEngine: AdaptiveEngineService = new AdaptiveEngineService()
  ) {}

  async submitQuiz(input: QuizSubmission): Promise<QuizResult> {
    // 1. Verify quiz exists and is active
    const quiz = await prisma.quiz.findUnique({
      where: { id: input.quizId },
      include: { questions: { include: { options: true } } },
    });
    if (!quiz) throw new AppError("Quiz not found", 404, "QUIZ_NOT_FOUND");
    if (quiz.status !== "ACTIVE") throw new AppError("Quiz is not active", 409, "QUIZ_INACTIVE");

    // 2. Idempotency check — prevent duplicate submissions for same session
    const alreadySubmitted = await redis.get(`quiz:session:${input.sessionId}`);
    if (alreadySubmitted) {
      throw new AppError("Quiz already submitted for this session", 409, "DUPLICATE_SUBMISSION");
    }

    // 3. Grade answers
    const { correctCount, totalCount, answerDetails } = this.gradeAnswers(
      quiz.questions,
      input.answers
    );
    const score = Math.round((correctCount / totalCount) * 100);

    // 4. Persist everything in a transaction
    const [submission, xpAwarded, badgesUnlocked] = await prisma.$transaction(async (tx) => {
      const sub = await tx.quizSubmission.create({
        data: {
          studentId: input.studentId,
          quizId: input.quizId,
          sessionId: input.sessionId,
          score,
          correctCount,
          totalCount,
          answers: { createMany: { data: answerDetails } },
        },
      });

      const xp = await this.xpService.awardXP(
        { studentId: input.studentId, source: "QUIZ", referenceId: sub.id, amount: score },
        tx
      );

      const badges = await this.badgeService.evaluateBadges(
        { studentId: input.studentId, trigger: "QUIZ_COMPLETE", metadata: { score, quizId: input.quizId } },
        tx
      );

      return [sub, xp, badges];
    });

    // 5. Mark session as submitted in Redis (TTL = 24 h)
    await redis.set(`quiz:session:${input.sessionId}`, submission.id, "EX", 86_400);

    // 6. Invalidate student score cache
    await redis.del(`cache:student:${input.studentId}:stats`);

    logger.info("quiz.submitted", {
      studentId: input.studentId,
      quizId: input.quizId,
      score,
      xpAwarded,
      badgesCount: badgesUnlocked.length,
    });

    // 7. Get next adaptive question (non-blocking, best-effort)
    let nextQuestion: QuizResult["nextQuestion"];
    try {
      nextQuestion = await this.adaptiveEngine.selectNextQuestion(
        input.studentId,
        quiz.topicId
      );
    } catch (err) {
      logger.warn("adaptive.nextQuestion.failed", { studentId: input.studentId, err });
    }

    return { score, correctCount, totalCount, xpAwarded, badgesUnlocked, nextQuestion };
  }

  private gradeAnswers(
    questions: any[],
    answers: QuizSubmission["answers"]
  ): { correctCount: number; totalCount: number; answerDetails: any[] } {
    const questionMap = new Map(questions.map((q) => [q.id, q]));
    let correctCount = 0;
    const answerDetails: any[] = [];

    for (const answer of answers) {
      const question = questionMap.get(answer.questionId);
      if (!question) continue;
      const correctOption = question.options.find((o: any) => o.isCorrect);
      const isCorrect = correctOption?.id === answer.selectedOptionId;
      if (isCorrect) correctCount++;
      answerDetails.push({
        questionId: answer.questionId,
        selectedOptionId: answer.selectedOptionId,
        isCorrect,
        timeTakenMs: answer.timeTakenMs,
      });
    }

    return { correctCount, totalCount: questions.length, answerDetails };
  }

  async getQuizById(quizId: string) {
    const cached = await redis.get(`cache:quiz:${quizId}`);
    if (cached) return JSON.parse(cached);

    const quiz = await prisma.quiz.findUnique({
      where: { id: quizId },
      include: { questions: { include: { options: true } }, topic: true },
    });
    if (!quiz) throw new AppError("Quiz not found", 404, "QUIZ_NOT_FOUND");

    await redis.set(`cache:quiz:${quizId}`, JSON.stringify(quiz), "EX", 3_600);
    return quiz;
  }

  async getNextAdaptiveQuestion(studentId: string, topicId: string) {
    return this.adaptiveEngine.selectNextQuestion(studentId, topicId);
  }
}
```

### Step 3 — XP Service Example (dependency)

```typescript
// src/services/xp.service.ts  (excerpt)
import { Prisma } from "@prisma/client";

export interface AwardXPInput {
  studentId: string;
  source: "QUIZ" | "STREAK" | "BADGE" | "DAILY_GOAL";
  referenceId: string;
  amount: number;
}

export class XPService {
  async awardXP(input: AwardXPInput, tx?: Prisma.TransactionClient): Promise<number> {
    const db = tx ?? prisma;
    const multiplier = await this.getStreakMultiplier(input.studentId, db);
    const finalXP = Math.round(input.amount * multiplier);

    await db.xpEvent.create({
      data: {
        studentId: input.studentId,
        source: input.source,
        referenceId: input.referenceId,
        amount: finalXP,
      },
    });
    await db.student.update({
      where: { id: input.studentId },
      data: { totalXP: { increment: finalXP } },
    });
    return finalXP;
  }

  private async getStreakMultiplier(studentId: string, db: any): Promise<number> {
    const student = await db.student.findUnique({ where: { id: studentId }, select: { currentStreak: true } });
    const streak = student?.currentStreak ?? 0;
    if (streak >= 30) return 2.0;
    if (streak >= 14) return 1.5;
    if (streak >= 7) return 1.25;
    return 1.0;
  }
}
```

## Output
- `src/services/<domain>.service.ts` — service class with all business logic
- `src/services/interfaces/I<Domain>Service.ts` — TypeScript interface for the service
- Updated `src/controllers/<domain>.controller.ts` — instantiates and calls the service
- Unit tests in `src/services/__tests__/<domain>.service.test.ts`

## Quality Checks
- [ ] No `express`, `Request`, or `Response` imports inside any service file
- [ ] All database access goes through `prisma` (no raw SQL unless `optimise-query.md` skill is invoked)
- [ ] Transactions wrap operations that must be atomic (XP + badge + submission = one `$transaction`)
- [ ] Idempotency keys are used for submission-like operations (Redis session check)
- [ ] Caches are invalidated on write; stale reads are acceptable only where TTL is explicitly chosen
- [ ] All errors thrown are `AppError` with an HTTP status code and machine-readable `code`
- [ ] Service constructor accepts dependencies via DI (facilitates unit test mocking)
- [ ] Unit tests cover: happy path, duplicate submission, quiz not found, transaction rollback

## Example

```typescript
// Test: duplicate submission is rejected
it("throws 409 DUPLICATE_SUBMISSION on second submit for same sessionId", async () => {
  redis.get.mockResolvedValueOnce("existing-submission-id");
  await expect(
    quizService.submitQuiz({ studentId: "s1", quizId: "q1", sessionId: "sess1", answers: [] })
  ).rejects.toMatchObject({ code: "DUPLICATE_SUBMISSION", statusCode: 409 });
});
```
