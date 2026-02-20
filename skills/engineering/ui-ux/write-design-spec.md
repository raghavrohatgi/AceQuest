# Skill: Write Design Specification

## Purpose
Define how to produce a complete, engineering-ready design specification for any AceQuest feature. A design spec translates UX intent into precise, unambiguous instructions that frontend engineers can implement without follow-up questions. It covers layout, interactions, states, responsive behaviour, copy, accessibility requirements, and acceptance criteria.

## Used By
- UI/UX Designer Agent
- Frontend Engineer Agent
- QA Agent (for acceptance criteria)

## Inputs
| Field | Type | Description |
| --- | --- | --- |
| `featureName` | string | Name of the feature, e.g. "Quiz Results Screen" |
| `userStory` | string | The user story this spec fulfils |
| `ageGroup` | `"5-7" \ | "8-10" \ | "11-13"` | Determines typography scale and interaction complexity |
| `platform` | `"mobile-first" \ | "desktop" \ | "both"` | Layout priority |
| `figmaLink` | string | URL to the Figma frames |
| `designTokens` | string | Reference to AceQuest design system token file |

## Design Spec Template

---

# Design Spec: Quiz Results Screen

**Feature:** Post-Quiz Results
**User Story:** As a Grade 5 student, after submitting a quiz, I want to see my score, XP earned, and any badges unlocked so that I feel rewarded and motivated to continue.
**Age Group:** 8–10
**Platform:** Mobile-first (375 px), responsive to 768 px tablet, 1280 px desktop
**Figma:** [Link to Figma frames]
**Design Tokens:** `/design-system/tokens.ts`
**Last Updated:** 2025-06-01

---

## 1. Overview

The Quiz Results screen appears immediately after a student submits a quiz. It delivers a celebratory moment (animation + score reveal), followed by XP and badge details, and a clear call-to-action to continue.

---

## 2. Layout Specifications

### 2.1 Mobile (375 px)

```
┌─────────────────────────────┐
│  [Back button]   AceQuest   │  ← Navigation bar (56 px)
├─────────────────────────────┤
│                             │
│    🎉 GREAT JOB, AARAV!    │  ← H1, 28 px, quest-navy, centre-aligned
│                             │
│  ┌────────────────────────┐ │
│  │     Score: 85%         │ │  ← Score card (rounded-2xl, shadow-md)
│  │   17 correct / 20      │ │
│  └────────────────────────┘ │
│                             │
│  ┌────────────────────────┐ │
│  │  +150 XP earned        │ │  ← XP pill (bg-quest-gold, text-white)
│  └────────────────────────┘ │
│                             │
│  Badges Unlocked:           │  ← Section heading H2, 18 px
│  ┌──────┐                  │
│  │ 🏆   │  Quiz Master     │  ← Badge row (icon 48 px + name + rarity)
│  └──────┘                  │
│                             │
│  [Try Another Quiz]         │  ← Primary CTA button, full-width
│  [Back to Dashboard]        │  ← Secondary CTA, outline style
│                             │
└─────────────────────────────┘
```

### 2.2 Desktop (1280 px)

Two-column layout:
- **Left column (60%):** Score card + answer review accordion
- **Right column (40%):** XP + badges + CTA buttons

---

## 3. Component Specifications

### 3.1 Score Card

| Property | Value |
| --- | --- |
| Background | `white` |
| Border radius | `16 px` (Tailwind: `rounded-2xl`) |
| Shadow | `shadow-md` |
| Padding | `24 px` |
| Score number | `font-size: 64 px`, `font-weight: 800`, colour based on score (see 3.1.1) |
| Score label | `"Your Score"`, `font-size: 14 px`, `color: gray-500` |

#### 3.1.1 Score Colour Thresholds

