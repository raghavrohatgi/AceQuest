---
planStatus:
  planId: plan-app-flow-and-gaps
  title: AceQuest B2C App — Screen Flow & Gap Analysis
  status: draft
  planType: system-design
  priority: high
  owner: raghavrohatgi
  stakeholders: []
  tags:
    - flowchart
    - b2c
    - ux
    - gaps
    - mockup
  created: "2026-02-14"
  updated: "2026-02-14T06:30:00.000Z"
  progress: 100
---
# AceQuest B2C App — Complete Screen Flow & Gap Analysis

> **Launch strategy**: B2C (direct to students/parents). No school/teacher portal needed for v1. Fastest path to market.

---

## Full Screen Flow (Login → Logout)

```mermaid
flowchart TD

  %% ── ENTRY ──
  A([App Launch]) --> B[onboarding-welcome]

  %% ── ONBOARDING PATHS ──
  B -->|Start Playing guest| C[onboarding-avatar\nname + grade + avatar]
  B -->|Sign Up| D[onboarding-signup\nmobile + email + name + grade]
  B -->|Log In| E[onboarding-login\nOTP via mobile or email]

  D -->|Send OTP| OTP[onboarding-otp\n6-digit code]
  OTP -->|verified| F[onboarding-avatar\navatar pick only]
  E --> G

  C --> TUT[onboarding-tutorial-1\n→ tutorial-2 → tutorial-3]
  F --> TUT
  TUT --> G[student-home-first-time\nno games yet]

  %% ── HOME ──
  G -->|returning visit| H[student-home-dashboard]
  H --> I[student-profile-selector\nwho's playing?]
  I -->|select child| H
  I -->|add new player| C

  %% ── NOTIFICATIONS & LIBRARY ──
  H -->|bell icon| NOTIF[notifications\nstreaks · challenges · badges]
  H -->|library tab| LIB[game-library\nbrowse all games]
  LIB -->|start game| K

  %% ── SUBJECT PAGES ──
  H -->|tap subject| J{Subject}
  J --> J1[subject-math]
  J --> J2[subject-english]
  J --> J3[subject-science]

  J1 & J2 & J3 -->|Start Game| K[game-pre-game\npre-game lobby]

  %% ── GAME INTRO + LOADING ──
  K --> INTRO[game-intro\nstory / narrative hook]
  INTRO --> LOAD[game-loading\nloading screen]

  %% ── DIAGNOSTIC ──
  LOAD --> L[game-diagnostic\nMCQ diagnostic test]
  L --> M[game-diagnostic-results\nknowledge meter]
  M -->|Let's Play!| N

  %% ── GAMEPLAY LOOP ──
  N[game-play\nMCQ + feedback] --> N
  N -->|wrong answer| WA[game-play-feedback-wrong\nexplanation + correct answer]
  WA --> N
  N -->|pause button| PAUSE[game-pause\nresume · settings · quit]
  PAUSE -->|resume| N
  PAUSE -->|quit| H
  N -->|halfway| CP[game-checkpoint\nhalfway stats + confetti]
  CP -->|continue| N
  N -->|concept video interstitial| VID[game-play-video\nmid-game video]
  VID -->|continue| N

  N -->|FITB question| O{FITB Variant}
  O --> O1[fitb — single blank]
  O --> O2[fitb — multi blank]
  O --> O3[fitb — image]
  O --> O4[fitb — audio]
  O --> O5[fitb — sentence+image]
  O --> O6[fitb — equation]
  O --> O7[fitb — typed]
  O --> O8[fitb — diagram]

  N -->|Match question| P{Match Variant}
  P --> P1[match — text↔text]
  P --> P2[match — text↔image]
  P --> P3[match — image↔image]
  P --> P4[match — text↔sound]
  P --> P5[match — sound↔text]

  N -->|Dropdown question| DD[game-play-dropdown\ninline select]
  DD --> N

  O1 & O2 & O3 & O4 & O5 & O6 & O7 & O8 --> N
  P1 & P2 & P3 & P4 & P5 --> N

  %% ── PASSAGE FLOW ──
  N -->|Passage question block| Q[game-play-passage-cover]
  Q --> R{Passage Type}
  R --> R1[passage-text]
  R --> R2[passage-audio]
  R --> R3[passage-image]
  R --> R4[passage-video]

  R1 & R2 & R3 & R4 -->|Go to Questions| S[game-play-passage-question\n50/50 split — MCQ]
  S --> S2[game-play-passage-explanation\npost-passage review]
  S2 --> N

  %% ── END GAME ──
  N -->|All questions done| T[game-results\nresults + leaderboard snippet]
  T -->|view full leaderboard| LB[leaderboard\npodium + full ranked list]
  LB --> H
  T -->|guest user| NUDGE[save-progress-nudge\nregister to save XP]
  NUDGE -->|enter phone| OTP
  NUDGE -->|not now| H
  T -->|free limit hit| PW[paywall\n3 games used · upgrade CTA]
  PW -->|choose plan| PLANS[subscription-plans\nmonthly / annual]
  PLANS --> H
  T --> H

  %% ── PROFILE + ACHIEVEMENTS ──
  H -->|profile icon| U[student-profile\nXP · streaks · achievements]
  U -->|view all badges| ACH[achievements\nearned · in progress · locked]
  ACH --> U
  U --> H

  %% ── SETTINGS + LOGOUT ──
  H -->|settings icon| SET[settings\naccount · subscription · preferences]
  SET -->|upgrade| PW
  SET -->|log out| V([Logged Out])
  V --> B
```

