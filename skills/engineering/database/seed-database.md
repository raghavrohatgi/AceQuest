# Skill: Seed Database

## Purpose
Define a reproducible, idempotent method for populating AceQuest's development, staging, and test databases with realistic fixture data. Seeds must cover all game mechanics (XP, badges, streaks, adaptive questions, grade levels 1-8) so that any engineer can spin up a fully functional local environment from scratch.

## Used By
- Backend Engineer Agent
- QA Agent
- DevOps Agent

## Inputs
| Field | Type | Description |
| --- | --- | --- |
| `environment` | `"development" \ | "test" \ | "staging"` | Target environment |
| `gradeRange` | `[number, number]` | Grade levels to generate, e.g. `[1, 8]` |
| `studentsPerGrade` | number | Number of student accounts per grade |
| `quizzesPerTopic` | number | Number of quizzes per topic |
| `questionsPerQuiz` | number | Number of questions per quiz |

## Procedure / Template

### Step 1 — Install Seed Utilities

```bash
npm install --save-dev @faker-js/faker
```

### Step 2 — Seed Entry Point

```typescript
// prisma/seed.ts
import { PrismaClient } from "@prisma/client";
import { seedUsers } from "./seeds/users";
import { seedTopics } from "./seeds/topics";
import { seedQuizzes } from "./seeds/quizzes";
import { seedBadges } from "./seeds/badges";
import { seedStudentProgress } from "./seeds/studentProgress";

const prisma = new PrismaClient();

async function main() {
  console.log("🌱 Starting database seed...");

  // Order matters — respect FK dependencies
  await seedTopics(prisma);
  console.log("  ✓ Topics");

  await seedBadges(prisma);
  console.log("  ✓ Badges");

  await seedUsers(prisma, { studentsPerGrade: 10, grades: [1, 2, 3, 4, 5, 6, 7, 8] });
  console.log("  ✓ Users & Students");

  await seedQuizzes(prisma, { quizzesPerTopic: 3, questionsPerQuiz: 10 });
  console.log("  ✓ Quizzes & Questions");

  await seedStudentProgress(prisma);
  console.log("  ✓ Submissions & Progress");

  console.log("🌱 Seed complete.");
}

main()
  .catch((err) => { console.error(err); process.exit(1); })
  .finally(() => prisma.$disconnect());
```

Register in `package.json`:
```json
{
  "prisma": {
    "seed": "ts-node --compiler-options {\"module\":\"CommonJS\"} prisma/seed.ts"
  }
}
```

### Step 3 — Topics Seed (Idempotent)

```typescript
// prisma/seeds/topics.ts
import { PrismaClient } from "@prisma/client";

export const TOPICS = [
  { slug: "mathematics-grade1", name: "Mathematics – Grade 1", gradeLevel: 1 },
  { slug: "mathematics-grade2", name: "Mathematics – Grade 2", gradeLevel: 2 },
  { slug: "english-grade1",     name: "English – Grade 1",     gradeLevel: 1 },
  { slug: "english-grade2",     name: "English – Grade 2",     gradeLevel: 2 },
  { slug: "science-grade3",     name: "Science – Grade 3",     gradeLevel: 3 },
  { slug: "mathematics-grade5", name: "Mathematics – Grade 5", gradeLevel: 5 },
  { slug: "social-studies-g6",  name: "Social Studies – Grade 6", gradeLevel: 6 },
  { slug: "hindi-grade4",       name: "Hindi – Grade 4",       gradeLevel: 4 },
];

export async function seedTopics(prisma: PrismaClient) {
  for (const topic of TOPICS) {
    await prisma.topic.upsert({
      where: { slug: topic.slug },
      create: topic,
      update: {},
    });
  }
}
```

### Step 4 — Users & Students Seed

```typescript
// prisma/seeds/users.ts
import { PrismaClient } from "@prisma/client";
import { faker } from "@faker-js/faker/locale/en_IN";  // Indian locale for realistic names
import bcrypt from "bcrypt";

interface UserSeedOptions {
  studentsPerGrade: number;
  grades: number[];
}

// Deterministic password for dev — never use in production
const DEV_PASSWORD_HASH = bcrypt.hashSync("AceQuest@dev123", 10);

export async function seedUsers(prisma: PrismaClient, opts: UserSeedOptions) {
  // Seed admin
  await prisma.user.upsert({
    where: { email: "admin@acequest.in" },
    create: {
      email: "admin@acequest.in",
      passwordHash: DEV_PASSWORD_HASH,
      role: "ADMIN",
      isVerified: true,
    },
    update: {},
  });

  // Seed one teacher per grade
  for (const grade of opts.grades) {
    const email = `teacher.grade${grade}@acequest.in`;
    await prisma.user.upsert({
      where: { email },
      create: {
        email,
        passwordHash: DEV_PASSWORD_HASH,
        role: "TEACHER",
        isVerified: true,
        teacher: { create: { displayName: faker.person.fullName(), gradeLevel: grade } },
      },
      update: {},
    });
  }

  // Seed students
  for (const grade of opts.grades) {
    for (let i = 0; i < opts.studentsPerGrade; i++) {
      const firstName = faker.person.firstName();
      const email = `student.g${grade}.${i + 1}@acequest.in`;

      await prisma.user.upsert({
        where: { email },
        create: {
          email,
          passwordHash: DEV_PASSWORD_HASH,
          role: "STUDENT",
          isVerified: true,
          student: {
            create: {
              displayName: firstName,
              gradeLevel: grade,
              totalXP: faker.number.int({ min: 0, max: 5000 }),
              currentStreak: faker.number.int({ min: 0, max: 30 }),
            },
          },
        },
        update: {},
      });
    }
  }
}
```

