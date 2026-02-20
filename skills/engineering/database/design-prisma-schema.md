# Skill: Design Prisma Schema

## Purpose
Define the standard approach for designing, extending, and documenting Prisma schemas for AceQuest's PostgreSQL database. Ensures models are normalised to at least 3NF, relations are correctly typed, soft-delete and audit patterns are applied consistently, and the schema compiles without errors before migration.

## Used By
- Backend Engineer Agent
- Database Agent
- Full-Stack Engineer Agent

## Inputs
| Field | Type | Description |
| --- | --- | --- |
| `domain` | string | Domain being modelled, e.g. `quiz`, `badge`, `subscription` |
| `entities` | string[] | List of entities, e.g. `["Quiz","Question","Option","Submission"]` |
| `relations` | object[] | Entity relationships with cardinality |
| `softDelete` | boolean | Whether entities should use soft-delete (`deletedAt`) |
| `auditFields` | boolean | Whether to include `createdAt` / `updatedAt` on all models |

## Procedure / Template

### Step 1 — Scaffold the Schema File

AceQuest uses a single `schema.prisma` file. Add new models at the bottom; never delete existing models.

```prisma
// prisma/schema.prisma

generator client {
  provider        = "prisma-client-js"
  previewFeatures = ["fullTextSearch", "fullTextIndex"]
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}
```

### Step 2 — Core User / Auth Models

```prisma
model User {
  id           String    @id @default(uuid())
  email        String    @unique
  phoneNumber  String?   @unique
  passwordHash String
  role         UserRole  @default(STUDENT)
  isVerified   Boolean   @default(false)
  createdAt    DateTime  @default(now())
  updatedAt    DateTime  @updatedAt
  deletedAt    DateTime?

  student Student?
  teacher Teacher?

  @@index([email])
  @@index([phoneNumber])
  @@map("users")
}

enum UserRole {
  STUDENT
  TEACHER
  PARENT
  ADMIN
}
```

### Step 3 — Student Profile and Progress Models

```prisma
model Student {
  id             String    @id @default(uuid())
  userId         String    @unique
  user           User      @relation(fields: [userId], references: [id], onDelete: Cascade)
  displayName    String
  gradeLevel     Int       // 1-8 for K-8
  dateOfBirth    DateTime?
  avatarUrl      String?
  totalXP        Int       @default(0)
  currentStreak  Int       @default(0)
  longestStreak  Int       @default(0)
  lastActiveDate DateTime?
  createdAt      DateTime  @default(now())
  updatedAt      DateTime  @updatedAt

  quizSubmissions QuizSubmission[]
  xpEvents        XPEvent[]
  badges          StudentBadge[]
  skillMasteries  SkillMastery[]

  @@index([totalXP(sort: Desc)])
  @@index([gradeLevel])
  @@map("students")
}
```

### Step 4 — Quiz and Question Models

```prisma
model Quiz {
  id          String     @id @default(uuid())
  title       String
  topicId     String
  topic       Topic      @relation(fields: [topicId], references: [id])
  gradeLevel  Int
  status      QuizStatus @default(DRAFT)
  timeLimit   Int?       // seconds; null = untimed
  createdAt   DateTime   @default(now())
  updatedAt   DateTime   @updatedAt
  deletedAt   DateTime?

  questions   Question[]
  submissions QuizSubmission[]

  @@index([topicId])
  @@index([gradeLevel, status])
  @@map("quizzes")
}

enum QuizStatus {
  DRAFT
  ACTIVE
  ARCHIVED
}

model Question {
  id          String       @id @default(uuid())
  quizId      String
  quiz        Quiz         @relation(fields: [quizId], references: [id], onDelete: Cascade)
  text        String
  imageUrl    String?
  difficulty  Float        // IRT b parameter, range -3 to 3
  type        QuestionType @default(MULTIPLE_CHOICE)
  explanation String?
  createdAt   DateTime     @default(now())
  updatedAt   DateTime     @updatedAt

  options     Option[]
  answerLogs  SubmissionAnswer[]

  @@index([quizId])
  @@index([difficulty])
  @@map("questions")
}

enum QuestionType {
  MULTIPLE_CHOICE
  TRUE_FALSE
  FILL_IN_THE_BLANK
}

model Option {
  id         String   @id @default(uuid())
  questionId String
  question   Question @relation(fields: [questionId], references: [id], onDelete: Cascade)
  text       String
  isCorrect  Boolean  @default(false)
  order      Int      @default(0)

  answerLogs SubmissionAnswer[]

  @@index([questionId])
  @@map("options")
}
```

