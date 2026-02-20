# Skill: Design Database Indexes

## Purpose
Define a systematic approach to selecting, creating, and documenting indexes for AceQuest's PostgreSQL database. Good indexes reduce query latency and CPU load; bad indexes waste write I/O and storage. This skill ensures every index decision is justified by a concrete query pattern, measured before and after, and documented in the schema.

## Used By
- Database Agent
- Backend Engineer Agent
- Performance Review Agent

## Inputs
| Field | Type | Description |
| --- | --- | --- |
| `queryPattern` | string | The SQL query or Prisma call that needs optimisation |
| `table` | string | Primary table name |
| `filterColumns` | string[] | Columns used in WHERE clauses |
| `sortColumns` | string[] | Columns used in ORDER BY |
| `cardinality` | object | Approximate distinct values per column |
| `tableRowCount` | number | Approximate number of rows |
| `writeFrequency` | `"high" \ | "medium" \ | "low"` | How often the table is written to |

## Procedure / Template

### Step 1 — Identify Query Patterns

List all frequent queries against the table and their access patterns:

| Query | Filter | Sort | Frequency |
| --- | --- | --- | --- |
| Leaderboard by grade | `gradeLevel = ?` | `totalXP DESC` | Every page load |
| Student submission history | `studentId = ?` | `submittedAt DESC` | Per session |
| Active quizzes by topic | `topicId = ?`, `status = 'ACTIVE'` | — | Per quiz load |
| Answer correctness rate | `questionId = ?`, `isCorrect = ?` | — | Analytics, daily |
| Skill mastery lookup | `studentId = ?`, `skillId = ?` | — | Per adaptive step |

### Step 2 — Index Type Selection

| Scenario | Index Type |
| --- | --- |
| Equality + range on text/uuid | B-Tree (default) |
| Full-text search on question text | GIN with `tsvector` |
| JSONB column queries | GIN |
| Geospatial (future feature) | GiST |
| Partial index (WHERE clause subset) | B-Tree with `WHERE` predicate |
| Index on expression / function | Expression index |

### Step 3 — Composite Index Column Order Rule

Always put **equality** columns before **range/sort** columns:

```
WHERE gradeLevel = 5            ← equality first
ORDER BY totalXP DESC           ← sort second
→  INDEX (gradeLevel, totalXP DESC)
```

Put the most selective column first among equality columns:
- `studentId` (UUID, ~100k distinct) before `gradeLevel` (1-8, 8 distinct)

### Step 4 — Create Indexes

```sql
-- 1. Leaderboard: grade filter + XP sort
CREATE INDEX CONCURRENTLY IF NOT EXISTS "students_gradeLevel_totalXP_idx"
  ON students ("gradeLevel", "totalXP" DESC)
  WHERE "deletedAt" IS NULL;   -- partial: exclude soft-deleted

-- 2. Submission history per student
CREATE INDEX CONCURRENTLY IF NOT EXISTS "quiz_submissions_studentId_submittedAt_idx"
  ON quiz_submissions ("studentId", "submittedAt" DESC);

-- 3. Active quizzes by topic (partial index)
CREATE INDEX CONCURRENTLY IF NOT EXISTS "quizzes_active_topicId_idx"
  ON quizzes ("topicId")
  WHERE status = 'ACTIVE';

-- 4. Answer analytics: question correctness
CREATE INDEX CONCURRENTLY IF NOT EXISTS "submission_answers_questionId_isCorrect_idx"
  ON submission_answers ("questionId", "isCorrect");

-- 5. Skill mastery point lookup (already covered by UNIQUE constraint, but explicit)
-- The UNIQUE constraint on (studentId, skillId) creates an implicit B-Tree index

-- 6. XP events timeline per student
CREATE INDEX CONCURRENTLY IF NOT EXISTS "xp_events_studentId_createdAt_idx"
  ON xp_events ("studentId", "createdAt" DESC);

-- 7. Full-text search on question text
ALTER TABLE questions ADD COLUMN IF NOT EXISTS search_vector tsvector
  GENERATED ALWAYS AS (to_tsvector('english', text)) STORED;

CREATE INDEX CONCURRENTLY IF NOT EXISTS "questions_search_vector_idx"
  ON questions USING GIN (search_vector);
```

