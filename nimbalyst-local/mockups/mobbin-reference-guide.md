# Mobbin Reference Guide for AceQuest
**Date:** 2026-02-09
**Purpose:** UX/UI inspiration for gamified assessment platform (Grades 3-8)

---

## 🎯 Top Apps to Reference on Mobbin

### **Primary References (Must Study)**

#### 1. **Duolingo** ⭐ Gold Standard
**Why:** The gold standard for gamified learning

**Key Features to Study:**
- Onboarding flow with avatar/character selection
- Bite-sized lesson structure (perfect for assessments)
- Streak counters and progress bars
- Celebration animations and feedback
- Daily goals and reminders
- Mobile-first, playful but professional

**AceQuest Application:**
- Student onboarding flow design
- Lesson completion patterns
- Streak system for daily practice
- XP and level-up mechanics

---

#### 2. **Kahoot!** ⭐ Quiz Platform
**Why:** Quiz-based learning platform with high engagement

**Key Features to Study:**
- Colorful, energetic design (great for Grades 3-8)
- Game lobby and countdown timers
- Immediate feedback on answers
- Leaderboards and rankings
- Question/answer UI patterns

**AceQuest Application:**
- Assessment question display
- Answer selection UI
- Timer countdown for timed quizzes
- Real-time feedback patterns

---

#### 3. **Khan Academy Kids** ⭐ Age-Appropriate
**Why:** Age-appropriate for younger students

**Key Features to Study:**
- Character-driven experience
- Badge and reward systems
- Progress tracking for parents/teachers
- Gentle error handling (no harsh "wrong" messages)
- Simple navigation for children

**AceQuest Application:**
- Grades 3-5 design patterns
- Parent dashboard inspiration
- Encouraging feedback (not harsh)
- Simple navigation for younger students

---

### **Secondary References (Specific Features)**

#### 4. **Quizlet**
**Focus:** Study games and flashcards

**What to Extract:**
- Multiple game modes for same content
- Progress tracking
- Study streaks
- Flashcard interaction patterns

---

#### 5. **Prodigy Math**
**Focus:** Math game for K-8

**What to Extract:**
- RPG-style adventure combined with curriculum
- Character customization and avatars
- Boss battles as assessments
- Parent/teacher dashboards

---

#### 6. **ABCmouse**
**Focus:** Early learning (check Grades 3-5 patterns)

**What to Extract:**
- Ticket/reward economy
- Progress paths and maps
- Age-appropriate visual hierarchy

---

## 📋 What to Study for Each AceQuest Feature

### **For Student Onboarding Flow**
Current file: `student-onboarding-flow.mockup.html`

**Reference Apps:**
- **Duolingo**: Welcome screens, avatar selection, tutorial flow
- **Khan Academy Kids**: Age-appropriate onboarding, parent connection
- **Prodigy Math**: Character creation and customization

**Screens to Capture:**
1. Welcome/splash screen
2. Account creation
3. Avatar/character selection
4. Tutorial/walkthrough (3-5 steps max)
5. First goal setting

**Key Elements:**
- Tone of welcome message
- Number of onboarding steps (keep under 5)
- Skip vs mandatory tutorial
- Visual progress indicator (step 1 of 4)

---

### **For Game/Assessment UI**
Future mockup needed: `student-assessment-game.mockup.html`

**Reference Apps:**
- **Kahoot!**: Question display, answer selection, timer UI
- **Quizlet**: Different game modes for assessments
- **Duolingo**: Lesson completion and feedback screens

**Screens to Capture:**
1. Question display (text + image)
2. Multiple choice answer layout
3. Timer countdown UI
4. Answer feedback (correct/incorrect)
5. Question progress (3 of 10)
6. Game completion screen

**Key Elements:**
- Question card design
- Answer button states (default, selected, correct, incorrect)
- Timer position and style
- Progress bar design
- Encouragement messages

---

### **For Progress & Rewards**
Future mockup needed: `student-rewards-system.mockup.html`

**Reference Apps:**
- **Duolingo**: Streak counters, XP system, level progression
- **Khan Academy**: Badges, energy points, skill trees
- **Prodigy Math**: Inventory, achievements, character progression

**Screens to Capture:**
1. Streak counter widget
2. XP gain animation
3. Badge unlock modal
4. Level-up celebration
5. Achievement showcase
6. Leaderboard

**Key Elements:**
- Streak fire icon and counter
- XP bar animation
- Badge design and unlock flow
- Celebration confetti/animations
- Leaderboard ranking display

---

### **For Dashboard/Home Screen**
Future mockup needed: `student-home-dashboard.mockup.html`

