# Skill: Write Database Migration

## Purpose
Define the standard workflow for creating, reviewing, and applying Prisma database migrations in AceQuest. Covers both schema-change migrations (additive, breaking, data) and manual SQL migrations for complex data transformations. Ensures every migration is reversible or at least safe, tested in staging, and deployed atomically in production.

## Used By
- Backend Engineer Agent
- Database Agent
- DevOps Agent

## Inputs
| Field | Type | Description |
| --- | --- | --- |
| `changeType` | `"additive" \ | "breaking" \ | "data"` | Nature of the change |
| `schemaChange` | string | Description of the Prisma schema diff |
| `estimatedRows` | number | Approximate rows affected (informs locking risk) |
| `downtime` | boolean | Whether production downtime is acceptable |
| `stagingVerified` | boolean | Must be true before production apply |

## Procedure / Template

### Step 1 — Determine Migration Strategy

| Change Type | Strategy |
| --- | --- |
| Add nullable column | Additive — single migration, zero downtime |
| Add NOT NULL column without default | Breaking — use two-phase: add nullable → backfill → add constraint |
| Rename column | Breaking — use two-phase: add new column → dual-write → drop old |
| Add index to large table | Use `CREATE INDEX CONCURRENTLY` in custom SQL |
| Backfill data | Separate data migration script with batching |

### Step 2 — Additive Migration (Happy Path)

```bash
# 1. Update prisma/schema.prisma with the new model/field
# 2. Generate and apply the migration
npx prisma migrate dev --name add_skill_mastery_table

# 3. Review the generated SQL before committing
cat prisma/migrations/<timestamp>_add_skill_mastery_table/migration.sql
```

Example generated SQL:
```sql
-- CreateTable
CREATE TABLE "skill_masteries" (
    "id" TEXT NOT NULL,
    "studentId" TEXT NOT NULL,
    "skillId" TEXT NOT NULL,
    "theta" DOUBLE PRECISION NOT NULL DEFAULT 0.0,
    "attempts" INTEGER NOT NULL DEFAULT 0,
    "updatedAt" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "skill_masteries_pkey" PRIMARY KEY ("id")
);

-- CreateIndex
CREATE UNIQUE INDEX "skill_masteries_studentId_skillId_key"
    ON "skill_masteries"("studentId", "skillId");

-- AddForeignKey
ALTER TABLE "skill_masteries"
    ADD CONSTRAINT "skill_masteries_studentId_fkey"
    FOREIGN KEY ("studentId") REFERENCES "students"("id")
    ON DELETE RESTRICT ON UPDATE CASCADE;
```

### Step 3 — Breaking Migration (Two-Phase for Zero Downtime)

**Phase 1 — Add new nullable column, deploy code that writes to BOTH old and new:**

```sql
-- prisma/migrations/20250601_phase1_rename_display_name/migration.sql
ALTER TABLE "students" ADD COLUMN "fullName" TEXT;
```

```typescript
// Dual-write in the service layer during Phase 1 deploy
await prisma.student.update({
  where: { id },
  data: { displayName: name, fullName: name },  // write to both
});
```

**Phase 2 — Backfill, add NOT NULL constraint, drop old column (separate deployment):**

```sql
-- prisma/migrations/20250608_phase2_rename_display_name/migration.sql

-- Backfill any rows that missed the dual-write window
UPDATE "students" SET "fullName" = "displayName" WHERE "fullName" IS NULL;

-- Now safe to add NOT NULL
ALTER TABLE "students" ALTER COLUMN "fullName" SET NOT NULL;

-- Drop old column only after confirming new code reads from fullName exclusively
ALTER TABLE "students" DROP COLUMN "displayName";
```

### Step 4 — Custom SQL Migration (Index CONCURRENTLY)

Prisma does not emit `CONCURRENTLY` — use a custom migration file instead.

```bash
# Create an empty migration
npx prisma migrate dev --create-only --name add_submissions_student_idx
```

Then replace the generated SQL:

