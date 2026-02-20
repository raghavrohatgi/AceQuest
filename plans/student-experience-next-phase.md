---
planStatus:
  planId: plan-student-experience-next-phase
  title: AceQuest — Student Experience Next Phase
  status: draft
  planType: initiative
  priority: high
  owner: raghavrohatgi
  stakeholders: []
  tags:
    - student-experience
    - engagement
    - learning
    - b2c
    - next-phase
  created: "2026-02-17"
  updated: "2026-02-17T00:00:00.000Z"
  progress: 0
---
# AceQuest — Student Experience: What Comes Next

> **Context:** All user flows and mockups for the core game loop are 100% complete (P0, P1, P2 screens all done). This plan identifies the next high-impact areas to build for students on the learning platform.

---

## Where We Are

The student experience covers:
- ✅ Onboarding (welcome → signup → OTP → avatar → tutorial)
- ✅ Home dashboard (first-time + returning)
- ✅ Subject pages (Math, English, Science)
- ✅ Full game loop (pre-game → diagnostic → gameplay → results)
- ✅ All question types (MCQ, FITB, Match, Dropdown, Passage)
- ✅ Monetisation flow (paywall, subscription plans, save-progress nudge)
- ✅ Social features (leaderboard, achievements, notifications)
- ✅ Settings & logout

---

## What Comes Next — 6 Key Areas

---

### 1. 📊 Personalised Learning Path

**The Gap:** After playing a game, the student sees results — but there's no system telling them *what to learn next* or *where their weak spots are* over time.

**What to Build:**
- **Skill Map / Learning Tree:** Visual tree of topics per subject (e.g. Math → Fractions → Adding Fractions). Nodes unlock as the student demonstrates mastery. Shows exactly where they are in the curriculum.
- **Weekly Learning Plan:** Based on diagnostic results, auto-generate a 5-game weekly plan. "You're weak at fractions — here are 3 recommended games this week."
- **Spaced Repetition Reminders:** Resurface topics the student got wrong 3 days later in a quick 5-question "Recall" mini-game.
- **"Next Best Game" Recommendation Card:** On the home screen, one prominent card: "Your next challenge: Fractions Level 2 — based on your last game."

**Screens Needed:**
- `skill-map.mockup.html` — topic tree per subject, mastery indicators
- `weekly-plan.mockup.html` — this week's recommended game schedule
- `recall-quiz.mockup.html` — short 5-question spaced repetition session

---

### 2. 🏆 Social & Competitive Layer (Friends + Challenges)

**The Gap:** The leaderboard is global/anonymous. There's no way for students to challenge friends or classmates directly.

**What to Build:**
- **Add Friends:** Students can search by username or share a friend code. Friend list shows their XP, streak, last played game.
- **1v1 Challenge:** Send a friend a challenge on a specific game/topic. Both play the same question set; winner is shown on a side-by-side results screen.
- **Weekly Class Challenge:** (for B2B later) Teacher or parent sets a challenge; students see a leaderboard specific to their group.
- **Friend Activity Feed:** "Arjun just scored 95% in Fractions!" — motivates students to come back and beat their friends.

**Screens Needed:**
- `friends.mockup.html` — friend list, add friend, friend activity
- `challenge-invite.mockup.html` — send challenge, pick topic/game
- `challenge-results.mockup.html` — side-by-side score comparison

---

### 3. 🎓 Parent Visibility Dashboard (B2C Unlockable)

**The Gap:** Parents pay the subscription but have no visibility into what their child is actually learning or how they're progressing.

**What to Build:**
- **Parent Mode:** Separate PIN-protected view within the same app (no separate app needed for v1).
- **Weekly Report Card:** Auto-generated every Sunday. Subjects covered, topics mastered, time spent, XP earned, streaks.
- **Strength & Gap Summary:** "Rohan is strong in Geometry (85% mastery) but needs help with Word Problems (42% mastery)."
- **Learning Streak Calendar:** GitHub-style heatmap of daily activity.
- **Recommended Actions:** "Rohan hasn't played Science in 2 weeks — tap to remind him."

**Screens Needed:**
- `parent-home.mockup.html` — overview of all child profiles
- `parent-child-report.mockup.html` — detailed per-child weekly report
- `parent-pin-entry.mockup.html` — PIN gate to parent mode

---

### 4. 🎁 Reward Economy & Cosmetics Store

**The Gap:** Students earn XP and badges, but XP has no spending mechanic. There's nothing to *buy* with earned currency, which limits long-term retention.

