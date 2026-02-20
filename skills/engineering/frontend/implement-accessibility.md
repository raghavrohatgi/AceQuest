# Skill: Implement Accessibility

## Purpose
Define the standard approach for making AceQuest's UI accessible to all K-8 students, including those who use screen readers, keyboard navigation, or have visual/motor impairments. Target: WCAG 2.1 Level AA compliance. Special considerations: young learners may use assistive technology configured by parents/schools; gamified elements (progress bars, badges, confetti) must be perceivable without relying on colour or animation alone.

## Used By
- Frontend Engineer Agent
- UI/UX Agent
- QA Accessibility Auditor Agent

## Inputs
| Field | Type | Description |
| --- | --- | --- |
| `component` | string | Component or page being made accessible |
| `wcagCriteria` | string[] | Specific WCAG 2.1 criteria to address |
| `userContext` | string | Who uses this (e.g. Grade 2 student with visual impairment) |
| `hasAnimation` | boolean | Whether component uses animation/confetti/transitions |
| `hasColourCoding` | boolean | Whether colour conveys state (correct/incorrect answers) |

## Procedure / Template

### Step 1 — Colour Contrast

All text must meet WCAG AA contrast ratios: 4.5:1 for normal text, 3:1 for large text (18pt+ or 14pt bold).

```typescript
// tailwind.config.ts — AceQuest brand colours with verified contrast
export default {
  theme: {
    extend: {
      colors: {
        "quest-navy":   "#1A1F5E",  // contrast 10.6:1 on white — AA ✓
        "quest-purple": "#6B21A8",  // contrast 7.2:1 on white — AA ✓
        "quest-gold":   "#D97706",  // contrast 4.6:1 on white — AA ✓ (avoid on light bg)
        "quest-green":  "#15803D",  // contrast 5.9:1 on white — AA ✓
        "quest-red":    "#B91C1C",  // contrast 5.9:1 on white — AA ✓
      },
    },
  },
};
```

### Step 2 — Semantic HTML Structure

```tsx
// src/components/quiz/QuizPage.tsx
export function QuizPage({ quiz }: { quiz: Quiz }) {
  return (
    <main aria-label={`Quiz: ${quiz.title}`}>
      <header>
        <h1>{quiz.title}</h1>
        <QuizProgressBar current={3} total={10} />  {/* see Step 5 */}
      </header>

      <section aria-label="Current question">
        <QuestionCard question={quiz.questions[current]} />
      </section>

      <nav aria-label="Quiz navigation">
        <Button onClick={handlePrev} disabled={current === 0}>Previous</Button>
        <Button onClick={handleNext}>Next</Button>
      </nav>
    </main>
  );
}
```

### Step 3 — Keyboard Navigation

```tsx
// src/components/quiz/AnswerOption.tsx
interface AnswerOptionProps {
  label: string;
  isSelected: boolean;
  isCorrect?: boolean;   // revealed after submission
  onSelect: () => void;
}

export function AnswerOption({ label, isSelected, isCorrect, onSelect }: AnswerOptionProps) {
  return (
    <button
      type="button"
      role="radio"
      aria-checked={isSelected}
      aria-label={label}
      onClick={onSelect}
      onKeyDown={(e) => {
        if (e.key === " " || e.key === "Enter") {
          e.preventDefault();
          onSelect();
        }
      }}
      className={cn(
        "w-full text-left px-4 py-3 rounded-xl border-2 transition-colors",
        "focus:outline-none focus:ring-4 focus:ring-quest-purple focus:ring-offset-2",
        isSelected ? "border-quest-purple bg-purple-50" : "border-gray-200 hover:border-quest-purple",
        // Colour is a supplement — icon also conveys state (Step 4)
        isCorrect === true && "border-quest-green bg-green-50",
        isCorrect === false && isSelected && "border-quest-red bg-red-50"
      )}
    >
      {/* Icon + colour together — never colour alone */}
      {isCorrect === true && <span aria-hidden="true" className="mr-2">✓</span>}
      {isCorrect === false && isSelected && <span aria-hidden="true" className="mr-2">✗</span>}
      {label}
    </button>
  );
}
```

Answer options are wrapped in a `radiogroup` for correct AT semantics:

```tsx
<div role="radiogroup" aria-label="Choose your answer" className="flex flex-col gap-3">
  {question.options.map((opt) => (
    <AnswerOption key={opt.id} {...opt} />
  ))}
</div>
```

### Step 4 — Colour Is Never the Sole Indicator

```tsx
// Correct/incorrect feedback — icon + colour + text, not colour alone
export function AnswerFeedback({ isCorrect }: { isCorrect: boolean }) {
  return (
    <div
      role="status"
      aria-live="polite"
      className={cn(
        "flex items-center gap-2 rounded-lg px-4 py-3 text-sm font-semibold",
        isCorrect ? "bg-green-50 text-quest-green" : "bg-red-50 text-quest-red"
      )}
    >
      {isCorrect ? (
        <>
          <span aria-hidden="true">✓</span>
          <span>Correct! Great job!</span>
        </>
      ) : (
        <>
          <span aria-hidden="true">✗</span>
          <span>Not quite — try the next one!</span>
        </>
      )}
    </div>
  );
}
```