```sql
-- prisma/migrations/20250601_add_submissions_student_idx/migration.sql

-- Run outside a transaction so CONCURRENTLY works
-- Note: Prisma wraps migrations in a transaction by default.
-- For CONCURRENTLY, prepend the pragma comment:
-- Migration: { "pragma": "no-transaction" }

CREATE INDEX CONCURRENTLY IF NOT EXISTS "quiz_submissions_studentId_submittedAt_idx"
    ON "quiz_submissions"("studentId", "submittedAt" DESC);
```

Add at the top of the file (Prisma reads this comment):
```sql
-- This migration was created manually. Pragma: no-transaction
```

### Step 5 — Data Migration Script (Batched)

For large-table backfills, use a standalone script instead of a SQL migration to avoid long-running locks.

```typescript
// scripts/backfill-skill-mastery.ts
import { prisma } from "../src/lib/prisma";

const BATCH_SIZE = 500;

async function backfill() {
  let cursor: string | undefined;
  let processed = 0;

  console.log("Starting SkillMastery backfill...");

  while (true) {
    const students = await prisma.student.findMany({
      take: BATCH_SIZE,
      skip: cursor ? 1 : 0,
      cursor: cursor ? { id: cursor } : undefined,
      select: { id: true },
      orderBy: { id: "asc" },
    });

    if (students.length === 0) break;

    const skills = await prisma.skill.findMany({ select: { id: true } });

    await prisma.$transaction(
      students.flatMap((student) =>
        skills.map((skill) =>
          prisma.skillMastery.upsert({
            where: { studentId_skillId: { studentId: student.id, skillId: skill.id } },
            create: { studentId: student.id, skillId: skill.id, theta: 0, attempts: 0 },
            update: {},
          })
        )
      )
    );

    cursor = students[students.length - 1].id;
    processed += students.length;
    console.log(`Processed ${processed} students...`);
  }

  console.log(`Backfill complete. Total: ${processed}`);
}

backfill().catch(console.error).finally(() => prisma.$disconnect());
```

Run:
```bash
npx ts-node scripts/backfill-skill-mastery.ts
```

### Step 6 — Production Deployment Checklist

```bash
# Staging
npx prisma migrate deploy   # applies pending migrations

# Verify
npx prisma db pull --print  # confirm schema matches

# Production (via CI/CD, not manually)
# Set DATABASE_URL to prod connection string
npx prisma migrate deploy
```

### Step 7 — Rollback Strategy

Prisma does not support automatic rollbacks. For safe rollback:
1. Write a compensating migration that reverses the DDL.
2. For data migrations, keep the original data in a staging table (`_backup_<table>_<date>`) before destructive ops.

```sql
-- Backup before destructive operation
CREATE TABLE "_backup_students_20250601" AS SELECT * FROM "students";
```

## Output
- `prisma/migrations/<timestamp>_<name>/migration.sql` — reviewed DDL
- Optional `scripts/backfill-<name>.ts` for data migrations
- Updated `prisma/schema.prisma`
- Migration applied and verified on staging before production PR is merged

## Quality Checks
- [ ] `prisma migrate dev` runs without errors locally
- [ ] Generated SQL reviewed manually — no unexpected `DROP` or `ALTER` without approval
- [ ] Migrations for large tables use `CONCURRENTLY` index creation
- [ ] Breaking changes use two-phase deployment (no downtime)
- [ ] Backfills run in batches of <= 1000 rows to avoid lock escalation
- [ ] `prisma migrate deploy` (not `migrate dev`) is used in CI/CD
- [ ] Staging apply verified before production PR approval
- [ ] Migration name is descriptive: `add_quiz_status_enum`, not `migration1`

## Example

```bash
# Developer workflow for a new column
$ npx prisma migrate dev --name add_student_timezone
Environment variables loaded from .env
Prisma schema loaded from prisma/schema.prisma
Datasource "db": PostgreSQL database "acequest_dev" at "localhost:5432"

Applying migration `20250601120000_add_student_timezone`

The following migration(s) have been created and applied from new schema changes:

migrations/
  └─ 20250601120000_add_student_timezone/
    └─ migration.sql

Your database is now in sync with your schema.
Generated Prisma Client (v5.x.x) to ./node_modules/.prisma/client in 142ms
```
