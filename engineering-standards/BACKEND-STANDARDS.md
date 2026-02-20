# AceQuest Backend Coding Standards
## Node.js/Express Best Practices

---

## Tech Stack

- **Runtime:** Node.js 20+ LTS
- **Framework:** Express.js or NestJS
- **Language:** TypeScript (strict mode)
- **Database:** PostgreSQL with Prisma ORM
- **Cache:** Redis
- **Authentication:** JWT with Auth0/Clerk
- **File Storage:** AWS S3
- **Testing:** Vitest + Supertest

---

## Project Structure

```
/src
  /api                       # API layer
    /routes                  # Route definitions
    /controllers             # Request handlers
    /middleware              # Express middleware
  /services                  # Business logic
    /assessment
    /user
    /gamification
  /models                    # Data models (Prisma schema)
  /lib                       # Shared utilities
    /auth                    # Authentication helpers
    /cache                   # Redis client
    /database                # Database client
    /storage                 # S3 client
    /validation              # Validation schemas
  /types                     # TypeScript types
  /config                    # Configuration
  /jobs                      # Background jobs
  /scripts                   # Utility scripts

/prisma
  schema.prisma              # Database schema
  /migrations                # Database migrations

/tests
  /unit                      # Unit tests
  /integration               # Integration tests
  /e2e                       # End-to-end tests
```

---

## TypeScript Standards

### Strict Configuration

```json
// tsconfig.json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "commonjs",
    "lib": ["ES2022"],
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "strictFunctionTypes": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "outDir": "./dist",
    "rootDir": "./src"
  }
}
```

### Type Definitions

```typescript
// ✅ GOOD - Explicit types
interface CreateAssessmentDTO {
  title: string;
  description: string;
  gradeLevel: number;
  subjectId: string;
  questions: QuestionDTO[];
  timeLimit?: number;
}

type AssessmentResponse = {
  id: string;
  title: string;
  questionCount: number;
  createdAt: Date;
};

// ❌ BAD - Using 'any'
function createAssessment(data: any): any {
  // Never use 'any'
}
```

---

## API Design Standards

### RESTful Conventions

```typescript
// ✅ GOOD - RESTful routes
GET    /api/v1/assessments              # List assessments
GET    /api/v1/assessments/:id          # Get assessment
POST   /api/v1/assessments              # Create assessment
PATCH  /api/v1/assessments/:id          # Update assessment
DELETE /api/v1/assessments/:id          # Delete assessment

GET    /api/v1/students/:id/progress    # Get student progress
POST   /api/v1/assessments/:id/submit   # Submit assessment

// ❌ BAD - Non-RESTful
GET    /api/v1/getAssessment/:id
POST   /api/v1/createAssessment
POST   /api/v1/deleteAssessment/:id
```

### API Versioning

Always include version in URL:
```typescript
// ✅ GOOD
app.use('/api/v1/assessments', assessmentRoutes);

// ❌ BAD
app.use('/api/assessments', assessmentRoutes);
```

### Request/Response Format

```typescript
// ✅ GOOD - Consistent response structure
interface APIResponse<T> {
  success: boolean;
  data?: T;
  error?: {
    code: string;
    message: string;
    details?: unknown;
  };
  meta?: {
    page?: number;
    pageSize?: number;
    total?: number;
  };
}

// Success response
res.json({
  success: true,
  data: {
    id: '123',
    title: 'Math Assessment'
  }
});

// Error response
res.status(400).json({
  success: false,
  error: {
    code: 'INVALID_INPUT',
    message: 'Grade level must be between 3 and 8'
  }
});

// Paginated response
res.json({
  success: true,
  data: assessments,
  meta: {
    page: 1,
    pageSize: 20,
    total: 156
  }
});
```

---

## Controller Pattern