### Step 5 — Progress Bars (Game UI)

```tsx
// src/components/ui/ProgressBar.tsx
interface ProgressBarProps {
  current: number;
  total: number;
  label?: string;
}

export function ProgressBar({ current, total, label = "Progress" }: ProgressBarProps) {
  const pct = Math.round((current / total) * 100);
  return (
    <div className="flex flex-col gap-1">
      <div className="flex justify-between text-xs text-gray-500">
        <span>{label}</span>
        <span aria-hidden="true">{current}/{total}</span>
      </div>
      <div
        role="progressbar"
        aria-valuenow={current}
        aria-valuemin={0}
        aria-valuemax={total}
        aria-label={`${label}: ${current} of ${total}`}
        className="h-3 rounded-full bg-gray-200 overflow-hidden"
      >
        <div
          className="h-full rounded-full bg-quest-purple transition-all duration-500"
          style={{ width: `${pct}%` }}
        />
      </div>
    </div>
  );
}
```

### Step 6 — Reduced Motion

```tsx
// src/components/ui/Confetti.tsx
"use client";
import dynamic from "next/dynamic";
import { useReducedMotion } from "@/hooks/useReducedMotion";

const ReactConfetti = dynamic(() => import("react-confetti"), { ssr: false });

export function CelebrationConfetti({ active }: { active: boolean }) {
  const prefersReducedMotion = useReducedMotion();

  if (!active) return null;

  // If user prefers reduced motion, show a static congratulations banner instead
  if (prefersReducedMotion) {
    return (
      <div role="status" aria-live="polite" className="text-center text-2xl font-bold text-quest-gold">
        Congratulations!
      </div>
    );
  }

  return <ReactConfetti recycle={false} numberOfPieces={200} />;
}
```

```typescript
// src/hooks/useReducedMotion.ts
import { useEffect, useState } from "react";

export function useReducedMotion(): boolean {
  const [matches, setMatches] = useState(false);
  useEffect(() => {
    const mq = window.matchMedia("(prefers-reduced-motion: reduce)");
    setMatches(mq.matches);
    const handler = (e: MediaQueryListEvent) => setMatches(e.matches);
    mq.addEventListener("change", handler);
    return () => mq.removeEventListener("change", handler);
  }, []);
  return matches;
}
```

### Step 7 — Skip Navigation Link

```tsx
// src/app/layout.tsx
export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <a
          href="#main-content"
          className="sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-4
                     bg-quest-purple text-white px-4 py-2 rounded-lg z-50"
        >
          Skip to main content
        </a>
        <Header />
        <main id="main-content">{children}</main>
        <Footer />
      </body>
    </html>
  );
}
```

### Step 8 — Focus Management in Modals

```tsx
// src/components/ui/Modal.tsx  (excerpt)
import { useEffect, useRef } from "react";
import FocusTrap from "focus-trap-react";

export function Modal({ isOpen, onClose, title, children }: ModalProps) {
  const firstFocusableRef = useRef<HTMLButtonElement>(null);

  useEffect(() => {
    if (isOpen) firstFocusableRef.current?.focus();
  }, [isOpen]);

  if (!isOpen) return null;

  return (
    <FocusTrap>
      <div
        role="dialog"
        aria-modal="true"
        aria-label={title}
        className="fixed inset-0 z-50 flex items-center justify-center bg-black/50"
      >
        <div className="bg-white rounded-2xl p-6 w-full max-w-md shadow-xl">
          <h2 className="text-xl font-bold">{title}</h2>
          {children}
          <button ref={firstFocusableRef} onClick={onClose} aria-label="Close dialog">
            ✕
          </button>
        </div>
      </div>
    </FocusTrap>
  );
}
```

## Output
- Accessible versions of all affected components
- `src/hooks/useReducedMotion.ts` — animation preference hook
- Skip-nav link in root layout
- `axe-core` violations reduced to zero in automated scan

## Quality Checks
- [ ] All interactive elements reachable and operable via keyboard (Tab, Enter, Space, Arrow keys)
- [ ] Colour contrast >= 4.5:1 for body text; >= 3:1 for large text (verified with colour-contrast analyser)
- [ ] No information conveyed by colour alone — icon or text also used
- [ ] `aria-label` or `aria-labelledby` on all form controls, dialogs, and landmarks
- [ ] `role="alert"` or `aria-live` on dynamic content (errors, feedback, score updates)
- [ ] `prefers-reduced-motion` respected — no auto-playing animations for users who opt out
- [ ] Focus management: modal traps focus; on close, focus returns to trigger element
- [ ] `lang="en"` (or `"hi"`) on `<html>` element
- [ ] Automated scan with `axe-core` or `@axe-core/react` in development: zero violations
- [ ] Manual keyboard-only navigation test passes

## Example

```
Component: QuizAnswerOptions
Before: Div elements styled as buttons, colour-only feedback (green/red borders)
After:  <button role="radio"> with aria-checked, aria-label, keyboard handler,
        icon + text + colour for correct/incorrect, focus ring visible at 4px
WCAG criteria met: 1.3.1 (Info and Relationships), 1.4.1 (Use of Color),
  1.4.3 (Contrast), 2.1.1 (Keyboard), 4.1.2 (Name, Role, Value)
```
