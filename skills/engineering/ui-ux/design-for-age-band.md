# Skill: Design for Age Band

## Purpose
Define design guidelines and decision rules for adapting AceQuest's UI to different K-8 age bands. The same underlying feature (quiz, leaderboard, badge) must be presented differently for a 6-year-old in Grade 1 versus a 13-year-old in Grade 8. This skill ensures age-appropriate typography, iconography, interaction complexity, copy tone, and gamification intensity.

## Used By
- UI/UX Designer Agent
- Frontend Engineer Agent
- Content Agent

## Inputs
| Field | Type | Description |
|-------|------|-------------|
| `ageBand` | `"band-1" \| "band-2" \| "band-3"` | Target age group (see bands below) |
| `feature` | string | Feature being designed, e.g. "Quiz results screen" |
| `gradeRange` | `[number, number]` | Grade levels within the band |
| `readingLevel` | string | Expected reading level, e.g. "Grade 2 independent reader" |

## Age Band Definitions

| Band | Grades | Ages | Descriptor |
|------|--------|------|------------|
| Band 1 | K–2 | 5–8 | Young Explorer |
| Band 2 | 3–5 | 8–11 | Curious Learner |
| Band 3 | 6–8 | 11–14 | Ambitious Achiever |

## Procedure / Template

### Step 1 — Typography Scale

```typescript
// src/design-system/typography.ts
export const typographyByBand = {
  "band-1": {
    // Large, clear, child-friendly rounded font
    fontFamily: "'Nunito', 'Comic Sans MS', sans-serif",
    bodySize: "18px",        // larger for emerging readers
    headingSize: "32px",
    lineHeight: "1.8",       // generous leading for early readers
    letterSpacing: "0.02em", // slight tracking aids readability
    fontWeight: "600",       // semi-bold; avoid thin weights
  },
  "band-2": {
    fontFamily: "'Nunito', sans-serif",
    bodySize: "16px",
    headingSize: "28px",
    lineHeight: "1.6",
    letterSpacing: "normal",
    fontWeight: "500",
  },
  "band-3": {
    fontFamily: "'Inter', sans-serif",  // more professional feel for tweens
    bodySize: "15px",
    headingSize: "24px",
    lineHeight: "1.5",
    letterSpacing: "normal",
    fontWeight: "400",
  },
};
```

### Step 2 — Colour and Visual Density

```typescript
export const visualStyleByBand = {
  "band-1": {
    // High saturation, primary colours, large tap targets
    palette: "bright",               // bold yellows, pinks, greens
    iconSize: "48px",                // large icons for small fingers
    borderRadius: "20px",            // very rounded, friendly
    shadowStrength: "strong",        // emphasised depth
    animationIntensity: "high",      // bouncy, frequent celebrations
    illustrationStyle: "character",  // animal characters, friendly faces
    colourCount: "many",             // multiple colours on a single screen OK
  },
  "band-2": {
    palette: "vibrant",
    iconSize: "36px",
    borderRadius: "12px",
    shadowStrength: "medium",
    animationIntensity: "medium",
    illustrationStyle: "adventure",  // landscapes, quests, exploration
    colourCount: "moderate",
  },
  "band-3": {
    palette: "rich",                 // deeper, more sophisticated tones
    iconSize: "24px",
    borderRadius: "8px",
    shadowStrength: "subtle",
    animationIntensity: "low",       // subtle transitions; over-animation feels childish to tweens
    illustrationStyle: "achievement",// trophies, stats, progress charts
    colourCount: "few",              // 2-3 accent colours; cleaner
  },
};
```

### Step 3 — Copy / Tone Guidelines

```typescript
export const copyToneByBand = {
  "band-1": {
    successMessage: ["Yay! You did it! 🌟", "WOW! Superstar! ⭐", "Amazing! 🎉"],
    failureMessage: ["Oops! Let's try again! 😊", "So close! Give it another go!"],
    instructionStyle: "imperative-simple",  // "Tap the right answer!"
    wordLimit: 8,                           // per instruction sentence
    useEmoji: true,
    useCharacters: true,                    // Buddy the owl mascot speaks
    readingLevelTarget: "Grade 1",
  },
  "band-2": {
    successMessage: ["Great job! You scored {score}%! 🎉", "Excellent! Keep it up!"],
    failureMessage: ["Nice try! Practice makes perfect.", "You'll get it next time!"],
    instructionStyle: "friendly-direct",
    wordLimit: 15,
    useEmoji: true,
    useCharacters: false,
    readingLevelTarget: "Grade 3",
  },
  "band-3": {
    successMessage: ["Score: {score}% — Well done.", "Achievement unlocked: {badge}"],
    failureMessage: ["{score}% — Review the explanations to improve.", "Keep practicing!"],
    instructionStyle: "peer-level",         // not talking down; treat as capable
    wordLimit: 25,
    useEmoji: false,                        // tweens find emoji patronising
    useCharacters: false,
    readingLevelTarget: "Grade 6",
  },
};
```

### Step 4 — Interaction Complexity