---

## Screens: Exists vs. Missing

| Screen | File | Status | Notes |
| --- | --- | --- | --- |
| Welcome / Splash | `onboarding-welcome` | ✅ Done |  |
| Sign Up | `onboarding-signup` | ✅ Done | 2-col form, OTP, play-first escape |
| Log In | `onboarding-login` | ✅ Done | Mobile/email tabs, recent profiles |
| Avatar + Name + Grade | `onboarding-avatar` | ✅ Done | Skips name/grade if from signup |
| Profile Selector | `student-profile-selector` | ✅ Done | Multi-child, Add New Player linked |
| Home (first-time) | `student-home-first-time` | ✅ Done |  |
| Home (returning) | `student-home-dashboard` | ✅ Done |  |
| Student Profile | `student-profile` | ✅ Done |  |
| Math Subject Page | `subject-math` | ✅ Done |  |
| English Subject Page | `subject-english` | ✅ Done |  |
| Science Subject Page | `subject-science` | ✅ Done |  |
| Pre-Game Lobby | `game-pre-game` | ✅ Done |  |
| Diagnostic Test | `game-diagnostic` | ✅ Done |  |
| Diagnostic Results | `game-diagnostic-results` | ✅ Done |  |
| Gameplay (MCQ) | `game-play` | ✅ Done |  |
| FITB (9 variants) | `game-play-fitb-*` | ✅ Done |  |
| Match (5 variants) | `game-play-match-*` | ✅ Done |  |
| Passage Cover | `game-play-passage-cover` | ✅ Done |  |
| Passage Text | `game-play-passage-text` | ✅ Done |  |
| Passage Audio | `game-play-passage-audio` | ✅ Done |  |
| Passage Image | `game-play-passage-image` | ✅ Done |  |
| Passage Video | `game-play-passage-video` | ✅ Done | Compact + expandable player |
| Passage Question | `game-play-passage-question` | ✅ Done | 50/50 split view |
| Passage Explanation | `game-play-passage-explanation` | ✅ Done |  |
| FITB Passage | `game-play-fitb-passage` | ✅ Done |  |
| Post-Game Results | `game-results` | ✅ Done |  |
| **OTP Verification** | `onboarding-otp.mockup.html` | ✅ Done | 6-digit box entry, countdown timer, resend link |
| **Settings / Logout** | `settings.mockup.html` | ✅ Done | Account info, subscription, preferences, dark mode toggle, logout |
| **Payment / Upgrade** | `paywall.mockup.html` | ✅ Done | Monthly/annual toggle, 7-day trial, feature list, free tier usage bar |
| **Progress Nudge** | `save-progress-nudge.mockup.html` | ✅ Done | Post-game sheet for guests showing XP at risk, inline phone entry |
| **Game Intro / Story** | `game-intro.mockup.html` | ✅ Done | Dark space theme, story hook, game metadata |
| **Game Loading** | `game-loading.mockup.html` | ✅ Done | Animated mascot, loading bar, fun tip |
| **Pause Menu** | `game-pause.mockup.html` | ✅ Done | Mid-game stats, resume/quit/settings |
| **Mid-game Checkpoint** | `game-checkpoint.mockup.html` | ✅ Done | Halfway stats, confetti, next section hint |
| **Mid-game Video** | `game-play-video.mockup.html` | ✅ Done | Concept video interstitial between question sets |
| **Dropdown Question** | `game-play-dropdown.mockup.html` | ✅ Done | Inline dashed pills, floating dropdowns, feedback |
| **Wrong Answer Detail** | `game-play-feedback-wrong.mockup.html` | ✅ Done | Your answer vs correct + step-by-step explanation |
| **Achievements Wall** | `achievements.mockup.html` | ✅ Done | Earned / In Progress / Locked, XP summary banner |
| **Subscription Plans** | `subscription-plans.mockup.html` | ✅ Done | Annual/monthly toggle, comparison table, free tier |
| **Game Library** | `game-library.mockup.html` | ✅ Done | Search, subject tabs, trending, continue, completed |
| **Tutorial step 1** | `onboarding-tutorial-1.mockup.html` | ✅ Done | Answer questions, earn XP |
| **Tutorial step 2** | `onboarding-tutorial-2.mockup.html` | ✅ Done | Compete on the leaderboard |
| **Tutorial step 3** | `onboarding-tutorial-3.mockup.html` | ✅ Done | Play free, upgrade anytime |
| **Leaderboard (full)** | `leaderboard.mockup.html` | ✅ Done | Podium, full ranked list, sticky your-rank strip |
| **Notifications** | `notifications.mockup.html` | ✅ Done | Streak reminders, badges, challenges, weekly summary |

