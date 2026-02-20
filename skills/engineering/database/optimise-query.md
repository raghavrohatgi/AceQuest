# Skill: Optimise Database Query

## Purpose
Provide a systematic method for identifying, diagnosing, and fixing slow or resource-intensive queries in AceQuest's PostgreSQL database. Covers EXPLAIN ANALYZE interpretation, index selection, N+1 elimination, query rewriting, and caching strategies so that every optimisation decision is evidence-based and measurable.

## Used By
- Backend Engineer Agent
- Database Agent
- Performance Review Agent

## Inputs
| Field | Type | Description |
| --- | --- | --- |
| `slowQuery` | string | The raw SQL or Prisma query that is slow |
| `executionTimeMs` | number | Current observed execution time |
| `targetTimeMs` | number | Acceptable execution time after optimisation |
| `tableSizes` | object | Approximate row counts for affected tables |
| `currentIndexes` | string[] | Existing indexes on the affected tables |

## Procedure / Template

### Step 1 — Capture the Slow Query

Enable `pg_stat_statements` to surface slow queries automatically:

```sql
-- Enable in postgresql.conf (or via superuser)
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;

-- Top 10 slowest queries
SELECT
  query,
  calls,
  total_exec_time / calls AS avg_ms,
  rows / calls AS avg_rows,
  100.0 * total_exec_time / SUM(total_exec_time) OVER () AS pct_total
FROM pg_stat_statements
ORDER BY total_exec_time DESC
LIMIT 10;
```

### Step 2 — Run EXPLAIN ANALYZE

```sql
EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON)
SELECT
  s.id,
  s."displayName",
  s."totalXP",
  COUNT(qs.id) AS submission_count,
  AVG(qs.score)::numeric(5,2) AS avg_score
FROM students s
LEFT JOIN quiz_submissions qs ON qs."studentId" = s.id
WHERE s."gradeLevel" = 5
  AND qs."submittedAt" > NOW() - INTERVAL '30 days'
GROUP BY s.id
ORDER BY s."totalXP" DESC
LIMIT 20;
```

Key nodes to look for:
| Node | Warning Sign | Action |
| --- | --- | --- |
| `Seq Scan` | On table > 10k rows | Add index |
| `Hash Join` | Large `Batches` count | Increase `work_mem`, or reduce result set |
| `Sort` | `Sort Method: external merge` | Add index, or increase `work_mem` |
| `Nested Loop` | Many iterations | Check for missing FK index on inner side |

### Step 3 — Diagnose N+1 in Prisma

```typescript
// BEFORE: N+1 — 1 query for quizzes + N queries for each quiz's questions
const quizzes = await prisma.quiz.findMany({ where: { topicId } });
for (const quiz of quizzes) {
  const questions = await prisma.question.findMany({ where: { quizId: quiz.id } });
  // ...
}

// AFTER: Single query with eager loading
const quizzes = await prisma.quiz.findMany({
  where: { topicId },
  include: {
    questions: {
      include: { options: { where: { isCorrect: true } } },
    },
  },
});
```

Use Prisma's `logging` option in development to surface N+1 patterns:

```typescript
// src/lib/prisma.ts
import { PrismaClient } from "@prisma/client";

export const prisma = new PrismaClient({
  log: process.env.NODE_ENV === "development"
    ? [{ emit: "event", level: "query" }]
    : [],
});

if (process.env.NODE_ENV === "development") {
  prisma.$on("query", (e) => {
    if (e.duration > 100) {
      console.warn(`[SLOW QUERY ${e.duration}ms] ${e.query}`);
    }
  });
}
```

### Step 4 — Add Missing Indexes

```sql
-- Composite index for the leaderboard query (gradeLevel filter + totalXP sort)
CREATE INDEX CONCURRENTLY IF NOT EXISTS "students_gradeLevel_totalXP_idx"
  ON students("gradeLevel", "totalXP" DESC);

-- Partial index for active quizzes only (reduces index size by ~80%)
CREATE INDEX CONCURRENTLY IF NOT EXISTS "quizzes_active_topicId_idx"
  ON quizzes("topicId")
  WHERE status = 'ACTIVE';

-- Index on FK + time for recent submissions query
CREATE INDEX CONCURRENTLY IF NOT EXISTS "quiz_submissions_studentId_submittedAt_idx"
  ON quiz_submissions("studentId", "submittedAt" DESC);
```