### Step 5 — Register Indexes in Prisma Schema

```prisma
model Student {
  // ...
  @@index([gradeLevel, totalXP(sort: Desc)], name: "students_gradeLevel_totalXP_idx")
}

model QuizSubmission {
  // ...
  @@index([studentId, submittedAt(sort: Desc)], name: "quiz_submissions_studentId_submittedAt_idx")
}

model SubmissionAnswer {
  // ...
  @@index([questionId, isCorrect], name: "submission_answers_questionId_isCorrect_idx")
}
```

Note: Partial indexes and expression indexes are not expressible in Prisma schema — add them via custom migration SQL.

### Step 6 — Measure Index Impact

```sql
-- Before adding index: capture baseline plan and timing
EXPLAIN (ANALYZE, BUFFERS)
SELECT id, "displayName", "totalXP"
FROM students
WHERE "gradeLevel" = 5 AND "deletedAt" IS NULL
ORDER BY "totalXP" DESC
LIMIT 20;
-- Execution Time: 1240ms, Seq Scan

-- After index creation:
-- Execution Time: 11ms, Index Scan using students_gradeLevel_totalXP_idx
```

### Step 7 — Index Maintenance Queries

```sql
-- Find unused indexes (candidates for removal)
SELECT
  schemaname,
  tablename,
  indexname,
  idx_scan,
  pg_size_pretty(pg_relation_size(indexrelid)) AS size
FROM pg_stat_user_indexes
WHERE idx_scan = 0
  AND schemaname = 'public'
ORDER BY pg_relation_size(indexrelid) DESC;

-- Find duplicate indexes
SELECT
  indrelid::regclass AS table_name,
  array_agg(indexrelid::regclass ORDER BY indexrelid::regclass) AS index_names,
  array_agg(indkey) AS key_columns
FROM pg_index
GROUP BY indrelid, indkey
HAVING COUNT(*) > 1;

-- Index bloat check
SELECT
  tablename,
  indexname,
  pg_size_pretty(pg_relation_size(indexrelid)) AS index_size,
  idx_scan,
  idx_tup_read,
  idx_tup_fetch
FROM pg_stat_user_indexes
JOIN pg_statio_user_indexes USING (indexrelid)
ORDER BY pg_relation_size(indexrelid) DESC
LIMIT 20;
```

### Step 8 — Index Decision Matrix

```
Write frequency HIGH + Table large → prefer fewer, targeted indexes
Write frequency LOW + Read-heavy → index aggressively on all filter/sort columns
Column cardinality LOW (< 10 distinct values) → partial or composite, NOT standalone
UNIQUE constraint needed → let PG create the index from the constraint
Full-text search → GIN on generated tsvector column
```

## Output
- SQL file at `prisma/migrations/<timestamp>_add_<table>_indexes/migration.sql`
- Updated `@@index()` annotations in `prisma/schema.prisma`
- Before/after `EXPLAIN ANALYZE` results documented in PR description
- Unused index report (any index with 0 scans after 7 days in staging is a candidate for removal)

## Quality Checks
- [ ] All new indexes created with `CONCURRENTLY` to avoid table locks in production
- [ ] `IF NOT EXISTS` used on all `CREATE INDEX` statements
- [ ] Composite index column order follows equality-before-sort rule
- [ ] Partial indexes used where only a subset of rows is queried (e.g. `status = 'ACTIVE'`)
- [ ] Index names are descriptive: `<table>_<col1>_<col2>_idx`
- [ ] No index on columns with < 10 distinct values unless it is the leading column in a composite
- [ ] `pg_stat_user_indexes` reviewed after 7 days of production traffic to confirm indexes are being used
- [ ] Write performance impact measured: benchmark INSERT/UPDATE throughput before and after

## Example

```
Scenario: Grade 5 leaderboard query taking 1.2 s on 50k students

Diagnosis: Seq Scan on students — no index on (gradeLevel, totalXP)

Solution:
  CREATE INDEX CONCURRENTLY IF NOT EXISTS students_gradeLevel_totalXP_idx
    ON students ("gradeLevel", "totalXP" DESC)
    WHERE "deletedAt" IS NULL;

Result: 11 ms (99.1% improvement). Zero downtime during creation.
INSERT overhead added: ~0.2 ms per student row (acceptable).
```