```typescript
export const interactionByBand = {
  "band-1": {
    minTapTargetPx: 56,         // WCAG + small motor control allowance
    maxOptionsPerQuestion: 3,   // 3 options max (A/B/C)
    hasTimer: false,            // no time pressure for young learners
    questionTypes: ["MULTIPLE_CHOICE"],  // no fill-in-the-blank
    feedbackImmediacy: "immediate",      // show correct/wrong instantly
    canSkipQuestions: false,
    maxQuestionsPerSession: 5,
    hintsAvailable: true,
    mascotHelp: true,           // Buddy owl offers hints
  },
  "band-2": {
    minTapTargetPx: 48,
    maxOptionsPerQuestion: 4,
    hasTimer: true,             // optional timer (student can toggle)
    questionTypes: ["MULTIPLE_CHOICE", "TRUE_FALSE"],
    feedbackImmediacy: "after-submit",
    canSkipQuestions: true,
    maxQuestionsPerSession: 10,
    hintsAvailable: true,
    mascotHelp: false,
  },
  "band-3": {
    minTapTargetPx: 44,         // standard WCAG minimum
    maxOptionsPerQuestion: 5,
    hasTimer: true,             // timer on by default
    questionTypes: ["MULTIPLE_CHOICE", "TRUE_FALSE", "FILL_IN_THE_BLANK"],
    feedbackImmediacy: "after-submit",
    canSkipQuestions: true,
    maxQuestionsPerSession: 20,
    hintsAvailable: false,      // no hints — fosters independence
    mascotHelp: false,
  },
};
```

### Step 5 — Gamification Intensity

```typescript
export const gamificationByBand = {
  "band-1": {
    xpVisible: false,                   // XP is abstract; use stars instead
    currencyName: "Stars",
    streakVisible: false,
    leaderboardType: "class-only",      // only see classmates, not strangers
    badgeFrequency: "high",             // award badges frequently for encouragement
    levelUpAnimation: "character-dance",
    celebrationTrigger: "every-correct-answer",
    soundEffects: true,
  },
  "band-2": {
    xpVisible: true,
    currencyName: "XP",
    streakVisible: true,
    leaderboardType: "grade-level",
    badgeFrequency: "medium",
    levelUpAnimation: "burst",
    celebrationTrigger: "quiz-complete",
    soundEffects: true,
  },
  "band-3": {
    xpVisible: true,
    currencyName: "XP",
    streakVisible: true,
    leaderboardType: "national",        // compete nationally
    badgeFrequency: "low",              // badges feel earned, not given
    levelUpAnimation: "subtle-glow",
    celebrationTrigger: "milestone-only",
    soundEffects: false,                // optional, off by default
  },
};
```

### Step 6 — Band-Aware Component Example

```tsx
// src/components/quiz/QuizFeedback.tsx
"use client";
import { useBand } from "@/hooks/useBand";

interface QuizFeedbackProps {
  isCorrect: boolean;
  score: number;
}

export function QuizFeedback({ isCorrect, score }: QuizFeedbackProps) {
  const band = useBand();   // derives band from student's gradeLevel in session

  const messages = {
    "band-1": { correct: "🌟 Amazing! That's right!", wrong: "Oops! Let's try again 😊" },
    "band-2": { correct: "🎉 Correct! Great job!", wrong: "Not quite — keep going!" },
    "band-3": { correct: "Correct.", wrong: `Incorrect. Your score: ${score}%` },
  };

  return (
    <div
      role="status"
      aria-live="polite"
      className={isCorrect ? "text-quest-green" : "text-quest-red"}
    >
      {isCorrect ? messages[band].correct : messages[band].wrong}
    </div>
  );
}
```

```typescript
// src/hooks/useBand.ts
import { useSession } from "@/hooks/useSession";

export type AgeBand = "band-1" | "band-2" | "band-3";

export function useBand(): AgeBand {
  const { student } = useSession();
  const grade = student?.gradeLevel ?? 5;
  if (grade <= 2) return "band-1";
  if (grade <= 5) return "band-2";
  return "band-3";
}
```

## Output
- Band configuration table for the feature (`typography`, `visual style`, `copy tone`, `interaction`, `gamification`)
- Band-aware component implementations
- Figma frames for all three band variants
- Design QA checklist confirming each band variant was reviewed

## Quality Checks
- [ ] Minimum tap target >= 56 px for Band 1, >= 48 px for Band 2, >= 44 px for Band 3
- [ ] Band 1: no timers, no more than 3 answer options, no fill-in-the-blank
- [ ] Band 1: Buddy owl mascot present for instruction and hint delivery
- [ ] Band 3: emoji removed from UI copy; tone is peer-level not patronising
- [ ] Leaderboard exposure: Band 1 = class only; Band 2 = grade only; Band 3 = national
- [ ] XP shown as Stars for Band 1 (abstract concept not appropriate for age 5-7)
- [ ] Celebration intensity reduced progressively across bands
- [ ] All three band variants reviewed by at least one educator before release
- [ ] Accessibility requirements met across all bands (see implement-accessibility.md)

## Example

```
Feature: Quiz results screen for Mathematics, Grade 2 student (Band 1)

Typography: Nunito 32px heading, 18px body, line-height 1.8
Visual: bright colours, 48px badge icon, 20px border-radius
Copy: "🌟 AMAZING! You got 4 right, {firstName}!"  (no "%" — abstract for age 6-8)
Gamification: Stars awarded (not XP), character dance animation, sound effect
Timer: not shown
Leaderboard: not shown on this screen (class-only leaderboard available elsewhere)
```
