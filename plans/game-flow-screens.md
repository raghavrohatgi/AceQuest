---
planStatus:
  planId: plan-game-flow-screens
  title: Game Flow Screens (Pre-game Diagnostic → Gameplay → Post-game Results)
  status: draft
  planType: feature
  priority: high
  owner: raghavrohatgi
  stakeholders: []
  tags:
    - game
    - student
    - ux
    - mockup
  created: "2026-02-13"
  updated: "2026-02-13T00:00:00.000Z"
  progress: 0
---
# Game Flow Screens

## Overview

Design the complete screen flow a student experiences from clicking "Start Game" on the home or subject page through to completing a game, including a pre-game diagnostic assessment and post-game results.

## User Journey

```
Home / Subject Page
      ↓ Click "Start Game"
[1] Pre-Game Lobby (already exists: game-pre-game.mockup.html)
      ↓ Click "Play Now"
[2] Diagnostic Test (NEW) — "Let's see what you know!"
      ↓ Complete short quiz
[3] Diagnostic Results + Learning Path (NEW) — Personalized starting point
      ↓ Begin game
[4] Gameplay Screen (NEW) — Questions with chosen interaction types
      ↓ Complete all questions
[5] Post-Game Results / End Screen (NEW) — Score, XP gained, badges unlocked
      ↓ Continue
Back to Home / Subject Page
```

---

## Screens to Design

### [1] Pre-Game Lobby (existing: `game-pre-game.mockup.html`)
Already exists. Shows game name, description, XP reward, difficulty. Has "Play Now" CTA.

---

### [2] Diagnostic Test Screen (`game-diagnostic.mockup.html`) — NEW

**Purpose:** Quickly assess prior knowledge before starting the game. 3–5 short questions covering key concepts of the topic. Low-stakes framing ("No grades, just helping us personalize your journey!").

**UI Elements:**
- Progress indicator: "Question 2 of 5"
- Topic badge + game title at top
- Question area (centered, large readable text)
- Answer area — supports multiple interaction types (see below)
- Skip option ("I'll figure it out as I go →")
- Encouraging micro-copy ("You're doing great!")
- Timer is optional / disabled for diagnostic to reduce anxiety

**Interaction Types (phase 1 & future):**
| Type | Description | Phase |
| --- | --- | --- |
| MCQ (single correct) | 4 options, one correct, tap to select | Phase 1 |
| Fill in the blank | Text input inline in a sentence | Phase 1 |
| Dropdown | Inline dropdown in a sentence | Phase 1 |
| Match the following | Drag/connect two columns | Phase 2 |
| Interactive game element | Custom mini-game (e.g., drag object to answer) | Phase 2 |

---

### [3] Diagnostic Results + Learning Path (`game-diagnostic-results.mockup.html`) — NEW

**Purpose:** Show the student where they stand and set expectations. Builds excitement rather than shame.

**UI Elements:**
- Emoji / character reaction (e.g., "You already know some of this! 🌟")
- Score visualization — not a number grade but a "knowledge meter" (e.g., "You've got the basics down!")
- 3 levels shown: Beginner / Getting There / Advanced — student's position highlighted
- "Your personalized game starts at Level X" message
- Single CTA: "Let's Play! 🚀"

---

### [4] Gameplay Screen (`game-play.mockup.html`) — NEW

**Purpose:** The core learning loop — questions presented one at a time with immediate feedback.

**UI Elements:**
- Top bar: Progress bar (e.g., Q4/10), XP earned so far, timer (optional)
- Back/pause button (with confirmation dialog)
- Question card (large, centered)
- Answer interaction area (MCQ / Fill-in / Dropdown / Match)
- Submit / Check button
- Feedback overlay after each answer:
  - Correct: green flash, "+10 XP", encouraging message
  - Incorrect: red flash, correct answer revealed, brief explanation

**Streak / combo system:** Consecutive correct answers show a "combo" indicator (e.g., "3x Combo! 🔥")

---

### [5] Post-Game Results Screen (`game-results.mockup.html`) — NEW

**Purpose:** Celebrate completion, show progress, reward with XP and badges.

**UI Elements:**
- Celebration animation (confetti / star burst)
- Score summary: X/Y correct, accuracy %
- XP gained: animated counter (e.g., "+50 XP")
- Before vs After knowledge meter (compare diagnostic score to final score)
- Badges unlocked (if any) — modal pops up for first badge
- Leaderboard position (future)
- Action buttons:
  - "Play Again" (same game)
  - "Try Next Game →" (next recommended)
  - "Back to Home"

---

## Question Interaction Type Designs

### MCQ (Single Correct)
- 4 answer cards in a 2×2 grid (mobile-friendly)
- Tap to select → highlights in purple
- Submit button activates after selection
- After submit: correct turns green, wrong turns red, correct answer shown if wrong

### Fill in the Blank
- Sentence with `[____]` replaced by a text input box
- Soft keyboard on mobile
- Submit on Enter or button tap

### Dropdown
- Sentence with inline `[▼ select]` element
- Tapping opens a small picker overlay
- Submit button

### Match the Following (Phase 2)
- Two columns: left = terms, right = definitions
- Lines drawn on connect
- Drag-to-match or tap-tap to connect

---

## Mockups to Create

1. `game-diagnostic.mockup.html` — Diagnostic test (MCQ variant)
2. `game-diagnostic-results.mockup.html` — Knowledge meter results
3. `game-play.mockup.html` — Gameplay with MCQ + feedback overlay
4. `game-results.mockup.html` — Post-game celebration & summary

> The existing `game-pre-game.mockup.html` stays as is.

---

## Design Principles

- **Encourage, never shame** — always positive framing for wrong answers
- **Mobile-first** — all screens work on phone
- **Visual consistency** — same color tokens as existing mockups
- **Gamification** — XP, streaks, badges visible throughout
- **Bite-sized** — each interaction is 1 question at a time, no overwhelming walls of text

---

## Decisions Made

1. **Diagnostic is mandatory** — no skip option
2. **Diagnostic questions:** 5–10, varies per game
3. **Game session:** 35–40 questions + optional interactive game element + video(s) in between to explain concepts
4. **Timer:** No timer by default; configurable as a game-design setting when building a game
5. **Match the Following:** Phase 2
6. **Leaderboard:** Design a mockup; can be toggled off per game later
