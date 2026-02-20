# Skill: Create API Endpoint

## Purpose
Define the standard procedure for creating a new REST API endpoint in AceQuest's Node.js/Express backend. Ensures every endpoint has consistent request validation, error handling, authentication hooks, logging, and response shaping so that all agents produce interoperable, maintainable code.

## Used By
- Backend Engineer Agent
- Full-Stack Engineer Agent
- API Integration Agent

## Inputs
| Field | Type | Description |
| --- | --- | --- |
| `resource` | string | The domain resource being exposed (e.g. `quiz`, `student`, `badge`) |
| `method` | string | HTTP verb: GET, POST, PUT, PATCH, DELETE |
| `path` | string | Express route path, e.g. `/api/v1/quizzes/:quizId/submit` |
| `authRequired` | boolean | Whether a valid JWT is required |
| `roles` | string[] | Optional role whitelist, e.g. `["teacher", "admin"]` |
| `bodySchema` | ZodSchema | Zod schema describing the request body (POST/PUT/PATCH) |
| `querySchema` | ZodSchema | Zod schema describing allowed query params |
| `serviceMethod` | string | Name of the service-layer function to delegate to |

## Procedure / Template

### Step 1 — Define Zod Schemas

Create or update the schema file under `src/schemas/<resource>.schema.ts`.

```typescript
// src/schemas/quiz.schema.ts
import { z } from "zod";

export const SubmitQuizBodySchema = z.object({
  answers: z
    .array(
      z.object({
        questionId: z.string().uuid(),
        selectedOptionId: z.string().uuid(),
        timeTakenMs: z.number().int().min(0).max(300_000),
      })
    )
    .min(1)
    .max(50),
  sessionId: z.string().uuid(),
});

export type SubmitQuizBody = z.infer<typeof SubmitQuizBodySchema>;

export const SubmitQuizParamsSchema = z.object({
  quizId: z.string().uuid(),
});
```

### Step 2 — Create the Controller

Create `src/controllers/<resource>.controller.ts`. Controllers must never contain business logic — delegate to the service layer immediately.

```typescript
// src/controllers/quiz.controller.ts
import { Request, Response, NextFunction } from "express";
import { QuizService } from "../services/quiz.service";
import { SubmitQuizBodySchema, SubmitQuizParamsSchema } from "../schemas/quiz.schema";
import { createSuccessResponse } from "../utils/response";
import { logger } from "../utils/logger";

export class QuizController {
  constructor(private readonly quizService: QuizService) {}

  submitQuiz = async (req: Request, res: Response, next: NextFunction): Promise<void> => {
    try {
      const params = SubmitQuizParamsSchema.parse(req.params);
      const body = SubmitQuizBodySchema.parse(req.body);

      logger.info("quiz.submit.start", {
        studentId: req.user!.id,
        quizId: params.quizId,
        sessionId: body.sessionId,
      });

      const result = await this.quizService.submitQuiz({
        studentId: req.user!.id,
        quizId: params.quizId,
        answers: body.answers,
        sessionId: body.sessionId,
      });

      logger.info("quiz.submit.success", {
        studentId: req.user!.id,
        quizId: params.quizId,
        score: result.score,
      });

      res.status(200).json(createSuccessResponse(result));
    } catch (error) {
      next(error);
    }
  };
}
```

### Step 3 — Register the Route

Create or update `src/routes/<resource>.routes.ts`. Always apply middleware in the order: auth → role-check → validate → handler.

```typescript
// src/routes/quiz.routes.ts
import { Router } from "express";
import { QuizController } from "../controllers/quiz.controller";
import { QuizService } from "../services/quiz.service";
import { authenticate } from "../middleware/authenticate";
import { requireRole } from "../middleware/requireRole";
import { validateRequest } from "../middleware/validateRequest";
import { SubmitQuizBodySchema, SubmitQuizParamsSchema } from "../schemas/quiz.schema";
import { rateLimiter } from "../middleware/rateLimiter";

const router = Router();
const controller = new QuizController(new QuizService());

router.post(
  "/:quizId/submit",
  authenticate,
  requireRole(["student"]),
  rateLimiter({ windowMs: 60_000, max: 10, keyPrefix: "quiz:submit" }),
  validateRequest({ params: SubmitQuizParamsSchema, body: SubmitQuizBodySchema }),
  controller.submitQuiz
);

export default router;
```

