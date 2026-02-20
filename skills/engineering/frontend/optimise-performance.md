# Skill: Optimise Frontend Performance

## Purpose
Provide a systematic procedure for measuring and improving the performance of AceQuest's Next.js 14 frontend. Performance is critical for K-8 students on low-bandwidth mobile connections across India. Targets: LCP < 2.5 s, CLS < 0.1, FID/INP < 200 ms, bundle size < 200 KB (initial JS), Lighthouse score >= 90 on mobile.

## Used By
- Frontend Engineer Agent
- Full-Stack Engineer Agent
- Performance Review Agent

## Inputs
| Field | Type | Description |
| --- | --- | --- |
| `page` | string | Next.js page/route being optimised, e.g. `/dashboard` |
| `currentLCP` | number | Current Largest Contentful Paint in ms |
| `currentBundleKB` | number | Current initial JS bundle size in KB |
| `primaryDevice` | string | Target device profile, e.g. `"low-end Android, 4G"` |
| `imageHeavy` | boolean | Whether the page has many images (game assets, badges) |

## Procedure / Template

### Step 1 — Measure Baseline

```bash
# Lighthouse CI
npm install --save-dev @lhci/cli
npx lhci autorun --collect.url=http://localhost:3000/dashboard

# Bundle analysis
npm install --save-dev @next/bundle-analyzer
ANALYZE=true next build
```

```javascript
// next.config.js
const withBundleAnalyzer = require("@next/bundle-analyzer")({
  enabled: process.env.ANALYZE === "true",
});
module.exports = withBundleAnalyzer({ /* nextConfig */ });
```

Record baseline metrics in the PR description before any changes.

### Step 2 — Image Optimisation

```tsx
// BEFORE — unoptimised
<img src="/badges/quiz-master.png" width={80} height={80} />

// AFTER — Next.js Image with priority for above-the-fold
import Image from "next/image";

<Image
  src="/badges/quiz-master.png"
  alt="Quiz Master badge — awarded for scoring 100% on any quiz"
  width={80}
  height={80}
  priority={isAboveTheFold}   // true for hero images, false for badge list items
  sizes="(max-width: 768px) 80px, 80px"
  className="rounded-full"
/>
```

Convert game assets to WebP/AVIF at build time:
```bash
npm install --save-dev sharp
# Next.js uses sharp automatically for Image component optimisation
```

### Step 3 — Code Splitting and Lazy Loading

```tsx
// Dynamic import for heavy components (e.g. quiz game engine)
import dynamic from "next/dynamic";

const QuizGameBoard = dynamic(
  () => import("@/components/quiz/QuizGameBoard"),
  {
    loading: () => <QuizGameBoardSkeleton />,
    ssr: false,   // client-only interactive component
  }
);

// Lazy load heavy third-party libraries
const Confetti = dynamic(() => import("react-confetti"), { ssr: false });
```

### Step 4 — Server Components vs Client Components

Move data-fetching and static rendering to Server Components; keep interactivity in Client Components.

```tsx
// src/app/dashboard/page.tsx  — Server Component (default in App Router)
import { getStudentStats } from "@/lib/data/student";
import { LeaderboardCard } from "@/components/dashboard/LeaderboardCard";
import { QuizGrid } from "@/components/quiz/QuizGrid";

export default async function DashboardPage() {
  // Runs on the server — no client JS for this fetch
  const stats = await getStudentStats();
  return (
    <main>
      <LeaderboardCard stats={stats} />  {/* Server Component */}
      <QuizGrid />                        {/* Server Component */}
    </main>
  );
}

// src/components/quiz/QuizTimer.tsx  — Client Component (needs state/effects)
"use client";
import { useState, useEffect } from "react";

export function QuizTimer({ durationSeconds }: { durationSeconds: number }) {
  const [remaining, setRemaining] = useState(durationSeconds);
  useEffect(() => {
    const id = setInterval(() => setRemaining((r) => Math.max(0, r - 1)), 1000);
    return () => clearInterval(id);
  }, []);
  return <div aria-label={`Time remaining: ${remaining} seconds`}>{remaining}s</div>;
}
```

