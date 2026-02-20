# Skill: Add Rate Limiting

## Purpose
Standardise how AceQuest applies rate limiting across all Express API endpoints. Rate limiting prevents abuse, protects the adaptive learning engine from being overwhelmed, and safeguards student data. This skill covers both global and per-route limits, Redis-backed sliding-window counters, and clear user-facing error responses.

## Used By
- Backend Engineer Agent
- Security Review Agent
- DevOps Agent

## Inputs
| Field | Type | Description |
| --- | --- | --- |
| `windowMs` | number | Duration of the sliding window in milliseconds |
| `max` | number | Maximum requests allowed per window |
| `keyPrefix` | string | Redis key prefix to namespace the counter (e.g. `"quiz:submit"`) |
| `keyBy` | `"ip" \ | "user" \ | "ip+user"` | How to identify the requester |
| `skipSuccessfulRequests` | boolean | If true, only failed requests count against the limit |
| `message` | string | Human-readable message returned on 429 |

## Procedure / Template

### Step 1 — Install Dependencies

```bash
npm install express-rate-limit rate-limit-redis ioredis
```

### Step 2 — Configure the Shared Redis Client

```typescript
// src/lib/redis.ts
import Redis from "ioredis";

export const redis = new Redis({
  host: process.env.REDIS_HOST ?? "localhost",
  port: Number(process.env.REDIS_PORT ?? 6379),
  password: process.env.REDIS_PASSWORD,
  lazyConnect: true,
  maxRetriesPerRequest: 3,
});

redis.on("error", (err) => {
  console.error("[Redis] Connection error:", err.message);
});
```

### Step 3 — Create the Rate Limiter Factory

```typescript
// src/middleware/rateLimiter.ts
import rateLimit, { Options } from "express-rate-limit";
import { RedisStore } from "rate-limit-redis";
import { redis } from "../lib/redis";
import { Request } from "express";

interface RateLimiterOptions {
  windowMs?: number;
  max?: number;
  keyPrefix?: string;
  keyBy?: "ip" | "user" | "ip+user";
  skipSuccessfulRequests?: boolean;
  message?: string;
}

export function rateLimiter(opts: RateLimiterOptions = {}) {
  const {
    windowMs = 60_000,
    max = 60,
    keyPrefix = "rl:global",
    keyBy = "user",
    skipSuccessfulRequests = false,
    message = "Too many requests. Please wait a moment and try again.",
  } = opts;

  const keyGenerator = (req: Request): string => {
    const ip = req.ip ?? "unknown";
    const userId = (req as any).user?.sub ?? "anon";
    if (keyBy === "ip") return `${keyPrefix}:${ip}`;
    if (keyBy === "user") return `${keyPrefix}:${userId}`;
    return `${keyPrefix}:${ip}:${userId}`;
  };

  return rateLimit({
    windowMs,
    max,
    skipSuccessfulRequests,
    keyGenerator,
    store: new RedisStore({
      sendCommand: (...args: string[]) => redis.call(...args) as any,
      prefix: keyPrefix,
    }),
    handler: (_req, res) => {
      res.status(429).json({
        success: false,
        data: null,
        meta: {
          code: "RATE_LIMIT_EXCEEDED",
          message,
          retryAfterMs: windowMs,
        },
        timestamp: new Date().toISOString(),
      });
    },
    standardHeaders: true,   // Return RateLimit-* headers
    legacyHeaders: false,
  });
}
```

### Step 4 — Apply Global Rate Limiter

Apply a permissive global limit early in the middleware chain to catch extreme flooding.

```typescript
// src/app.ts  (excerpt)
import express from "express";
import { rateLimiter } from "./middleware/rateLimiter";

const app = express();

// Global: 300 req / minute per IP (unauthenticated safety net)
app.use(rateLimiter({ windowMs: 60_000, max: 300, keyPrefix: "rl:global", keyBy: "ip" }));

app.use(express.json({ limit: "50kb" }));
// ... other middleware
```