### Step 4 — Mount the Router in app.ts

```typescript
// src/app.ts  (excerpt)
import quizRoutes from "./routes/quiz.routes";
app.use("/api/v1/quizzes", quizRoutes);
```

### Step 5 — Standard Response Utilities

```typescript
// src/utils/response.ts
export interface ApiResponse<T> {
  success: boolean;
  data: T;
  meta?: Record<string, unknown>;
  timestamp: string;
}

export function createSuccessResponse<T>(data: T, meta?: Record<string, unknown>): ApiResponse<T> {
  return {
    success: true,
    data,
    meta,
    timestamp: new Date().toISOString(),
  };
}

export function createErrorResponse(message: string, code: string): ApiResponse<null> {
  return {
    success: false,
    data: null,
    meta: { code },
    timestamp: new Date().toISOString(),
  };
}
```

### Step 6 — Global Error Handler (reference only, already exists)

```typescript
// src/middleware/errorHandler.ts
import { ZodError } from "zod";
import { Request, Response, NextFunction } from "express";
import { createErrorResponse } from "../utils/response";

export function errorHandler(err: unknown, _req: Request, res: Response, _next: NextFunction) {
  if (err instanceof ZodError) {
    return res.status(422).json({
      success: false,
      errors: err.flatten().fieldErrors,
      timestamp: new Date().toISOString(),
    });
  }
  // AppError, PrismaClientKnownRequestError, etc. handled below
  const status = (err as any)?.statusCode ?? 500;
  const message = (err as any)?.message ?? "Internal server error";
  res.status(status).json(createErrorResponse(message, (err as any)?.code ?? "INTERNAL_ERROR"));
}
```

## Output
- A new controller file at `src/controllers/<resource>.controller.ts`
- Updated schema file at `src/schemas/<resource>.schema.ts`
- Updated or new route file at `src/routes/<resource>.routes.ts`
- App mounting entry in `src/app.ts`

## Quality Checks
- [ ] No business logic inside the controller — all logic lives in the service
- [ ] All request inputs (params, query, body) are validated with Zod before use
- [ ] `req.user` is only accessed after the `authenticate` middleware is applied
- [ ] Role guard is applied before reaching the handler
- [ ] Rate limiter is attached to mutation endpoints
- [ ] All log statements include structured key-value fields (no interpolated strings)
- [ ] HTTP status codes match REST semantics: 200 OK, 201 Created, 204 No Content, 422 Validation, 401 Unauth, 403 Forbidden, 404 Not Found
- [ ] `try/catch` delegates to `next(error)` so the global handler runs
- [ ] Unit tests exist for the controller (mock the service) and for the schema

## Example

**Feature:** A student submits answers for a quiz.

```
POST /api/v1/quizzes/3f7a1b2c-1234-5678-abcd-ef0123456789/submit
Authorization: Bearer <student-jwt>
Content-Type: application/json

{
  "sessionId": "a1b2c3d4-0000-1111-2222-333344445555",
  "answers": [
    { "questionId": "q1-uuid", "selectedOptionId": "opt-uuid", "timeTakenMs": 8000 },
    { "questionId": "q2-uuid", "selectedOptionId": "opt-uuid", "timeTakenMs": 12000 }
  ]
}
```

**Success response (200):**
```json
{
  "success": true,
  "data": {
    "score": 85,
    "correctCount": 17,
    "totalCount": 20,
    "xpAwarded": 150,
    "badgesUnlocked": ["quiz-master"]
  },
  "timestamp": "2025-06-01T10:30:00.000Z"
}
```