### Step 5 — Caching Strategy

```typescript
// src/lib/data/quiz.ts — Next.js data caching
export async function getActiveQuizzes(gradeLevel: number) {
  const res = await fetch(
    `${process.env.API_BASE_URL}/api/v1/quizzes?gradeLevel=${gradeLevel}&status=ACTIVE`,
    {
      next: {
        revalidate: 300,   // ISR: revalidate every 5 minutes
        tags: [`quizzes-grade-${gradeLevel}`],
      },
    }
  );
  return res.json();
}

// On-demand revalidation after admin publishes a new quiz
import { revalidateTag } from "next/cache";
export async function publishQuiz(quizId: string, gradeLevel: number) {
  await fetch(`/api/v1/quizzes/${quizId}/publish`, { method: "POST" });
  revalidateTag(`quizzes-grade-${gradeLevel}`);
}
```

### Step 6 — Reduce Layout Shift (CLS)

```tsx
// Always specify width and height for images — prevents layout shift
<Image src="..." width={80} height={80} alt="..." />

// Reserve space for async-loaded content with skeletons
export function BadgeListSkeleton() {
  return (
    <div className="grid grid-cols-4 gap-4">
      {Array.from({ length: 8 }).map((_, i) => (
        <div key={i} className="w-20 h-20 rounded-full bg-gray-200 animate-pulse" />
      ))}
    </div>
  );
}
```

### Step 7 — Font Optimisation

```typescript
// src/app/layout.tsx
import { Inter, Nunito } from "next/font/google";

const nunito = Nunito({
  subsets: ["latin"],
  variable: "--font-nunito",
  display: "swap",   // prevents invisible text during font load
  preload: true,
});
```

### Step 8 — Tailwind CSS Purging

```javascript
// tailwind.config.ts
export default {
  content: [
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  // content array ensures unused classes are purged in production build
};
```

### Step 9 — Memoisation for Expensive Renders

```tsx
import { memo, useMemo } from "react";

// Memoize list items to avoid re-renders when parent updates
export const LeaderboardRow = memo(function LeaderboardRow({ student }: { student: Student }) {
  return (
    <tr>
      <td>{student.rank}</td>
      <td>{student.displayName}</td>
      <td>{student.totalXP.toLocaleString("en-IN")} XP</td>
    </tr>
  );
});

// Expensive computation — memoize result
const sortedStudents = useMemo(
  () => [...students].sort((a, b) => b.totalXP - a.totalXP),
  [students]
);
```

## Output
- Lighthouse CI report: before and after scores
- Bundle analysis screenshots showing reduced chunk sizes
- Updated page components using Server Components where possible
- Dynamic imports for heavy components
- Image components converted to `next/image`

## Quality Checks
- [ ] LCP < 2.5 s on simulated Moto G4 + 4G throttling in Chrome DevTools
- [ ] CLS < 0.1: all images have explicit dimensions; skeletons reserve space
- [ ] INP < 200 ms: no long tasks blocking the main thread during user interaction
- [ ] Initial JS bundle < 200 KB gzipped (verify with bundle analyzer)
- [ ] No `"use client"` on components that don't need interactivity
- [ ] All images use `next/image` with `alt` text and `sizes` attribute
- [ ] `next/font` used for all Google Fonts — zero layout shift from font load
- [ ] ISR revalidation periods documented with rationale
- [ ] Lighthouse score >= 90 Performance on mobile emulation

## Example

```
Page: /dashboard (Grade 5 student)
Before: LCP 4.1 s, JS 380 KB, Lighthouse 58
Changes: Server Components, lazy QuizGameBoard, next/image, ISR 5 min
After:  LCP 1.9 s, JS 145 KB, Lighthouse 94

Key wins:
- QuizGameBoard (120 KB) now lazy-loaded on user interaction
- Hero badge image now served as WebP via next/image
- Student stats fetched on server — 0 KB client JS for that data
```