### Step 5 — Submission Models

```prisma
model QuizSubmission {
  id           String    @id @default(uuid())
  studentId    String
  student      Student   @relation(fields: [studentId], references: [id])
  quizId       String
  quiz         Quiz      @relation(fields: [quizId], references: [id])
  sessionId    String    @unique  // idempotency key
  score        Int       // 0-100
  correctCount Int
  totalCount   Int
  submittedAt  DateTime  @default(now())

  answers SubmissionAnswer[]
  xpEvent XPEvent?

  @@index([studentId, submittedAt(sort: Desc)])
  @@index([quizId])
  @@map("quiz_submissions")
}

model SubmissionAnswer {
  id               String         @id @default(uuid())
  submissionId     String
  submission       QuizSubmission @relation(fields: [submissionId], references: [id], onDelete: Cascade)
  questionId       String
  question         Question       @relation(fields: [questionId], references: [id])
  selectedOptionId String
  selectedOption   Option         @relation(fields: [selectedOptionId], references: [id])
  isCorrect        Boolean
  timeTakenMs      Int

  @@index([submissionId])
  @@index([questionId, isCorrect])
  @@map("submission_answers")
}
```

### Step 6 — Gamification Models

```prisma
model Badge {
  id          String  @id @default(uuid())
  slug        String  @unique
  name        String
  description String
  iconUrl     String
  xpReward    Int     @default(0)
  rarity      BadgeRarity @default(COMMON)
  createdAt   DateTime @default(now())

  studentBadges StudentBadge[]

  @@map("badges")
}

enum BadgeRarity {
  COMMON
  RARE
  EPIC
  LEGENDARY
}

model StudentBadge {
  studentId  String
  student    Student  @relation(fields: [studentId], references: [id])
  badgeId    String
  badge      Badge    @relation(fields: [badgeId], references: [id])
  awardedAt  DateTime @default(now())

  @@id([studentId, badgeId])
  @@map("student_badges")
}

model XPEvent {
  id           String         @id @default(uuid())
  studentId    String
  student      Student        @relation(fields: [studentId], references: [id])
  source       XPSource
  referenceId  String         // FK to quiz_submission, badge, etc.
  amount       Int
  createdAt    DateTime       @default(now())
  submissionId String?        @unique
  submission   QuizSubmission? @relation(fields: [submissionId], references: [id])

  @@index([studentId, createdAt(sort: Desc)])
  @@map("xp_events")
}

enum XPSource {
  QUIZ
  STREAK
  BADGE
  DAILY_GOAL
  REFERRAL
}
```

### Step 7 — Adaptive Learning Model

```prisma
model SkillMastery {
  id         String   @id @default(uuid())
  studentId  String
  student    Student  @relation(fields: [studentId], references: [id])
  skillId    String
  skill      Skill    @relation(fields: [skillId], references: [id])
  theta      Float    @default(0.0)   // IRT ability estimate
  attempts   Int      @default(0)
  updatedAt  DateTime @updatedAt

  @@unique([studentId, skillId])
  @@index([studentId])
  @@map("skill_masteries")
}
```

## Output
- Updated `prisma/schema.prisma` with new models
- `prisma/migrations/<timestamp>_<description>/migration.sql` (generated by `prisma migrate dev`)
- Regenerated Prisma client types

## Quality Checks
- [ ] `prisma validate` passes with zero errors
- [ ] Every model has `@@map()` with snake_case table name
- [ ] All foreign keys specify `onDelete` behaviour explicitly
- [ ] UUID primary keys used (`@default(uuid())`)
- [ ] `createdAt` / `updatedAt` on all mutable models
- [ ] `deletedAt DateTime?` on models that require soft-delete
- [ ] Composite indexes defined for common query patterns (multi-column WHERE clauses)
- [ ] Enum values are SCREAMING_SNAKE_CASE
- [ ] No circular required relations
- [ ] `prisma migrate dev --name <description>` run in development before committing

## Example

```bash
# Validate the schema
npx prisma validate

# Generate migration
npx prisma migrate dev --name add_quiz_submission_models

# Regenerate client
npx prisma generate
```