**What to Build:**
- **Coin System:** XP converts to "Star Coins" (soft currency). Earn coins by playing, maintaining streaks, completing challenges.
- **Cosmetics Store:** Students spend coins on: avatar frames, background themes, mascot outfits, chat stickers. No pay-to-win — all gameplay items are earned, only cosmetics are purchasable.
- **Seasonal Events:** Time-limited cosmetics tied to festivals (Diwali skins, Republic Day badge) to drive re-engagement.
- **Daily Login Reward:** Spin-the-wheel or scratch card for bonus coins. Drives daily habit.

**Screens Needed:**
- `store.mockup.html` — cosmetics catalog, coin balance, featured items
- `daily-reward.mockup.html` — daily spin/scratch card
- `avatar-customisation.mockup.html` — extended avatar editor with purchased items

---

### 5. 📚 Content Depth & Curriculum Alignment

**The Gap:** The platform has 3 subjects (Math, English, Science). But the CBSE curriculum has 100s of topics per grade, and currently there's no clear view of curriculum coverage.

**What to Build:**
- **Curriculum Map:** Every game is tagged to a CBSE chapter and learning objective. Students and parents can see % coverage of the full syllabus.
- **Exam Mode:** Before school exams, a "Rapid Revision" mode — timed, high-pressure practice on recent topics. Like a mock test but with the game aesthetic.
- **Hindi / Regional Language Games:** Unlock games in Hindi or regional languages (Tamil, Telugu, Marathi). Critical for Tier 2/3 India penetration.
- **Cross-Subject Challenges:** "Math + Science combo" games for topics that span subjects (e.g. measurements in both Math and Science).

**Screens Needed:**
- `curriculum-map.mockup.html` — chapter-by-chapter coverage grid
- `exam-mode.mockup.html` — timed revision mode with score report
- `language-selector.mockup.html` — in-game language switcher

---

### 6. 🔔 Re-engagement & Habit Formation

**The Gap:** The notification screen exists, but the strategy for bringing students back daily (outside of school reminders) isn't fully developed.

**What to Build:**
- **Streak Protection:** If a student is about to lose their streak, a push notification fires at their usual play time: "Don't lose your 7-day streak! Play 1 game to keep it."
- **Weekly Challenge Reveal:** Every Monday, a new weekly challenge appears on the home screen with a special badge reward. Creates a weekly ritual.
- **"Your Rival" Feature:** The app picks a student slightly above you on the leaderboard as your "rival." You get notified when they pull ahead.
- **Smart Notification Timing:** Learn each student's typical play time from history; schedule nudges around that window (not at 2am).
- **Parent-Triggered Reminders:** Parent can set a study time from parent mode; the app reminds the child at that time.

**Screens Needed:**
- `streak-protection-alert.mockup.html` — streak at-risk notification panel
- `weekly-challenge-reveal.mockup.html` — Monday challenge card with countdown
- `rival-update.mockup.html` — "your rival overtook you" screen

---

## Priority Order

| Priority | Area | Why First |
| --- | --- | --- |
| 🔴 P0 | **Personalised Learning Path** | Core product value — turns one-time players into repeat learners. Directly tied to retention and subscription renewal. |
| 🔴 P0 | **Parent Visibility Dashboard** | Parents are the paying customer in B2C India. Giving them a report card dramatically increases willingness to renew. |
| 🟡 P1 | **Re-engagement & Habit Formation** | Streak protection + weekly challenges are quick wins that drive DAU without building new screens from scratch. |
| 🟡 P1 | **Social & Competitive Layer** | Friends + challenges increase word-of-mouth virality. Critical for organic growth. |
| 🟢 P2 | **Reward Economy & Cosmetics Store** | Increases depth of engagement for active users; not needed to prove core value. |
| 🟢 P2 | **Content Depth & Curriculum Alignment** | Needed for B2B school contracts and Tier 2/3 expansion; not blocking B2C launch. |

---

## Recommended Next Steps

1. **Start with Personalised Learning Path** — Design the skill map and weekly plan screens (mockups), then spec the adaptive algorithm that drives recommendations.
2. **Build Parent Dashboard** — 3-4 screens; high ROI given parents hold the subscription wallet.
3. **Quick-win: Streak Protection + Weekly Challenge** — These are notification-layer features that can be added with minimal new screens.
4. **Social Layer** — Friend challenges as the next major feature after core retention is solved.

---

## Notes

- All items above assume B2C (direct-to-parent/student) launch. B2B (school portal, teacher dashboard, class analytics) is a separate track.
- Regional language support (Hindi, Tamil, etc.) should be threaded into every feature, not treated as a separate bolt-on.
- Every new screen should follow the existing UI/UX framework (`design-system/ui-ux-framework.md`) — particularly the age-split design patterns (Grades 3-5 vs 6-8).