| Score Range | Text Colour | Background Tint |
| --- | --- | --- |
| 90–100% | `quest-green` (#15803D) | `green-50` |
| 70–89% | `quest-gold` (#D97706) | `yellow-50` |
| 0–69% | `quest-red` (#B91C1C) | `red-50` |

**Note:** Colour is supplementary — score value in text is always shown regardless.

### 3.2 XP Pill

```
background: linear-gradient(135deg, #D97706, #F59E0B)
color: white
border-radius: 24 px
padding: 8 px 20 px
font-size: 18 px
font-weight: 700
icon: ⚡ (sparkle emoji) + "+{n} XP"
animation: scale 0 → 1 over 600 ms (ease-out-back), delayed 400 ms after score reveal
```

### 3.3 Badge Card

| Property | Value |
| --- | --- |
| Layout | Row: icon (48 × 48) + text column |
| Icon style | Circular, `border: 2 px solid quest-gold` |
| Badge name | `font-size: 16 px`, `font-weight: 600`, `quest-navy` |
| Rarity label | `font-size: 12 px`, colour per rarity (see below) |
| Unlock animation | Slide up + fade in, 300 ms delay per badge |

Rarity label colours:
- COMMON: `gray-500`
- RARE: `quest-purple`
- EPIC: `orange-600`
- LEGENDARY: `quest-gold` with shimmer CSS animation

---

## 4. Copy / Content

| Element | Text |
| --- | --- |
| Page title (90–100%) | "🎉 PERFECT! You're a star, {firstName}!" |
| Page title (70–89%) | "🎉 GREAT JOB, {firstName}!" |
| Page title (0–69%) | "Keep going, {firstName}! Practice makes perfect." |
| Score label | "Your Score" |
| XP label | "+{xp} XP earned" |
| Badges section heading | "Badges Unlocked" (hidden if 0 badges) |
| No badges | (omit section entirely — do not show "No badges unlocked") |
| Primary CTA | "Try Another Quiz" |
| Secondary CTA | "Back to Dashboard" |

**Tone:** Encouraging, celebratory, second-person address using student's first name. No negative language (avoid "Only X%", "You failed").

---

## 5. Interactions and Animations

| Trigger | Animation | Duration | Easing |
| --- | --- | --- | --- |
| Page load | Score number counts up from 0 to final value | 800 ms | ease-out |
| Score reveal complete | XP pill scales in | 600 ms | ease-out-back |
| XP reveal complete | Badges slide up one by one | 300 ms each | ease-out |
| If score >= 90% | Confetti explosion (respects prefers-reduced-motion) | 3 s | — |
| Primary CTA hover | Background darkens 10%, scale 1.02 | 150 ms | ease |

**Reduced motion fallback:** Replace all animations with instant opacity fade (150 ms).

---

## 6. Responsive Breakpoints

| Breakpoint | Behaviour |
| --- | --- |
| < 375 px | Score font-size reduces to 48 px; badges stack vertically |
| 375–767 px | Single column, full-width cards |
| 768–1279 px | Single column, cards capped at 480 px wide, centred |
| >= 1280 px | Two-column layout (60/40 split) |

---

## 7. Accessibility Requirements

- [ ] Page `<h1>` is the title string (e.g. "GREAT JOB, AARAV!")
- [ ] Score card has `role="region"` and `aria-label="Your quiz score"`
- [ ] Score number has `aria-label="Score: 85 percent"`
- [ ] XP pill has `role="status"` and `aria-live="polite"` — announced when revealed
- [ ] Badge section has `role="list"` with each badge as `role="listitem"`
- [ ] Confetti does not trigger if `prefers-reduced-motion: reduce` is set
- [ ] All colour-coded score states also show the percentage value in text

---

## 8. Acceptance Criteria

- [ ] Score displays correctly for values 0–100
- [ ] XP pill shows the exact XP awarded by the backend (not hardcoded)
- [ ] Badges section is hidden when no badges are unlocked (no empty state shown)
- [ ] Score colour matches the threshold table in §3.1.1
- [ ] All animations complete within 2 seconds of page load
- [ ] Confetti does not appear when `prefers-reduced-motion: reduce` is set
- [ ] Title copy varies based on score range as defined in §4
- [ ] "Try Another Quiz" navigates to `/quiz?topic={topicId}&gradeLevel={gradeLevel}`
- [ ] Lighthouse accessibility score >= 95 on this page

## Output
- Completed spec document (this template, filled)
- Figma frames linked in spec
- Spec reviewed and approved by lead designer before engineering handoff
- Acceptance criteria copied into the implementation ticket

## Quality Checks
- [ ] Every measurement is in px OR Tailwind class — no ambiguity
- [ ] All states covered: empty (0 badges), single badge, multiple badges
- [ ] Copy written for all score tiers and age groups
- [ ] Accessibility requirements are specific and testable
- [ ] Animation durations and easings are defined precisely
- [ ] Responsive breakpoints match Tailwind's default breakpoint system