**Reference Apps:**
- **Duolingo**: Daily goals, lesson tree, streak display
- **Khan Academy**: Personalized recommendations, "Continue learning"
- **Kahoot!**: Discover games, saved collections

**Screens to Capture:**
1. Home dashboard layout
2. Quick stats (streak, XP, level)
3. Recommended games
4. Recent activity
5. Achievements preview
6. Navigation menu

**Key Elements:**
- Widget-based layout
- Personalization ("Welcome back, [Name]!")
- Call-to-action placement
- Quick access to profile/settings

---

## 🎨 Key Design Patterns from 2026 Leaders

### **Duolingo's Design DNA**

**Visual Style:**
- Bright colors (#58CC02 green, #1CB0F6 blue)
- Fun, bouncy animations
- Friendly mascot (Duo the owl)
- Rounded corners everywhere

**UX Patterns:**
- Bite-sized lessons (5-10 minutes max)
- Immediate feedback with sound + animation
- Gentle error handling ("Oops, try again!")
- Daily streak emphasis (habit building)
- XP as universal currency

**Onboarding:**
- Personalized path selection
- Goal setting (5, 10, 15 min/day)
- Character introduction
- Quick win in first session

---

### **Kahoot!'s Design DNA**

**Visual Style:**
- Bold, saturated colors (purple, blue, pink)
- Geometric shapes (triangles, circles, squares for answers)
- High contrast
- Energetic, playful

**UX Patterns:**
- Game lobby with PIN code
- Countdown timers (3...2...1...)
- Color-coded answers (not just text)
- Leaderboard after each question
- Music and sound effects

**Engagement:**
- Competition-driven (leaderboards)
- Time pressure (timed questions)
- Social experience (see others' scores)

---

### **Khan Academy's Design DNA**

**Visual Style:**
- Clean, minimal, professional
- Blue and green color scheme
- Lots of white space
- Clear hierarchy

**UX Patterns:**
- Skill trees (visual progress maps)
- Mastery-based progression (practice until proficient)
- Video + practice combo
- Hints and explanations
- Energy points + badges

**Accessibility:**
- High contrast
- Scalable text
- Keyboard navigation
- Screen reader friendly

---

## 💡 Specific Elements to Extract for AceQuest

### **1. Onboarding Screens** (3-5 steps max)

**Duolingo Pattern:**
```
Screen 1: "Learn a language for free. Forever." (value prop)
Screen 2: "Which language?" (personalization)
Screen 3: "Why are you learning?" (goal setting)
Screen 4: "How much time per day?" (commitment)
Screen 5: "Create your profile" (account)
```

**AceQuest Adaptation:**
```
Screen 1: "Assessment Without Anxiety" (value prop)
Screen 2: "Choose your avatar" (personalization)
Screen 3: "Quick tutorial" (how to play)
Screen 4: "Your first quest!" (quick win)
Screen 5: "You earned 50 XP!" (celebration)
```

---

### **2. Question/Answer UI**

**Kahoot! Pattern:**
- Full-screen question display
- Large text (readable from distance)
- 4 answer buttons (colored: red, blue, yellow, green)
- Timer at top center
- Question number indicator

**Duolingo Pattern:**
- Question text at top
- Image/illustration in middle (if applicable)
- Answer options at bottom
- Progress bar at very top
- No timer (self-paced)

**AceQuest Recommendation:**
- Hybrid approach: Duolingo's calmness + Kahoot's energy
- Optional timer (teacher can enable for timed assessments)
- Color + icon for answers (not just text)
- Gentle feedback (green checkmark, not harsh red X)

---

### **3. Celebration Screens**

**Duolingo Pattern:**
```css
/* Modal appears */
background: gradient (yellow to orange)
animation: confetti falling
icon: trophy or star (large)
text: "Lesson Complete!" (32px bold)
subtext: "+10 XP" (24px)
button: "Continue" (primary CTA)
```

**Khan Academy Pattern:**
```css
/* Badge unlock */
background: white modal
animation: badge scales up, sparkles
icon: badge image (128px)
text: "You earned the [Badge Name]!" (24px)
description: what it's for (16px)
button: "Awesome!" (primary CTA)
```

**AceQuest Adaptation:**
- Confetti for first-time achievements
- Subtle animation for regular completion
- Show XP gain prominently
- "Next Quest" CTA to maintain flow

---

### **4. Progress Tracking**

**Streak Counter (Duolingo):**
```html
<div class="streak-widget">
  <span class="fire-icon">🔥</span>
  <span class="streak-count">7</span>
  <span class="streak-label">day streak</span>
</div>
```
- Orange/red gradient background
- Fire emoji prominent
- Large number (32px+)
- Updates daily with animation

**Progress Bar (Khan Academy):**
```html
<div class="skill-progress">
  <div class="skill-name">Multiplication</div>
  <div class="progress-bar">
    <div class="progress-fill" style="width: 60%"></div>
  </div>
  <div class="progress-label">60% to mastery</div>
</div>
```
- Blue fill color
- Percentage or fraction (3/5)
- Clear label of what's being tracked

**AceQuest Application:**
- Use streak for daily login/play
- Progress bars for topic mastery
- Level system (1-50) for overall progression
- Badge collection (visual showcase)

---

### **5. Navigation Patterns**

**Student App (Duolingo pattern):**
```
Bottom Tab Bar:
[🏠 Home] [📚 Library] [🏆 Quests] [👤 Profile]
```

**Teacher Dashboard (Khan pattern):**
```
Left Sidebar:
- Dashboard
- Students
- Assignments
- Reports
- Settings
```

**AceQuest Navigation:**
- Students: Bottom tabs (mobile-friendly, thumb-friendly)
- Teachers: Sidebar (data-dense, desktop-first)
- Parents: Top tabs (simple, limited options)

---

## 🔍 Mobbin Search & Capture Strategy

### **Filters to Use:**
- **Category**: Education, Kids, Productivity
- **Platform**: iOS (cleaner design) + Android (wider reach)
- **Screen Types**:
  - Onboarding
  - Home/Dashboard
  - Game/Quiz
  - Profile
  - Progress/Stats
  - Rewards/Achievements

### **For Each App, Capture:**

1. **Screenshot + Notes**
   - What works well?
   - What doesn't apply to AceQuest?
   - Color palette used
   - Typography choices
   - Spacing and layout

2. **Interaction Patterns**
   - Button states
   - Transitions
   - Animations (described)
   - Gestures (swipe, tap, long-press)

3. **Content Strategy**
   - Tone of voice
   - Encouragement messages
   - Error handling language
   - Tutorial copy

---

## 📊 Feature Mapping: App Reference → AceQuest

| AceQuest Feature | Reference App | Specific Screens to Study |
|------------------|---------------|---------------------------|
| Student Onboarding | Duolingo | Welcome, goal setting, first lesson |
| Avatar Selection | Prodigy Math | Character customization, avatar options |
| Tutorial/Walkthrough | Khan Academy Kids | Interactive tutorial, tooltips |
| Assessment UI | Kahoot! | Question display, answer selection, timer |
| Answer Feedback | Duolingo | Correct/incorrect states, explanations |
| Progress Bar | Khan Academy | Skill mastery, progress tracking |
| Streak System | Duolingo | Streak counter, streak freeze, reminders |
| XP System | Duolingo | XP gain animation, level-up |
| Badge System | Khan Academy | Badge unlock, badge showcase |
| Leaderboard | Kahoot! | Ranking display, podium, scores |
| Daily Goals | Duolingo | Goal setting, daily reminder |
| Home Dashboard | Duolingo | Lesson tree, stats widget, CTA placement |
| Game Library | Kahoot! | Browse games, categories, search |
| Profile Settings | Duolingo | Avatar, stats, settings, logout |
| Parent Dashboard | Khan Academy | Progress reports, time spent, recommendations |
| Teacher Dashboard | Kahoot! | Class management, reports, analytics |
| Offline Mode | Duolingo | Downloaded lessons, sync indicator |
| Low-Data Mode | N/A | Create original pattern (no good reference) |
| Celebration Screen | Duolingo | Confetti, trophy, XP display |
| Error States | Duolingo | Gentle corrections, try again prompts |

---

## 🎨 Design System Extraction

### **Color Palettes to Study:**

**Duolingo:**
- Primary: #58CC02 (bright green)
- Secondary: #1CB0F6 (bright blue)
- Accent: #FF9600 (orange)
- Error: #EA2B2B (red, but softened in use)

**Kahoot!:**
- Primary: #46178F (purple)
- Accent: #E21B3C (pink-red)
- Answers: #E21B3C (red), #1368CE (blue), #D89E00 (yellow), #26890C (green)

**Khan Academy:**
- Primary: #14BF96 (teal-green)
- Secondary: #1C758A (blue)
- Neutral: Grays
- Badges: Gold, silver, bronze variants

**For AceQuest:**
- Already defined: Purple #6366F1, Orange #F59E0B, Green #10B981
- ✅ Good balance between Duolingo's playfulness and Khan's professionalism

---

### **Typography to Study:**

**Duolingo:**
- Headings: Bold, rounded sans-serif
- Body: Regular sans-serif, 16-18px
- Large text for answers (24px+)

**Kahoot!:**
- Headings: Extra bold, all caps sometimes
- Body: Bold for emphasis, 18-20px
- Huge text for questions (32px+)

**Khan Academy:**
- Headings: Semi-bold sans-serif
- Body: Regular, excellent readability
- Math: Specific font for equations

**For AceQuest:**
- ✅ Already using system fonts (good for performance)
- Consider: Bolder headings for younger students (Grades 3-5)

---

### **Animation Patterns:**

**Duolingo:**
- Bounce animations (playful)
- Confetti on success
- Shake on error (gentle)
- Slide transitions between screens
- Progress bar fills smoothly

**Kahoot!:**
- Countdown timer pulsates
- Correct answer grows/pulses
- Leaderboard slides in from right
- Energetic, fast animations

**Khan Academy:**
- Subtle fades
- Smooth scrolling
- Badge scale-up on unlock
- Minimal, professional

**For AceQuest:**
- Grades 3-5: More Duolingo-style (playful)
- Grades 6-8: More Khan-style (subtle)
- Or: Balanced approach (option in v1.2 framework)

---

## 📝 Specific Mockups to Create

Based on Mobbin research, create these mockups:

### **Priority 1 (MVP):**
1. ✅ `student-login-signup.mockup.html` - DONE
2. ✅ `student-onboarding-flow.mockup.html` - DONE
3. ⏱️ `student-home-dashboard.mockup.html` - NEEDED
4. ⏱️ `student-assessment-game.mockup.html` - NEEDED
5. ⏱️ `student-results-feedback.mockup.html` - NEEDED

### **Priority 2 (Post-MVP):**
6. ⏱️ `student-rewards-badges.mockup.html`
7. ⏱️ `student-profile-stats.mockup.html`
8. ⏱️ `teacher-dashboard-overview.mockup.html`
9. ⏱️ `teacher-student-reports.mockup.html`
10. ⏱️ `parent-progress-view.mockup.html`

---

## 🎯 Action Items for Mobbin Research

### **This Week:**
- [ ] Search Duolingo on Mobbin
  - [ ] Capture 5 onboarding screens
  - [ ] Capture 3 lesson completion screens
  - [ ] Capture streak widget
  - [ ] Capture XP/level UI
  - [ ] Note animation patterns

- [ ] Search Kahoot! on Mobbin
  - [ ] Capture question display
  - [ ] Capture answer selection UI
  - [ ] Capture timer countdown
  - [ ] Capture leaderboard
  - [ ] Note color usage for answers

- [ ] Search Khan Academy Kids on Mobbin
  - [ ] Capture character selection
  - [ ] Capture badge system
  - [ ] Capture parent dashboard
  - [ ] Capture gentle error states
  - [ ] Note age-appropriate patterns

### **Next Week:**
- [ ] Create `student-home-dashboard.mockup.html` based on research
- [ ] Create `student-assessment-game.mockup.html` based on Kahoot! patterns
- [ ] Update UI/UX framework with specific pattern references

---

## 📚 Additional Resources

**Industry Articles:**
- [Gamification in EdTech – Lessons from Duolingo, Khan Academy, IXL, and Kahoot!](https://prodwrks.com/gamification-in-edtech-lessons-from-duolingo-khan-academy-ixl-and-kahoot/)
- [How to Design Like Duolingo: Gamification & Engagement](https://www.uinkits.com/blog-post/how-to-design-like-duolingo-gamification-engagement)
- [Duolingo - an in-depth UX and user onboarding breakdown](https://userguiding.com/blog/duolingo-onboarding-ux)
- [Best Education Apps for Students in 2025](https://schoolposterprinters.com/best-education-apps-for-students-in-2025-boost-learning/)

---

## 🎨 Design Principles Summary

From studying these apps, key principles for AceQuest:

1. **Playful but Professional** - Duolingo does this perfectly
2. **Immediate Feedback** - Kahoot's instant answer feedback
3. **Gentle Corrections** - Khan Academy's "Try again" approach
4. **Habit Formation** - Duolingo's streaks and daily goals
5. **Visual Progress** - Khan Academy's skill trees and progress bars
6. **Age Appropriateness** - Khan Kids for younger, Prodigy for balance
7. **Mobile-First** - All apps prioritize mobile experience
8. **Accessibility** - Khan Academy's high contrast and clear hierarchy

**Apply to AceQuest:**
- ✅ All principles align with our "Assessment Without Anxiety" mission
- ✅ UI/UX Framework v1.2 already incorporates these
- Next: Translate principles into specific mockups

---

**Last Updated:** 2026-02-09
**Next Review:** After Mobbin research is complete (1 week)