```typescript
// ✅ GOOD - Thin controllers, fat services
import { Request, Response, NextFunction } from 'express';
import { assessmentService } from '@/services/assessment';
import { CreateAssessmentSchema } from '@/lib/validation';

export class AssessmentController {
  async create(req: Request, res: Response, next: NextFunction) {
    try {
      // 1. Validate input
      const validatedData = CreateAssessmentSchema.parse(req.body);

      // 2. Call service layer
      const assessment = await assessmentService.create(
        validatedData,
        req.user.id
      );

      // 3. Return response
      return res.status(201).json({
        success: true,
        data: assessment,
      });
    } catch (error) {
      next(error); // Pass to error handler middleware
    }
  }

  async getById(req: Request, res: Response, next: NextFunction) {
    try {
      const { id } = req.params;
      const assessment = await assessmentService.getById(id, req.user.id);

      if (!assessment) {
        return res.status(404).json({
          success: false,
          error: {
            code: 'NOT_FOUND',
            message: 'Assessment not found',
          },
        });
      }

      return res.json({
        success: true,
        data: assessment,
      });
    } catch (error) {
      next(error);
    }
  }
}
```

---

## Service Layer

```typescript
// ✅ GOOD - Business logic in services
import { prisma } from '@/lib/database';
import { cache } from '@/lib/cache';
import { CreateAssessmentDTO } from '@/types';

export class AssessmentService {
  async create(data: CreateAssessmentDTO, userId: string) {
    // Business logic
    if (data.gradeLevel < 3 || data.gradeLevel > 8) {
      throw new ValidationError('Grade level must be between 3 and 8');
    }

    // Database transaction
    const assessment = await prisma.assessment.create({
      data: {
        ...data,
        createdById: userId,
        status: 'draft',
      },
      include: {
        questions: true,
      },
    });

    // Invalidate cache
    await cache.del(`user:${userId}:assessments`);

    // Return result
    return assessment;
  }

  async getById(id: string, userId: string) {
    // Check cache first
    const cacheKey = `assessment:${id}`;
    const cached = await cache.get(cacheKey);
    if (cached) {
      return JSON.parse(cached);
    }

    // Fetch from database
    const assessment = await prisma.assessment.findFirst({
      where: {
        id,
        OR: [
          { createdById: userId },
          { published: true },
        ],
      },
      include: {
        questions: true,
        _count: {
          select: { attempts: true },
        },
      },
    });

    // Cache result
    if (assessment) {
      await cache.setex(cacheKey, 300, JSON.stringify(assessment));
    }

    return assessment;
  }

  async calculateAdaptiveDifficulty(
    studentId: string,
    subjectId: string
  ): Promise<DifficultyLevel> {
    // Complex business logic
    const history = await this.getStudentHistory(studentId, subjectId);
    const recentPerformance = this.analyzePerformance(history);

    return this.determineDifficulty(recentPerformance);
  }
}

export const assessmentService = new AssessmentService();
```

---

## Middleware Standards

### Authentication Middleware

```typescript
// ✅ GOOD - Auth middleware
import { Request, Response, NextFunction } from 'express';
import { verifyJWT } from '@/lib/auth';

export async function authenticate(
  req: Request,
  res: Response,
  next: NextFunction
) {
  try {
    const token = req.headers.authorization?.replace('Bearer ', '');

    if (!token) {
      return res.status(401).json({
        success: false,
        error: {
          code: 'NO_TOKEN',
          message: 'Authentication required',
        },
      });
    }

    const payload = await verifyJWT(token);
    req.user = payload; // Attach user to request
    next();
  } catch (error) {
    return res.status(401).json({
      success: false,
      error: {
        code: 'INVALID_TOKEN',
        message: 'Invalid or expired token',
      },
    });
  }
}
```

### Authorization Middleware

```typescript
// ✅ GOOD - Role-based authorization
export function authorize(...roles: string[]) {
  return (req: Request, res: Response, next: NextFunction) => {
    if (!req.user) {
      return res.status(401).json({
        success: false,
        error: { code: 'UNAUTHORIZED', message: 'Authentication required' },
      });
    }

    if (!roles.includes(req.user.role)) {
      return res.status(403).json({
        success: false,
        error: { code: 'FORBIDDEN', message: 'Insufficient permissions' },
      });
    }

    next();
  };
}

// Usage
router.delete(
  '/assessments/:id',
  authenticate,
  authorize('teacher', 'admin'),
  assessmentController.delete
);
```

### Validation Middleware