### Step 5 — Quizzes & Questions Seed

```typescript
// prisma/seeds/quizzes.ts
import { PrismaClient } from "@prisma/client";
import { faker } from "@faker-js/faker";
import { TOPICS } from "./topics";

const QUESTION_TEMPLATES: Record<number, () => { text: string; options: string[]; correctIndex: number }> = {
  1: () => ({
    text: `What is ${faker.number.int({ min: 1, max: 9 })} + ${faker.number.int({ min: 1, max: 9 })}?`,
    options: ["4", "7", "12", "15"],
    correctIndex: 1,
  }),
};

interface QuizSeedOptions { quizzesPerTopic: number; questionsPerQuiz: number; }

export async function seedQuizzes(prisma: PrismaClient, opts: QuizSeedOptions) {
  const topics = await prisma.topic.findMany();

  for (const topic of topics) {
    for (let q = 0; q < opts.quizzesPerTopic; q++) {
      const quiz = await prisma.quiz.upsert({
        where: { id: `seed-quiz-${topic.slug}-${q}` },
        create: {
          id: `seed-quiz-${topic.slug}-${q}`,
          title: `${topic.name} – Quiz ${q + 1}`,
          topicId: topic.id,
          gradeLevel: topic.gradeLevel,
          status: "ACTIVE",
          timeLimit: 600,
        },
        update: {},
      });

      for (let qi = 0; qi < opts.questionsPerQuiz; qi++) {
        const difficulty = parseFloat(faker.number.float({ min: -2, max: 2, fractionDigits: 2 }).toFixed(2));
        const qId = `seed-q-${quiz.id}-${qi}`;

        await prisma.question.upsert({
          where: { id: qId },
          create: {
            id: qId,
            quizId: quiz.id,
            text: `Sample question ${qi + 1} for ${topic.name}`,
            difficulty,
            type: "MULTIPLE_CHOICE",
            options: {
              createMany: {
                data: [
                  { text: "Option A", isCorrect: true,  order: 0 },
                  { text: "Option B", isCorrect: false, order: 1 },
                  { text: "Option C", isCorrect: false, order: 2 },
                  { text: "Option D", isCorrect: false, order: 3 },
                ],
              },
            },
          },
          update: {},
        });
      }
    }
  }
}
```

### Step 6 — Badges Seed

```typescript
// prisma/seeds/badges.ts
import { PrismaClient } from "@prisma/client";

const BADGES = [
  { slug: "first-quiz",     name: "First Quiz!",      rarity: "COMMON",    xpReward: 50,  description: "Complete your first quiz." },
  { slug: "quiz-master",    name: "Quiz Master",       rarity: "RARE",      xpReward: 200, description: "Score 100% on any quiz." },
  { slug: "week-streak",    name: "7-Day Streak",      rarity: "RARE",      xpReward: 300, description: "Log in 7 days in a row." },
  { slug: "month-streak",   name: "30-Day Streak",     rarity: "EPIC",      xpReward: 1000, description: "30-day login streak." },
  { slug: "speed-demon",    name: "Speed Demon",       rarity: "COMMON",    xpReward: 75,  description: "Complete a quiz in under 2 minutes." },
  { slug: "perfect-ten",    name: "Perfect 10",        rarity: "LEGENDARY", xpReward: 500, description: "Score 100% on 10 quizzes." },
];

export async function seedBadges(prisma: PrismaClient) {
  for (const badge of BADGES) {
    await prisma.badge.upsert({
      where: { slug: badge.slug },
      create: { ...badge, iconUrl: `/badges/${badge.slug}.svg` },
      update: {},
    });
  }
}
```

### Step 7 — Run the Seed

```bash
# Reset dev DB and reseed from scratch
npx prisma migrate reset --force

# Seed without reset (idempotent)
npx prisma db seed
```

## Output
- `prisma/seed.ts` — orchestrator
- `prisma/seeds/topics.ts`, `users.ts`, `quizzes.ts`, `badges.ts`, `studentProgress.ts`
- All seeds are idempotent (use `upsert` not `create`)
- Dev database populated with at least 80 students, 24 quizzes, 240 questions, 6 badges

## Quality Checks
- [ ] All seeds use `upsert` with deterministic IDs — running twice is safe
- [ ] Seed emails follow pattern `<role>.g<grade>.<n>@acequest.in` for easy identification
- [ ] FK order respected: Topics → Badges → Users → Quizzes → Submissions
- [ ] Indian locale used for faker names (`@faker-js/faker/locale/en_IN`)
- [ ] Dev password documented in README; never the same as staging
- [ ] `prisma db seed` completes in under 60 seconds for default config
- [ ] Seed script does not run in `production` environment (guard at top of seed.ts)

## Example

```bash
$ npx prisma db seed
Running seed command `ts-node ... prisma/seed.ts` ...
🌱 Starting database seed...
  ✓ Topics (8 records)
  ✓ Badges (6 records)
  ✓ Users & Students (80 students + 8 teachers + 1 admin)
  ✓ Quizzes & Questions (24 quizzes, 240 questions)
  ✓ Submissions & Progress
🌱 Seed complete.
```