### Step 5 — Apply Per-Route Rate Limiters

Tighter limits on sensitive or expensive routes:

```typescript
// src/routes/quiz.routes.ts  (excerpt)
import { rateLimiter } from "../middleware/rateLimiter";

// Students can submit at most 10 quiz results per minute
router.post(
  "/:quizId/submit",
  authenticate,
  requireRole(["student"]),
  rateLimiter({ windowMs: 60_000, max: 10, keyPrefix: "quiz:submit", keyBy: "user" }),
  validateRequest({ params: SubmitQuizParamsSchema, body: SubmitQuizBodySchema }),
  controller.submitQuiz
);

// Auth: 5 login attempts per 10 minutes per IP to prevent brute force
router.post(
  "/login",
  rateLimiter({ windowMs: 10 * 60_000, max: 5, keyPrefix: "auth:login", keyBy: "ip" }),
  authController.login
);

// Password reset: 3 per hour per IP
router.post(
  "/forgot-password",
  rateLimiter({ windowMs: 3_600_000, max: 3, keyPrefix: "auth:forgot", keyBy: "ip" }),
  authController.forgotPassword
);
```

### Step 6 — Redis Key Structure Reference

```
rl:global:<ip>                    ← global IP-based counter
quiz:submit:<userId>              ← per-user quiz submission counter
auth:login:<ip>                   ← login brute-force counter
auth:forgot:<ip>                  ← password-reset counter
```

Keys expire automatically after `windowMs` milliseconds (set via `EX` in RedisStore internals).

### Step 7 — Checking Current Rate Limit State (Admin Utility)

```typescript
// src/utils/rateLimitAdmin.ts
import { redis } from "../lib/redis";

export async function getRateLimitStatus(keyPrefix: string, identifier: string) {
  const key = `${keyPrefix}:${identifier}`;
  const count = await redis.get(key);
  const ttl = await redis.ttl(key);
  return { key, count: Number(count ?? 0), ttlSeconds: ttl };
}

export async function resetRateLimit(keyPrefix: string, identifier: string): Promise<void> {
  await redis.del(`${keyPrefix}:${identifier}`);
}
```

### Step 8 — Environment Variables

```env
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=supersecret
```

## Output
- Updated `src/lib/redis.ts` with shared client
- New `src/middleware/rateLimiter.ts` factory function
- Per-route `rateLimiter()` calls added to affected route files
- Global limiter mounted in `src/app.ts`

## Quality Checks
- [ ] Global limiter is applied before `express.json()` to avoid parsing large payloads before rejection
- [ ] Auth endpoints (login, register, forgot-password) always have IP-based limits
- [ ] Authenticated mutation endpoints use user-based limits to prevent per-account abuse
- [ ] Rate limit headers (`RateLimit-Limit`, `RateLimit-Remaining`, `RateLimit-Reset`) are included in responses
- [ ] 429 response uses the standard `ApiResponse` shape with `code: "RATE_LIMIT_EXCEEDED"`
- [ ] Redis unavailability does NOT crash the server (ioredis retries silently; rateLimit falls back gracefully)
- [ ] Unit tests mock the Redis store and assert 429 on the (max+1)th request
- [ ] Load-tested to confirm Redis counter accuracy under concurrent requests

## Example

```
# First 10 quiz submissions in 1 minute — 200 OK each
POST /api/v1/quizzes/:id/submit  →  200

# 11th request in the same minute window
POST /api/v1/quizzes/:id/submit
→ 429 Too Many Requests
  RateLimit-Limit: 10
  RateLimit-Remaining: 0
  RateLimit-Reset: 1717228260

{
  "success": false,
  "data": null,
  "meta": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Too many requests. Please wait a moment and try again.",
    "retryAfterMs": 60000
  },
  "timestamp": "2025-06-01T10:31:00.000Z"
}
```
