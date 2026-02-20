# Skill: Implement Authentication Middleware

## Purpose
Provide a repeatable procedure for creating and applying JWT-based authentication middleware in AceQuest's Express backend. Middleware must verify access tokens, attach a typed `req.user` object, handle refresh-token rotation, and integrate with Redis for token revocation (logout/ban).

## Used By
- Backend Engineer Agent
- Security Review Agent
- Full-Stack Engineer Agent

## Inputs
| Field | Type | Description |
| --- | --- | --- |
| `jwtSecret` | string | Environment variable name holding the signing secret |
| `tokenExpiry` | string | Access token lifetime, e.g. `"15m"` |
| `refreshExpiry` | string | Refresh token lifetime, e.g. `"7d"` |
| `roles` | string[] | All valid roles in the system: `["student","teacher","parent","admin"]` |
| `redisClient` | RedisClient | Shared Redis client for blocklist checks |

## Procedure / Template

### Step 1 — Define the JWT Payload Type

```typescript
// src/types/auth.ts
export type UserRole = "student" | "teacher" | "parent" | "admin";

export interface JwtPayload {
  sub: string;          // userId (UUID)
  role: UserRole;
  iat: number;
  exp: number;
  jti: string;          // unique token ID for revocation
}

// Augment Express Request so req.user is typed everywhere
declare global {
  namespace Express {
    interface Request {
      user?: JwtPayload;
    }
  }
}
```

### Step 2 — Implement the authenticate Middleware

```typescript
// src/middleware/authenticate.ts
import { Request, Response, NextFunction } from "express";
import jwt from "jsonwebtoken";
import { redis } from "../lib/redis";
import { JwtPayload } from "../types/auth";
import { AppError } from "../utils/AppError";

const JWT_SECRET = process.env.JWT_SECRET!;

export async function authenticate(
  req: Request,
  _res: Response,
  next: NextFunction
): Promise<void> {
  try {
    const authHeader = req.headers.authorization;
    if (!authHeader?.startsWith("Bearer ")) {
      throw new AppError("Missing or malformed Authorization header", 401, "MISSING_TOKEN");
    }

    const token = authHeader.slice(7);

    let payload: JwtPayload;
    try {
      payload = jwt.verify(token, JWT_SECRET) as JwtPayload;
    } catch (err: any) {
      const code = err.name === "TokenExpiredError" ? "TOKEN_EXPIRED" : "INVALID_TOKEN";
      throw new AppError("Token verification failed", 401, code);
    }

    // Check Redis blocklist (logout / forced expiry)
    const revoked = await redis.get(`blocklist:token:${payload.jti}`);
    if (revoked) {
      throw new AppError("Token has been revoked", 401, "TOKEN_REVOKED");
    }

    req.user = payload;
    next();
  } catch (error) {
    next(error);
  }
}
```

### Step 3 — Implement requireRole Middleware

```typescript
// src/middleware/requireRole.ts
import { Request, Response, NextFunction } from "express";
import { UserRole } from "../types/auth";
import { AppError } from "../utils/AppError";

export function requireRole(allowed: UserRole[]) {
  return (req: Request, _res: Response, next: NextFunction): void => {
    if (!req.user) {
      return next(new AppError("Not authenticated", 401, "NOT_AUTHENTICATED"));
    }
    if (!allowed.includes(req.user.role)) {
      return next(
        new AppError(
          `Role '${req.user.role}' is not permitted for this action`,
          403,
          "FORBIDDEN"
        )
      );
    }
    next();
  };
}
```

### Step 4 — Token Issuance Helpers

```typescript
// src/utils/tokens.ts
import jwt from "jsonwebtoken";
import { v4 as uuidv4 } from "uuid";
import { redis } from "../lib/redis";
import { JwtPayload, UserRole } from "../types/auth";

const JWT_SECRET = process.env.JWT_SECRET!;
const REFRESH_SECRET = process.env.REFRESH_SECRET!;

export function issueAccessToken(userId: string, role: UserRole): string {
  const jti = uuidv4();
  const payload: Omit<JwtPayload, "iat" | "exp"> = { sub: userId, role, jti };
  return jwt.sign(payload, JWT_SECRET, { expiresIn: "15m" });
}

export function issueRefreshToken(userId: string): string {
  return jwt.sign({ sub: userId, jti: uuidv4() }, REFRESH_SECRET, { expiresIn: "7d" });
}

export async function revokeToken(jti: string, ttlSeconds: number): Promise<void> {
  // Store until the token would have expired naturally
  await redis.set(`blocklist:token:${jti}`, "1", "EX", ttlSeconds);
}
```