---

## Gap Summary by Priority

### 🔴 P0 — Needed Before Any User Testing — ✅ ALL DONE
| Gap | Status |
| --- | --- |
| OTP Verification screen | ✅ Done — `onboarding-otp.mockup.html` |
| Settings + Logout | ✅ Done — `settings.mockup.html` |
| Save Progress Nudge | ✅ Done — `save-progress-nudge.mockup.html` |
| Paywall / Free Tier Limit | ✅ Done — `paywall.mockup.html` (monthly/annual, 7-day trial) |

### 🟡 P1 — Needed for Complete Core Loop ✅ All Done
| Screen | File | Status |
| --- | --- | --- |
| Game Intro / Story | `game-intro.mockup.html` | ✅ Done |
| Pause Menu | `game-pause.mockup.html` | ✅ Done |
| Mid-game Checkpoint | `game-checkpoint.mockup.html` | ✅ Done |
| Wrong Answer Detail | `game-play-feedback-wrong.mockup.html` | ✅ Done |
| Game Library | `game-library.mockup.html` | ✅ Done |
| Subscription Plans | `subscription-plans.mockup.html` | ✅ Done |

### 🟢 P2 — Polish / Nice-to-Have ✅ All Done
| Screen | File | Status |  |
| --- | --- | --- | --- |
| Game Loading screen | `game-loading.mockup.html` | ✅ Done |  |
| Mid-game Video interstitial | `game-play-video.mockup.html` | ✅ Done |  |
| Dropdown question type | `game-play-dropdown.mockup.html` | ✅ Done |  |
| Achievements Wall | `achievements.mockup.html` | ✅ Done |  |
| Tutorial step 1 | `onboarding-tutorial-1.mockup.html` | ✅ Done |  |
| Tutorial step 2 | `onboarding-tutorial-2.mockup.html` | ✅ Done |  |
| Tutorial step 3 | `onboarding-tutorial-3.mockup.html` | ✅ Done |  |
| Full Leaderboard | `leaderboard.mockup.html` | ✅ Done |  |
| Notifications screen | `notifications.mockup.html` | ✅ Done |  |

---

## B2C Monetisation Flow (Recommended)

```
Guest plays 1 full game free
    ↓
End of game → "Save your progress!" nudge → Register (mobile OTP)
    ↓
Registered user gets 3 games/week free
    ↓
Hits free limit → Paywall screen → Plan selection (₹99/month or ₹799/year)
    ↓
Payment → Unlimited access
```

This defers payment until the student has experienced real value — reduces friction at download and increases conversion.

---

## All Screens — Complete ✅

P0, P1, and P2 screens are all built. The full core loop is mocked up end to end from app launch → gameplay → results → paywall → logout.