### Step 5 — Rewrite with Raw SQL via Prisma (when ORM adds overhead)

```typescript
// src/repositories/leaderboard.repository.ts
import { prisma } from "../lib/prisma";
import { Prisma } from "@prisma/client";

export async function getGradeLeaderboard(gradeLevel: number, limit: number = 20) {
  return prisma.$queryRaw<LeaderboardRow[]>(
    Prisma.sql`
      SELECT
        s.id,
        s."displayName",
        s."avatarUrl",
        s."totalXP",
        RANK() OVER (ORDER BY s."totalXP" DESC) AS rank
      FROM students s
      INNER JOIN users u ON u.id = s."userId"
      WHERE s."gradeLevel" = ${gradeLevel}
        AND u."deletedAt" IS NULL
      ORDER BY s."totalXP" DESC
      LIMIT ${limit}
    `
  );
}
```

### Step 6 — Caching Hot Queries with Redis

```typescript
// src/services/leaderboard.service.ts
import { redis } from "../lib/redis";
import { getGradeLeaderboard } from "../repositories/leaderboard.repository";

const LEADERBOARD_TTL = 300; // 5 minutes — acceptable staleness for leaderboard

export async function getCachedLeaderboard(gradeLevel: number) {
  const cacheKey = `cache:leaderboard:grade:${gradeLevel}`;
  const cached = await redis.get(cacheKey);
  if (cached) return JSON.parse(cached);

  const data = await getGradeLeaderboard(gradeLevel);
  await redis.set(cacheKey, JSON.stringify(data), "EX", LEADERBOARD_TTL);
  return data;
}

export async function invalidateLeaderboard(gradeLevel: number) {
  await redis.del(`cache:leaderboard:grade:${gradeLevel}`);
}
```

### Step 7 — Query Plan Diff (Before vs After)

Document the improvement in a PR comment:

```
Before optimisation:
  Planning: 2ms | Execution: 1,240ms
  Seq Scan on quiz_submissions (rows=284000, loops=1)

After adding composite index:
  Planning: 4ms | Execution: 18ms   ← 98.5% improvement
  Index Scan using quiz_submissions_studentId_submittedAt_idx
```

### Step 8 — Pagination Pattern (avoid OFFSET on large tables)

```typescript
// Cursor-based pagination — O(log n) vs OFFSET's O(n)
async function getSubmissions(studentId: string, cursor?: string, take = 20) {
  return prisma.quizSubmission.findMany({
    where: { studentId },
    orderBy: { submittedAt: "desc" },
    take,
    skip: cursor ? 1 : 0,
    cursor: cursor ? { id: cursor } : undefined,
  });
}
```

## Output
- SQL `EXPLAIN ANALYZE` output with interpretation notes
- New index DDL committed to `prisma/migrations/` via custom migration
- Updated Prisma queries replacing N+1 patterns
- Redis caching layer for queries with acceptable staleness
- Before/after benchmark results documented in PR

## Quality Checks
- [ ] `EXPLAIN ANALYZE` run on staging data (not just local dev)
- [ ] Every new index created with `CONCURRENTLY` on tables > 10k rows
- [ ] No `Seq Scan` on tables > 50k rows after optimisation (unless intentional)
- [ ] N+1 queries eliminated using `include` or batched raw SQL
- [ ] Leaderboard and reporting queries are cached in Redis with appropriate TTL
- [ ] `work_mem` not permanently increased in `postgresql.conf` without DBA review
- [ ] Benchmark: average query time measured over 100 runs, not a single observation
- [ ] Indexes documented in `design-indexes.md` skill output

## Example

```
Problem: Leaderboard query for Grade 5 taking 1.2 s with 50k students.

Root cause: Seq Scan on students table (gradeLevel not indexed),
            Sort on totalXP requires external merge (no index).

Fix applied:
  CREATE INDEX CONCURRENTLY students_gradeLevel_totalXP_idx
    ON students("gradeLevel", "totalXP" DESC);

Result: 18 ms (98.5% improvement). Redis cache added with 5-min TTL.
```