### Step 5 — Refresh Token Endpoint

```typescript
// src/controllers/auth.controller.ts  (excerpt)
import { Request, Response, NextFunction } from "express";
import jwt from "jsonwebtoken";
import { prisma } from "../lib/prisma";
import { issueAccessToken, issueRefreshToken, revokeToken } from "../utils/tokens";
import { AppError } from "../utils/AppError";

const REFRESH_SECRET = process.env.REFRESH_SECRET!;

export async function refreshTokenHandler(
  req: Request,
  res: Response,
  next: NextFunction
): Promise<void> {
  try {
    const { refreshToken } = req.cookies as { refreshToken?: string };
    if (!refreshToken) throw new AppError("No refresh token", 401, "NO_REFRESH_TOKEN");

    let payload: any;
    try {
      payload = jwt.verify(refreshToken, REFRESH_SECRET);
    } catch {
      throw new AppError("Invalid refresh token", 401, "INVALID_REFRESH_TOKEN");
    }

    const user = await prisma.user.findUniqueOrThrow({ where: { id: payload.sub } });

    // Rotate: revoke old refresh, issue new pair
    await revokeToken(payload.jti, 7 * 24 * 3600);
    const newAccess = issueAccessToken(user.id, user.role as any);
    const newRefresh = issueRefreshToken(user.id);

    res.cookie("refreshToken", newRefresh, {
      httpOnly: true,
      secure: process.env.NODE_ENV === "production",
      sameSite: "strict",
      maxAge: 7 * 24 * 60 * 60 * 1000,
    });

    res.json({ success: true, data: { accessToken: newAccess } });
  } catch (error) {
    next(error);
  }
}
```

### Step 6 — Logout Handler

```typescript
export async function logoutHandler(
  req: Request,
  res: Response,
  next: NextFunction
): Promise<void> {
  try {
    if (req.user) {
      // Remaining TTL in seconds
      const ttl = req.user.exp - Math.floor(Date.now() / 1000);
      if (ttl > 0) await revokeToken(req.user.jti, ttl);
    }
    res.clearCookie("refreshToken");
    res.status(204).send();
  } catch (error) {
    next(error);
  }
}
```

### Step 7 — AppError Utility

```typescript
// src/utils/AppError.ts
export class AppError extends Error {
  constructor(
    message: string,
    public readonly statusCode: number,
    public readonly code: string
  ) {
    super(message);
    this.name = "AppError";
    Object.setPrototypeOf(this, AppError.prototype);
  }
}
```

## Output
- `src/types/auth.ts` — typed JWT payload + Express augmentation
- `src/middleware/authenticate.ts` — JWT verification + Redis blocklist check
- `src/middleware/requireRole.ts` — role-based guard factory
- `src/utils/tokens.ts` — issue/revoke helpers
- Updated `src/controllers/auth.controller.ts` with refresh + logout handlers

## Quality Checks
- [ ] `JWT_SECRET` and `REFRESH_SECRET` are read from environment, never hardcoded
- [ ] `req.user` type is augmented globally so TypeScript enforces it
- [ ] Blocklist check uses `jti` (per-token ID), not `sub` (would block all tokens for user)
- [ ] Refresh tokens are rotated on every use (old token revoked immediately)
- [ ] `refreshToken` cookie is `httpOnly`, `secure` in production, `sameSite: strict`
- [ ] Access token TTL is short (15 min); refresh token TTL is 7 days
- [ ] Error codes are machine-readable strings (`TOKEN_EXPIRED`, `INVALID_TOKEN`, etc.)
- [ ] Unit tests: valid token, expired token, revoked token, missing header, wrong role

## Example

```
# Protected request
GET /api/v1/students/me
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

# 200 — token valid
{ "success": true, "data": { "id": "uuid", "name": "Aarav", "role": "student" } }

# 401 — token expired
{ "success": false, "meta": { "code": "TOKEN_EXPIRED" }, "timestamp": "..." }

# 403 — wrong role
{ "success": false, "meta": { "code": "FORBIDDEN" }, "timestamp": "..." }
```