```typescript
// ✅ GOOD - Zod validation middleware
import { z } from 'zod';

export function validateBody<T extends z.ZodType>(schema: T) {
  return (req: Request, res: Response, next: NextFunction) => {
    try {
      req.body = schema.parse(req.body);
      next();
    } catch (error) {
      if (error instanceof z.ZodError) {
        return res.status(400).json({
          success: false,
          error: {
            code: 'VALIDATION_ERROR',
            message: 'Invalid request data',
            details: error.errors,
          },
        });
      }
      next(error);
    }
  };
}

// Usage
router.post(
  '/assessments',
  authenticate,
  validateBody(CreateAssessmentSchema),
  assessmentController.create
);
```

### Rate Limiting

```typescript
// ✅ GOOD - Rate limiting
import rateLimit from 'express-rate-limit';

export const apiLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // 100 requests per window
  message: {
    success: false,
    error: {
      code: 'RATE_LIMIT_EXCEEDED',
      message: 'Too many requests, please try again later',
    },
  },
  standardHeaders: true,
  legacyHeaders: false,
});

// Stricter limit for authentication
export const authLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 5,
  skipSuccessfulRequests: true,
});

app.use('/api', apiLimiter);
app.use('/api/v1/auth', authLimiter);
```

---

## Error Handling

### Custom Error Classes

```typescript
// ✅ GOOD - Custom error hierarchy
export class AppError extends Error {
  constructor(
    public code: string,
    public message: string,
    public statusCode: number = 500,
    public isOperational: boolean = true
  ) {
    super(message);
    Object.setPrototypeOf(this, AppError.prototype);
  }
}

export class ValidationError extends AppError {
  constructor(message: string) {
    super('VALIDATION_ERROR', message, 400);
  }
}

export class NotFoundError extends AppError {
  constructor(resource: string) {
    super('NOT_FOUND', `${resource} not found`, 404);
  }
}

export class UnauthorizedError extends AppError {
  constructor(message = 'Unauthorized') {
    super('UNAUTHORIZED', message, 401);
  }
}

export class ForbiddenError extends AppError {
  constructor(message = 'Forbidden') {
    super('FORBIDDEN', message, 403);
  }
}
```

### Global Error Handler

```typescript
// ✅ GOOD - Centralized error handling
export function errorHandler(
  err: Error,
  req: Request,
  res: Response,
  next: NextFunction
) {
  // Log error
  logger.error('Error occurred:', {
    error: err.message,
    stack: err.stack,
    path: req.path,
    method: req.method,
    userId: req.user?.id,
  });

  // Handle known errors
  if (err instanceof AppError) {
    return res.status(err.statusCode).json({
      success: false,
      error: {
        code: err.code,
        message: err.message,
      },
    });
  }

  // Handle Prisma errors
  if (err.constructor.name === 'PrismaClientKnownRequestError') {
    return res.status(400).json({
      success: false,
      error: {
        code: 'DATABASE_ERROR',
        message: 'Database operation failed',
      },
    });
  }

  // Handle unknown errors
  res.status(500).json({
    success: false,
    error: {
      code: 'INTERNAL_ERROR',
      message: process.env.NODE_ENV === 'production'
        ? 'An unexpected error occurred'
        : err.message,
    },
  });
}

app.use(errorHandler);
```

---

## Database Standards (Prisma)

### Schema Design

```prisma
// ✅ GOOD - Well-structured schema
model User {
  id            String   @id @default(cuid())
  email         String   @unique
  role          Role     @default(STUDENT)
  createdAt     DateTime @default(now())
  updatedAt     DateTime @updatedAt

  // Relations
  profile       Profile?
  assessments   Assessment[]
  progress      Progress[]

  @@index([email])
  @@map("users")
}

model Assessment {
  id          String   @id @default(cuid())
  title       String
  description String?
  gradeLevel  Int
  subjectId   String
  published   Boolean  @default(false)
  createdAt   DateTime @default(now())
  updatedAt   DateTime @updatedAt

  // Relations
  subject     Subject  @relation(fields: [subjectId], references: [id])
  questions   Question[]
  attempts    AssessmentAttempt[]
  createdBy   User     @relation(fields: [createdById], references: [id])
  createdById String

  @@index([subjectId])
  @@index([createdById])
  @@index([gradeLevel, published])
  @@map("assessments")
}
```

