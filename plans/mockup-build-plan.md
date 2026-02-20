---
planStatus:
  planId: plan-mockup-build-plan
  title: AceQuest Student App — Complete Mockup Build Plan
  status: in-development
  planType: system-design
  priority: high
  owner: raghavrohatgi
  stakeholders: []
  tags:
    - mockup
    - student
    - ux
    - game-flow
    - onboarding
  created: "2026-02-13"
  updated: "2026-02-14T07:00:00.000Z"
  progress: 80
---
# AceQuest Student App — Complete Mockup Build Plan

## What exists today

| File | Screen | Status |
| --- | --- | --- |
| `student-profile-selector.mockup.html` | Profile selector (who's playing?) — "Add New Player" links to avatar flow for multi-child support | ✅ Done |
| `student-home-first-time.mockup.html` | First-time home (no games yet) | ✅ Done |
| `student-home-dashboard.mockup.html` | Returning student home | ✅ Done |
| `student-profile.mockup.html` | Student profile & achievements | ✅ Done |
| `subject-math.mockup.html` | Math subject page | ✅ Done |
| `subject-english.mockup.html` | English subject page | ✅ Done |
| `subject-science.mockup.html` | Science subject page | ✅ Done |
| `game-pre-game.mockup.html` | Pre-game lobby screen | ✅ Done |

---

## What needs to be built (Game Flow)

These 4 screens complete the core game loop triggered by "Start Game":

| File | Screen | Status |
| --- | --- | --- |
| `game-diagnostic.mockup.html` | Diagnostic test (MCQ) | ⏳ In progress |
| `game-diagnostic-results.mockup.html` | Knowledge meter results | ⏳ In progress |
| `game-play.mockup.html` | Gameplay (MCQ + feedback) | ⏳ In progress |
| `game-results.mockup.html` | Post-game results + leaderboard | ⏳ In progress |

---

## What needs to be built (Rest of student journey per sitemap)

Based on `sitemap-jobs-to-be-done.md` and `student-user-journey-v1.md`:

### Onboarding Flow
| File | Screen | Priority |
| --- | --- | --- |
| `onboarding-welcome.mockup.html` | Welcome splash — mascot, tagline, subject pills, social proof, "Start Playing" CTA + Log in link | ✅ Done |
| `onboarding-signup.mockup.html` | Sign up — 2-col form (mobile+email / name+grade), Google/Apple, OTP flow, "Play first →" escape hatch, links to avatar with `?from=signup` | ✅ Done |
| `onboarding-login.mockup.html` | Login — mobile/email tab switcher, Google/Apple, OTP, recent player profile chips | ✅ Done |
| `onboarding-avatar.mockup.html` | Avatar picker (6-col compact grid) + name + grade; fields hidden when `?from=signup`; progressive reg nudge shown for guest flow; links to home | ✅ Done |
| `onboarding-tutorial-1.mockup.html` | Tutorial: Welcome screen (Step 2 of 3) | P1 |
| `onboarding-tutorial-2.mockup.html` | Tutorial: Finding games (Quick tour 1/2) | P1 |
| `onboarding-tutorial-3.mockup.html` | Tutorial: How to play (Quick tour 2/2) | P1 |

**Onboarding UX Rules (Progressive Registration):**
- Students can play immediately without any account — no barrier on download
- Flow A (Guest): Welcome → Avatar (name + grade + save-progress nudge) → Home
- Flow B (Sign up): Welcome → Sign Up (mobile OTP + name + grade) → Avatar (pick only) → Home
- Flow C (Login): Welcome → Log In → Home Dashboard
- Multi-child: Profile Selector → "Add New Player" → Avatar (full name+grade flow)
- Registration ask is deferred — nudge to add mobile only after student has played and has XP/streaks worth saving
- Payment prompt comes even later, after value is established

### Game Library
| File | Screen | Priority |
| --- | --- | --- |
| `game-library.mockup.html` | Game library / browse all games | P0 |
| `game-preview.mockup.html` | Game preview before starting | P1 |

### Gameplay (In-game flow)
| File | Screen | Priority |
| --- | --- | --- |
| `game-loading.mockup.html` | Game loading screen | P2 |
| `game-intro.mockup.html` | Game story introduction | P1 |
| `game-play-fitb.mockup.html` | FITB Variant 1: Single blank, text sentence | ✅ Done |
| `game-play-fitb-multi.mockup.html` | FITB Variant 2: Multiple blanks (3 blanks) with progress dots | ✅ Done |
| `game-play-fitb-image.mockup.html` | FITB Variant 3: Image shown, identify the word | ✅ Done |
| `game-play-fitb-audio.mockup.html` | FITB Variant 4: Voiceover, listen and identify | ✅ Done |
| `game-play-fitb-sentence-image.mockup.html` | FITB Variant 5: Sentence + image side by side, fill blank | ✅ Done |
| `game-play-fitb-equation.mockup.html` | FITB Variant 6: Math equation with missing number | ✅ Done |
| `game-play-fitb-typed.mockup.html` | FITB Variant 7: Free-type keyboard input (no word bank), 3 attempts | ✅ Done |
| `game-play-fitb-diagram.mockup.html` | FITB Variant 8: Label the diagram (human body parts) | ✅ Done |
| `game-play-fitb-passage.mockup.html` | FITB Variant 9: Reading passage with 3 blanks scattered in text | ✅ Done |
| `game-play-match-text.mockup.html` | Match Variant 1: Text to text (6 pairs, countries & capitals) | ✅ Done |
| `game-play-match-text-image.mockup.html` | Match Variant 2: Text to image (5 pairs, animals) | ✅ Done |
| `game-play-match-image.mockup.html` | Match Variant 3: Image to image (4 pairs, plants & fruits) | ✅ Done |
| `game-play-match-text-sound.mockup.html` | Match Variant 4: Text to sound (4 pairs, instruments) | ✅ Done |
| `game-play-match-sound-text.mockup.html` | Match Variant 5: Sound to text (4 pairs, spelling) | ✅ Done |
| `game-play-dropdown.mockup.html` | Gameplay: Dropdown variant | P1 |
| `game-play-video.mockup.html` | Mid-game concept video screen | P1 |
| `game-play-interactive.mockup.html` | Mid-game interactive mini-game screen | P2 |
| `game-play-feedback-wrong.mockup.html` | Wrong-answer feedback overlay | P1 |
| `game-checkpoint.mockup.html` | Mid-game checkpoint / break | P1 |
| `game-pause.mockup.html` | Pause menu | P1 |

### Passage-Based Question Flow
Passages are multi-question blocks around a source (text/video/audio/image). Each passage has a cover, reader, associated questions (MCQ/FITB/Match/T-F), and optional explanations for hard questions.

| File | Screen | Notes |
| --- | --- | --- |
| `game-play-passage-cover.mockup.html` | Passage cover | Title, subject tag, cover image (center-aligned), source credit, "Start Reading" CTA. Restart button removed. Full-screen. | ✅ Done |
| `game-play-passage-text.mockup.html` | Text passage reader | Scrollable text, audio button, Back + Go to Questions on same row. Full-screen. Multilingual fonts. | ✅ Done |
| `game-play-passage-video.mockup.html` | Video passage | Compact mini-player (160px) with expand-to-16:9 button (YouTube-style), transcript toggle, scrollable card. Full-screen. | ✅ Done |
| `game-play-passage-audio.mockup.html` | Audio passage | Full audio player UI (waveform), transcript panel, Back + Go to Questions row. Full-screen. | ✅ Done |
| `game-play-passage-image.mockup.html` | Image passage | Annotated water cycle infographic, interactive labels, zoom hint. Full-screen. | ✅ Done |
| `game-play-passage-question.mockup.html` | Passage question screen | MCQ with 50/50 split-screen "View Passage" panel. Auto-opens correct passage type (text/video/audio/image) via `?type=` URL param. Tabs shown for mockup review only — real app renders one type. | ✅ Done |
| `game-play-passage-explanation.mockup.html` | Post-passage explanation | After all questions answered; explanation card for hard questions, source credit. Full-screen. | ✅ Done |
| `game-play-fitb-passage.mockup.html` | FITB passage variant | Reading passage with 3 blanks scattered in text. Full-screen. Multilingual fonts. | ✅ Done |

**Passage UX Rules:**
- Each passage is exactly **one type**: text, audio, video, or image — never a mix
- Passage cover always shows: title, cover image (center-aligned), topic badge, source credit
- "View Passage" on every question screen opens a **50/50 horizontal split panel** showing the relevant passage content inline
- Split panel auto-selects content from `?type=text|audio|video|image` URL param passed by the passage screen
- Back + Go to Questions always on the same row; Back uses white-on-purple frosted style
- All passage screens are full-screen (no max-width constraint)
- All passage screens support multilingual fonts: Hindi/Marathi (Devanagari), Gujarati, Punjabi (Gurmukhi) via Noto Sans
- On restart: completed questions are greyed-out / skipped, student picks up from first unanswered
- Question types within a passage: MCQ, FITB (any variant), Match, True/False
- True/False is a simplified MCQ with only two options (True / False)

### Achievements & Progress
| File | Screen | Priority |
| --- | --- | --- |
| `achievements.mockup.html` | Full achievements wall | P1 |

### Other
| File | Screen | Priority |
| --- | --- | --- |
| `logout-confirm.mockup.html` | Logout confirmation | P2 |

---

## Full User Flow (Reference)

```
[Welcome / Splash]
    ├── "Start Playing" (guest) → [Avatar + Name + Grade] → [Home First-time]
    ├── "Sign Up"               → [Sign Up Form (mobile+name+grade)] → [Avatar (pick only)] → [Home First-time]
    └── "Log In"                → [Login (OTP)] → [Home Dashboard]

[Profile Selector] (multi-child)
    └── "Add New Player"        → [Avatar + Name + Grade] → [Home First-time]
    ↓ click "Start your first game" or subject game button
[Subject Page] ← exists (math/english/science)
    ↓ click "Start Game"
[Pre-Game Lobby] ← exists
    ↓ click "Play Now"
[Diagnostic Test] ← building now
    ↓ complete
[Diagnostic Results / Knowledge Meter] ← building now
    ↓ "Let's Play!"
[Game Story Intro]
    ↓
[Gameplay: Q1] → [Feedback] → [Q2] → ... → [Mid-game Video] → ...
    ↓ Q35-40 done
[Post-Game Results + Leaderboard] ← building now
    ↓
[Home Dashboard (returning)]
```

---

## Build Priority Order

### Phase 1 (Now — complete game loop)
1. `game-diagnostic.mockup.html`
2. `game-diagnostic-results.mockup.html`
3. `game-play.mockup.html`
4. `game-results.mockup.html`

### Phase 2 (Onboarding + supporting game screens)
5. `onboarding-welcome.mockup.html`
6. `onboarding-signup.mockup.html`
7. `onboarding-login.mockup.html`
8. `onboarding-avatar.mockup.html`
9. `game-library.mockup.html`
10. `game-preview.mockup.html`
11. `game-intro.mockup.html`

### Phase 3 (Fill-in-blank, dropdown, checkpoint, pause, video)
12. `game-play-fitb.mockup.html` ✅ (+ 8 variants: multi, image, audio, sentence-image, equation, typed, diagram, passage)
13. `game-play-match-*.mockup.html` ✅ (5 variants: text-text, text-image, image-image, text-sound, sound-text)
14. `game-play-dropdown.mockup.html`
15. `game-play-video.mockup.html`
16. `game-checkpoint.mockup.html`
17. `game-pause.mockup.html`
18. `game-play-feedback-wrong.mockup.html`

### Phase 4 (Remaining)
18. `onboarding-tutorial-1/2/3.mockup.html`
19. `achievements.mockup.html`
20. `game-loading.mockup.html`
21. `game-play-interactive.mockup.html`
22. `logout-confirm.mockup.html`

---

## Mockup References (to be linked as screenshots once created)

### Game Flow (Phase 1)
![Diagnostic Test](screenshot.png){mockup:nimbalyst-local/mockups/game-diagnostic.mockup.html}
![Diagnostic Results](screenshot.png){mockup:nimbalyst-local/mockups/game-diagnostic-results.mockup.html}
![Gameplay](screenshot.png){mockup:nimbalyst-local/mockups/game-play.mockup.html}
![Post-Game Results](screenshot.png){mockup:nimbalyst-local/mockups/game-results.mockup.html}