### Query Optimization

```typescript
// ✅ GOOD - Efficient queries
// Select only needed fields
const users = await prisma.user.findMany({
  select: {
    id: true,
    email: true,
    profile: {
      select: { name: true },
    },
  },
});

// Use pagination
const assessments = await prisma.assessment.findMany({
  skip: (page - 1) * pageSize,
  take: pageSize,
  orderBy: { createdAt: 'desc' },
});

// Use transactions for related operations
await prisma.$transaction(async (tx) => {
  const assessment = await tx.assessment.create({ data: assessmentData });
  await tx.question.createMany({ data: questions });
  return assessment;
});

// ❌ BAD - Inefficient
// Fetching all data
const users = await prisma.user.findMany({
  include: { // Over-fetching
    profile: true,
    assessments: true,
    progress: true,
  },
});

// N+1 queries
for (const user of users) {
  const progress = await prisma.progress.findMany({ // N+1!
    where: { userId: user.id },
  });
}
```

---

## Caching Strategy

```typescript
// ✅ GOOD - Strategic caching
import Redis from 'ioredis';

const redis = new Redis(process.env.REDIS_URL);

// Cache frequently accessed data
export async function getAssessment(id: string) {
  const cacheKey = `assessment:${id}`;

  // Try cache first
  const cached = await redis.get(cacheKey);
  if (cached) {
    return JSON.parse(cached);
  }

  // Fetch from database
  const assessment = await prisma.assessment.findUnique({
    where: { id },
    include: { questions: true },
  });

  // Cache for 5 minutes
  if (assessment) {
    await redis.setex(cacheKey, 300, JSON.stringify(assessment));
  }

  return assessment;
}

// Invalidate cache on updates
export async function updateAssessment(id: string, data: UpdateData) {
  const updated = await prisma.assessment.update({
    where: { id },
    data,
  });

  // Invalidate cache
  await redis.del(`assessment:${id}`);

  return updated;
}
```

---

## Security Best Practices

### Input Sanitization

```typescript
// ✅ GOOD - Validate and sanitize all inputs
import { z } from 'zod';
import validator from 'validator';

const CreateUserSchema = z.object({
  email: z.string().email().transform(validator.normalizeEmail),
  name: z.string().min(1).max(100).transform(validator.escape),
  grade: z.number().int().min(3).max(8),
});
```

### Password Security

```typescript
// ✅ GOOD - Secure password handling
import bcrypt from 'bcrypt';

const SALT_ROUNDS = 12;

export async function hashPassword(password: string): Promise<string> {
  return bcrypt.hash(password, SALT_ROUNDS);
}

export async function verifyPassword(
  password: string,
  hash: string
): Promise<boolean> {
  return bcrypt.compare(password, hash);
}

// Never log passwords
logger.info('User login attempt', {
  email: user.email,
  // password: 'xxx' // ❌ NEVER log passwords!
});
```

### SQL Injection Prevention

```typescript
// ✅ GOOD - Prisma prevents SQL injection
await prisma.user.findMany({
  where: {
    email: userInput, // Automatically parameterized
  },
});

// ❌ BAD - Raw SQL with user input
await prisma.$executeRawUnsafe(
  `SELECT * FROM users WHERE email = '${userInput}'` // VULNERABLE!
);

// ✅ GOOD - If raw SQL needed, use parameters
await prisma.$executeRaw`
  SELECT * FROM users WHERE email = ${userInput}
`;
```

### CORS Configuration

```typescript
// ✅ GOOD - Strict CORS
import cors from 'cors';

app.use(
  cors({
    origin: process.env.ALLOWED_ORIGINS?.split(',') || [],
    credentials: true,
    optionsSuccessStatus: 200,
    maxAge: 86400, // 24 hours
  })
);

// ❌ BAD - Permissive CORS
app.use(cors({ origin: '*' })); // DON'T DO THIS IN PRODUCTION
```

---

## Logging Standards

```typescript
// ✅ GOOD - Structured logging
import winston from 'winston';

export const logger = winston.createLogger({
  level: process.env.LOG_LEVEL || 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.errors({ stack: true }),
    winston.format.json()
  ),
  defaultMeta: { service: 'acequest-api' },
  transports: [
    new winston.transports.File({ filename: 'error.log', level: 'error' }),
    new winston.transports.File({ filename: 'combined.log' }),
  ],
});

// Use in application
logger.info('Assessment created', {
  assessmentId: assessment.id,
  userId: user.id,
  gradeLevel: assessment.gradeLevel,
});

logger.error('Assessment creation failed', {
  error: error.message,
  userId: user.id,
  data: sanitizedData, // Remove sensitive info
});
```

---

## Testing Standards

### Unit Tests

```typescript
// ✅ GOOD - Unit test services
import { describe, it, expect, vi } from 'vitest';
import { assessmentService } from '@/services/assessment';
import { prisma } from '@/lib/database';

vi.mock('@/lib/database');

describe('AssessmentService', () => {
  describe('create', () => {
    it('creates assessment with valid data', async () => {
      const mockData = {
        title: 'Math Test',
        gradeLevel: 5,
        subjectId: 'math',
      };

      const mockResult = { id: '123', ...mockData };
      vi.mocked(prisma.assessment.create).mockResolvedValue(mockResult);

      const result = await assessmentService.create(mockData, 'user123');

      expect(result).toEqual(mockResult);
      expect(prisma.assessment.create).toHaveBeenCalledWith(
        expect.objectContaining({
          data: expect.objectContaining(mockData),
        })
      );
    });

    it('throws ValidationError for invalid grade', async () => {
      const invalidData = {
        title: 'Test',
        gradeLevel: 12, // Invalid
        subjectId: 'math',
      };

      await expect(
        assessmentService.create(invalidData, 'user123')
      ).rejects.toThrow(ValidationError);
    });
  });
});
```

### Integration Tests

```typescript
// ✅ GOOD - Integration test APIs
import request from 'supertest';
import { describe, it, expect, beforeAll, afterAll } from 'vitest';
import { app } from '@/app';
import { generateToken } from '@/lib/auth';

describe('POST /api/v1/assessments', () => {
  let authToken: string;

  beforeAll(async () => {
    authToken = await generateToken({ id: 'test-user', role: 'teacher' });
  });

  it('creates assessment with valid data', async () => {
    const response = await request(app)
      .post('/api/v1/assessments')
      .set('Authorization', `Bearer ${authToken}`)
      .send({
        title: 'Math Assessment',
        gradeLevel: 5,
        subjectId: 'math',
      });

    expect(response.status).toBe(201);
    expect(response.body.success).toBe(true);
    expect(response.body.data).toHaveProperty('id');
  });

  it('returns 401 without authentication', async () => {
    const response = await request(app)
      .post('/api/v1/assessments')
      .send({ title: 'Test' });

    expect(response.status).toBe(401);
  });
});
```

---

## Environment Configuration

```typescript
// ✅ GOOD - Type-safe environment variables
import { z } from 'zod';

const envSchema = z.object({
  NODE_ENV: z.enum(['development', 'production', 'test']),
  PORT: z.string().transform(Number),
  DATABASE_URL: z.string().url(),
  REDIS_URL: z.string().url(),
  JWT_SECRET: z.string().min(32),
  AWS_ACCESS_KEY_ID: z.string(),
  AWS_SECRET_ACCESS_KEY: z.string(),
  AWS_S3_BUCKET: z.string(),
  LOG_LEVEL: z.enum(['error', 'warn', 'info', 'debug']).default('info'),
});

export const env = envSchema.parse(process.env);

// Usage
console.log(env.PORT); // Type-safe, validated
```

---

## Key Takeaways

1. ✅ TypeScript strict mode always
2. ✅ Thin controllers, business logic in services
3. ✅ Validate all inputs with Zod
4. ✅ Use Prisma for database access (prevents SQL injection)
5. ✅ Implement proper error handling with custom classes
6. ✅ Cache strategically with Redis
7. ✅ Security first (auth, rate limiting, input sanitization)
8. ✅ Structured logging (Winston)
9. ✅ Test all business logic
10. ✅ Environment variables validated and type-safe

---

**Priority: Security > Reliability > Performance > Developer Experience**
