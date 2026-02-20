# Student User Journey - V1 (MVP)
**Complete flow from Login to Logout**

**Version:** 1.0 (Months 1-6 Pilot)
**User Type:** Grade 3-8 Student (B2B - School enrollment)
**Last Updated:** 2026-02-09

---

## Journey Overview

```
┌─────────────┐    ┌──────────────┐    ┌─────────────┐    ┌──────────────┐    ┌─────────────┐
│   LOGIN     │ -> │  ONBOARDING  │ -> │    HOME     │ -> │  GAME PLAY   │ -> │   LOGOUT    │
│   SCREEN    │    │  (First-time)│    │  DASHBOARD  │    │  EXPERIENCE  │    │             │
└─────────────┘    └──────────────┘    └─────────────┘    └──────────────┘    └─────────────┘
     │                    │                   │                   │                   │
  Account             Avatar            Browse/Select         Assessment          End Session
  Creation            Setup             Games                 Completion
```

**Total Journey Time (First Session):** ~30-45 minutes
**Total Journey Time (Return Session):** ~20-30 minutes

---

## STEP 1: LOGIN / ACCOUNT CREATION

### 1.1 Initial Landing Screen

**URL/Route:** `/` or App Launch
**First-time user:** Not logged in
**Returning user:** Auto-login if remembered

#### Screen Elements

**Hero Section:**
```
┌────────────────────────────────────────────────┐
│                                                │
│        🎮  Welcome to AceQuest!  🚀            │
│                                                │
│    "Play games. Level up your learning."      │
│                                                │
│    [Visual: Animated characters/games]        │
│                                                │
│         ┌──────────────────────┐              │
│         │   START PLAYING →    │              │
│         └──────────────────────┘              │
│                                                │
│         Already have an account?              │
│              👉 Log In                         │
│                                                │
└────────────────────────────────────────────────┘
```

**User Actions:**
- Tap "START PLAYING" → Goes to Account Creation
- Tap "Log In" → Goes to Login Form

---

### 1.2a Account Creation (First-Time Users)

**URL/Route:** `/signup`
**Time:** 2-3 minutes

#### Screen Layout

```
┌────────────────────────────────────────────────┐
│  ← Back                      AceQuest Logo     │
├────────────────────────────────────────────────┤
│                                                │
│         Create Your Account                    │
│                                                │
│  ┌──────────────────────────────────────────┐ │
│  │  Your Name                                │ │
│  │  [____________]                           │ │
│  └──────────────────────────────────────────┘ │
│                                                │
│  ┌──────────────────────────────────────────┐ │
│  │  Email                                    │ │
│  │  [____________]                           │ │
│  └──────────────────────────────────────────┘ │
│                                                │
│  ┌──────────────────────────────────────────┐ │
│  │  Create Password                          │ │
│  │  [____________]   👁                      │ │
│  └──────────────────────────────────────────┘ │
│                                                │
│  Grade: [Dropdown: 3|4|5|6|7|8]               │
│                                                │
│  ┌────────────────────────────────────────┐   │
│  │        CREATE ACCOUNT →                │   │
│  └────────────────────────────────────────┘   │
│                                                │
│  By signing up, you agree to our Terms        │
│                                                │
└────────────────────────────────────────────────┘
```

**Validation:**
- Name: Required, 2+ characters
- Email: Required, valid email format
- Password: 6+ characters (student-friendly)
- Grade: Must select from dropdown

**Notes:**
- **School code removed** from signup for reduced friction
- Students can add school code later in Profile settings
- All users start as independent (B2C) users
- When school code added, account becomes school-linked (B2B)

**Success:** → Goes to Onboarding (Avatar Selection)

---

### 1.2b Login (Returning Users)

**URL/Route:** `/login`
**Time:** 30 seconds

#### Screen Layout

```
┌────────────────────────────────────────────────┐
│  ← Back                      AceQuest Logo     │
├────────────────────────────────────────────────┤
│                                                │
│         Welcome Back! 👋                       │
│                                                │
│  ┌──────────────────────────────────────────┐ │
│  │  Email or Username                        │ │
│  │  [____________]                           │ │
│  └──────────────────────────────────────────┘ │
│                                                │
│  ┌──────────────────────────────────────────┐ │
│  │  Password                                 │ │
│  │  [____________]   👁                      │ │
│  └──────────────────────────────────────────┘ │
│                                                │
│  ☐ Remember me                                │
│                                                │
│  ┌────────────────────────────────────────┐   │
│  │           LOG IN →                     │   │
│  └────────────────────────────────────────┘   │
│                                                │
│  Forgot password? | Need help?                │
│                                                │
└────────────────────────────────────────────────┘
```

**Success:** → Goes directly to Home Dashboard
**First-time after account creation:** → Goes to Onboarding

---

## STEP 2: ONBOARDING (First-Time Users Only)

### 2.1 Avatar Selection

**URL/Route:** `/onboarding/avatar`
**Time:** 1-2 minutes
**Shown:** Only on first login

#### Screen Layout

```
┌────────────────────────────────────────────────┐
│                 Step 1 of 3                    │
├────────────────────────────────────────────────┤
│                                                │
│      Choose Your Game Character! 🎨            │
│                                                │
│  ┌─────┐  ┌─────┐  ┌─────┐  ┌─────┐          │
│  │ 🦁  │  │ 🐯  │  │ 🦊  │  │ 🐻  │          │
│  │Lion │  │Tiger│  │ Fox │  │Bear │          │
│  └─────┘  └─────┘  └─────┘  └─────┘          │
│                                                │
│  ┌─────┐  ┌─────┐  ┌─────┐  ┌─────┐          │
│  │ 🚀  │  │ 🧙  │  │ 🦸  │  │ 🤖  │          │
│  │Space│  │Wizard│ │Hero │  │Robot│          │
│  └─────┘  └─────┘  └─────┘  └─────┘          │
│                                                │
│         [More avatars scroll...]               │
│                                                │
│  ┌────────────────────────────────────────┐   │
│  │         CONTINUE →                     │   │
│  └────────────────────────────────────────┘   │
│                                                │
│            Skip for now                        │
│                                                │
└────────────────────────────────────────────────┘
```

**User Action:** Select avatar → Tap Continue
**Skip Option:** Available (can customize later in profile)

---

### 2.2 Interactive Tutorial

**URL/Route:** `/onboarding/tutorial`
**Time:** 2-3 minutes
**Shown:** Only on first login (can skip)

#### Tutorial Flow (3 Screens)

**Screen 1: Welcome**
```
┌────────────────────────────────────────────────┐
│                 Step 2 of 3                    │
├────────────────────────────────────────────────┤
│                                                │
│     👋 Hi [Student Name]!                      │
│                                                │
│  [Animated character waving]                   │
│                                                │
│  Welcome to AceQuest! Here's how it works:    │
│                                                │
│  ✨ You'll play fun games                      │
│  📊 Each game helps you learn                  │
│  🏆 Earn badges and level up                   │
│  📈 Track your progress                        │
│                                                │
│  Ready to see how it works?                   │
│                                                │
│  ┌────────────────────────────────────────┐   │
│  │         SHOW ME →                      │   │
│  └────────────────────────────────────────┘   │
│                                                │
│            Skip tutorial                       │
│                                                │
└────────────────────────────────────────────────┘
```

**Screen 2: Finding Games**
```
┌────────────────────────────────────────────────┐
│              Quick Tour (1/2)                  │
├────────────────────────────────────────────────┤
│                                                │
│  [Screenshot of Home Dashboard with highlight] │
│                                                │
│     ↓ Here's where you'll see your games      │
│                                                │
│  ┌────────────────────────────────┐           │
│  │ Recommended Games              │ ← Tap here│
│  │ ┌─────┐ ┌─────┐ ┌─────┐       │           │
│  │ │Game1│ │Game2│ │Game3│       │           │
│  │ └─────┘ └─────┘ └─────┘       │           │
│  └────────────────────────────────┘           │
│                                                │
│  Your teacher assigns games, or you can       │
│  explore and play any game you like!          │
│                                                │
│  ┌────────────────────────────────────────┐   │
│  │         NEXT →                         │   │
│  └────────────────────────────────────────┘   │
│                                                │
└────────────────────────────────────────────────┘
```

**Screen 3: Playing Games**
```
┌────────────────────────────────────────────────┐
│              Quick Tour (2/2)                  │
├────────────────────────────────────────────────┤
│                                                │
│  [Screenshot of game interface with highlights]│
│                                                │
│  When you play a game:                         │
│                                                │
│  📖 Follow the story                           │
│  🎯 Answer questions as part of the game       │
│  💡 Get instant feedback                       │
│  🎉 Earn badges when you complete it           │
│                                                │
│  Don't worry about getting everything right!   │
│  This is about learning, not testing.          │
│                                                │
│  ┌────────────────────────────────────────┐   │
│  │    LET'S PLAY MY FIRST GAME! →        │   │
│  └────────────────────────────────────────┘   │
│                                                │
│            Skip to home                        │
│                                                │
└────────────────────────────────────────────────┘
```

**After Tutorial:** → Goes to Home Dashboard
**OR if "Let's Play":** → Goes to Tutorial Game (short 5-min demo game)

---

## STEP 3: HOME DASHBOARD

### 3.1 Main Dashboard

**URL/Route:** `/student/home`
**Time:** Variable (browsing hub)
**Frequency:** Every session start

#### Screen Layout (Desktop/Tablet)

```
┌────────────────────────────────────────────────────────────────┐
│  AceQuest 🎮        [Search games...]           🔔 👤 Aarav ▼  │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  👋 Welcome back, Aarav!                      🔥 Streak: 3 days│
│                                                                │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │  Continue Playing                                         │ │
│  │  ┌──────────────┐                                         │ │
│  │  │  Space Math  │  75% complete                          │ │
│  │  │  [Progress]  │  ⏱ 10 min left                         │ │
│  │  │  [Image]     │  [CONTINUE →]                          │ │
│  │  └──────────────┘                                         │ │
│  └──────────────────────────────────────────────────────────┘ │
│                                                                │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │  Recommended for You                      [View All →]   │ │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐ │ │
│  │  │Fraction  │  │Grammar   │  │Science   │  │More...   │ │ │
│  │  │Adventure │  │Quest     │  │Explorer  │  │          │ │ │
│  │  │          │  │          │  │          │  │          │ │ │
│  │  │Math 📊  │  │English🔤│  │Science🔬│  │          │ │ │
│  │  │⏱ 20 min │  │⏱ 15 min │  │⏱ 25 min │  │          │ │ │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘ │ │
│  └──────────────────────────────────────────────────────────┘ │
│                                                                │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │  Assigned by Your Teacher                 [View All →]   │ │
│  │  ┌──────────┐  ┌──────────┐                              │ │
│  │  │Decimals  │  │Reading   │                              │ │
│  │  │Practice  │  │Challenge │                              │ │
│  │  │          │  │          │                              │ │
│  │  │Math 📊  │  │English🔤│                              │ │
│  │  │Due: 2 days│  │Due: 5 days│                            │ │
│  │  └──────────┘  └──────────┘                              │ │
│  └──────────────────────────────────────────────────────────┘ │
│                                                                │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │  Your Progress                                            │ │
│  │                                                            │ │
│  │  Math      ████████░░ 80%     5 games completed          │ │
│  │  English   ██████░░░░ 60%     4 games completed          │ │
│  │  Science   ███████░░░ 70%     4 games completed          │ │
│  │                                                            │ │
│  │  [View Detailed Progress →]                               │ │
│  └──────────────────────────────────────────────────────────┘ │
│                                                                │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │  Recent Achievements                      [View All →]   │ │
│  │  🏆 Fraction Master       🌟 Reading Rockstar            │ │
│  │  Earned 2 days ago        Earned 4 days ago              │ │
│  └──────────────────────────────────────────────────────────┘ │
│                                                                │
└────────────────────────────────────────────────────────────────┘
│  🏠 Home    🎮 Games    🏆 Achievements    👤 Profile          │
└────────────────────────────────────────────────────────────────┘
```

#### Screen Elements Explained

**Top Navigation Bar:**
- Logo (clickable → returns to home)
- Search bar (find games by name or topic)
- Notifications bell 🔔 (assignments, achievements)
- Profile dropdown (settings, logout)
- Streak indicator (gamification for daily usage)

**Continue Playing Section:**
- Shows incomplete game (if any)
- Progress bar (% complete)
- Time estimate to finish
- Large "CONTINUE" button

**Recommended for You:**
- AI-suggested games based on learning gaps
- 3-4 game cards visible, horizontal scroll for more
- Each card shows: thumbnail, title, subject icon, duration

**Assigned by Teacher:**
- Games specifically assigned by teacher
- Due date prominently displayed
- Visual indicator if due soon (yellow/red highlight)

**Your Progress:**
- Subject-wise progress bars
- Number of games completed per subject
- Link to detailed progress page

**Recent Achievements:**
- Last 2-3 badges earned
- Date earned
- Link to full achievement wall

**Bottom Navigation (Mobile):**
- Home, Games, Achievements, Profile
- Always visible for easy navigation

---

### 3.2 User Actions from Home

**Primary Actions:**
1. **Continue incomplete game** → Go to Game Play (Step 4)
2. **Select recommended game** → Go to Game Preview → Game Play
3. **Browse all games** → Go to Game Library (3.3)
4. **View profile** → Go to Profile (3.4)
5. **Check achievements** → Go to Achievements (3.5)
6. **Search for game** → Search results → Game preview

---

### 3.3 Game Library / Browse

**URL/Route:** `/student/games`
**Time:** 2-5 minutes (browsing)

#### Screen Layout

```
┌────────────────────────────────────────────────────────────────┐
│  ← Back to Home                                🔔 👤 Aarav ▼   │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  Game Library                      [Search games...]          │
│                                                                │
│  Filter by:  [All Subjects ▼] [All Grades ▼] [Duration ▼]    │
│  Sort by:    [Recommended ▼]                                  │
│                                                                │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐     │
│  │Fraction  │  │Grammar   │  │Science   │  │Geometry  │     │
│  │Adventure │  │Quest     │  │Explorer  │  │Challenge │     │
│  │⭐⭐⭐⭐⭐│  │⭐⭐⭐⭐░│  │⭐⭐⭐⭐░│  │⭐⭐⭐░░│     │
│  │Math 📊  │  │English🔤│  │Science🔬│  │Math 📊  │     │
│  │⏱ 20 min │  │⏱ 15 min │  │⏱ 25 min │  │⏱ 30 min │     │
│  │Grade 5-6 │  │Grade 4-6 │  │Grade 5-7 │  │Grade 6-8 │     │
│  │✓Completed│  │          │  │          │  │          │     │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘     │
│                                                                │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐     │
│  │Reading   │  │Algebra   │  │Plants &  │  │Verb      │     │
│  │Explorer  │  │Basics    │  │Animals   │  │Tenses    │     │
│  │⭐⭐⭐⭐░│  │⭐⭐⭐⭐⭐│  │⭐⭐⭐⭐░│  │⭐⭐⭐⭐░│     │
│  │English🔤│  │Math 📊  │  │Science🔬│  │English🔤│     │
│  │⏱ 18 min │  │⏱ 22 min │  │⏱ 20 min │  │⏱ 15 min │     │
│  │Grade 3-5 │  │Grade 7-8 │  │Grade 4-6 │  │Grade 5-7 │     │
│  │          │  │          │  │          │  │          │     │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘     │
│                                                                │
│  [Load More Games...]                                         │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

#### Screen Elements

**Filters:**
- **Subject:** All, Math, English, Science
- **Grade:** All, 3, 4, 5, 6, 7, 8
- **Duration:** All, 5-15 min, 15-25 min, 25-35 min
- **Status:** All, Not Started, In Progress, Completed

**Sort Options:**
- Recommended for me (default - AI-based)
- Newest first
- Most popular
- Shortest first

**Game Cards:**
- Thumbnail image
- Title
- Star rating (difficulty/complexity)
- Subject icon
- Duration
- Grade range
- Completion status (✓ if completed)

**User Actions:**
- Click game card → Game Preview (3.3.1)
- Apply filters → Updated results
- Search → Filtered results
- Scroll → Load more games

---

### 3.3.1 Game Preview (Before Playing)

**URL/Route:** `/student/games/{game-id}/preview`
**Time:** 30 seconds - 1 minute

#### Screen Layout

```
┌────────────────────────────────────────────────────────────────┐
│  ← Back to Games                               🔔 👤 Aarav ▼   │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  [Large Game Banner Image]                                     │
│                                                                │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │                                                            │ │
│  │  🎮 Fraction Adventure                                    │ │
│  │                                                            │ │
│  │  Help Captain Fraction explore the number galaxy by       │ │
│  │  solving fraction challenges! Navigate through asteroid   │ │
│  │  fields, collect star crystals, and master fractions.     │ │
│  │                                                            │ │
│  │  📊 Subject: Math                                         │ │
│  │  ⏱ Duration: 20 minutes                                   │ │
│  │  🎯 Grade Level: 5-6                                      │ │
│  │  ⭐ Difficulty: ⭐⭐⭐⭐░                               │ │
│  │                                                            │ │
│  │  What you'll learn:                                       │ │
│  │  • Adding and subtracting fractions                       │ │
│  │  • Comparing fractions                                    │ │
│  │  • Simplifying fractions                                  │ │
│  │                                                            │ │
│  │  ┌────────────────────────────────────────────┐          │ │
│  │  │          🚀 START GAME                     │          │ │
│  │  └────────────────────────────────────────────┘          │ │
│  │                                                            │ │
│  │  [Preview Screenshots/Video]                              │ │
│  │                                                            │ │
│  └──────────────────────────────────────────────────────────┘ │
│                                                                │
│  📊 Other students found this helpful:                        │
│  "Fun way to practice fractions!" - Grade 5 student           │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

**User Actions:**
- Tap "START GAME" → Go to Game Play (Step 4)
- Tap "Back" → Return to Game Library

---

### 3.4 Profile Page

**URL/Route:** `/student/profile`
**Time:** 1-3 minutes

#### Screen Layout

```
┌────────────────────────────────────────────────────────────────┐
│  ← Back to Home                                🔔 Logout       │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│     [Avatar - Large]                                           │
│                                                                │
│     Aarav Kumar                                                │
│     Grade 5 | Independent Learner                             │
│     🔥 Streak: 3 days | Level 12 Math Wizard                  │
│                                                                │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │  Games Completed                    13 games              │ │
│  │  Total Time Played                  4 hours 25 min        │ │
│  │  Achievements Earned                8 badges              │ │
│  └──────────────────────────────────────────────────────────┘ │
│                                                                │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │  School Connection                     [Not Connected]   │ │
│  │                                                            │ │
│  │  🏫 Connect to your school to:                            │ │
│  │  • See teacher assignments                                │ │
│  │  • Join your classmates                                   │ │
│  │  • Share progress with teachers                           │ │
│  │                                                            │ │
│  │  ┌────────────────────────────────────────┐              │ │
│  │  │  ADD SCHOOL CODE                       │              │ │
│  │  └────────────────────────────────────────┘              │ │
│  │                                                            │ │
│  └──────────────────────────────────────────────────────────┘ │
│                                                                │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │  Your Strengths                                           │ │
│  │                                                            │ │
│  │  ⭐ Multiplication - You're great at this!                │ │
│  │  ⭐ Reading Comprehension - Keep it up!                   │ │
│  │  ⭐ Scientific Inquiry - Awesome work!                    │ │
│  │                                                            │ │
│  └──────────────────────────────────────────────────────────┘ │
│                                                                │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │  Achievement Wall                         [View All →]   │ │
│  │                                                            │ │
│  │  🏆        🌟        🎯        ⭐        🔥        🎖     │ │
│  │  Fraction  Reading   Problem   Science   Streak   Math   │ │
│  │  Master    Star      Solver    Explorer  Champion Hero   │ │
│  │                                                            │ │
│  └──────────────────────────────────────────────────────────┘ │
│                                                                │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │  Settings                                                 │ │
│  │                                                            │ │
│  │  ✏️ Edit Profile (change avatar, name)                   │ │
│  │  🔔 Notifications (email reminders)                       │ │
│  │  🔒 Privacy (who can see my progress)                    │ │
│  │  ❓ Help & Support                                        │ │
│  │                                                            │ │
│  └──────────────────────────────────────────────────────────┘ │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

**User Actions:**
- Add school code (optional, can be done anytime)
- View detailed achievements
- Edit profile (avatar, name)
- Adjust settings
- Access help/support
- Logout (top right)

**Notes:**
- Status shows "Independent Learner" if no school connected
- Shows school name if connected (e.g., "Sunrise International School")
- School connection section visible to all users
- Benefits clearly listed to encourage connection

---

### 3.5 Achievements Page

**URL/Route:** `/student/achievements`
**Time:** 1-2 minutes

#### Screen Layout

```
┌────────────────────────────────────────────────────────────────┐
│  ← Back to Profile                             🔔 👤 Aarav ▼   │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  🏆 Your Achievements                                          │
│                                                                │
│  You've earned 8 out of 24 badges!                            │
│  [████████░░░░░░░░░░░░░░] 33%                                 │
│                                                                │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │  Earned (8)                                               │ │
│  │                                                            │ │
│  │  🏆 Fraction Master          Earned 2 days ago            │ │
│  │  Complete 5 fraction games                                │ │
│  │                                                            │ │
│  │  🌟 Reading Rockstar         Earned 4 days ago            │ │
│  │  Ace 3 reading comprehension games                        │ │
│  │                                                            │ │
│  │  🔥 3-Day Streak            Earned today!                 │ │
│  │  Play games 3 days in a row                               │ │
│  │                                                            │ │
│  │  [5 more badges...]                                       │ │
│  │                                                            │ │
│  └──────────────────────────────────────────────────────────┘ │
│                                                                │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │  In Progress (5)                                          │ │
│  │                                                            │ │
│  │  🎯 Problem Solver           3/5 complete                 │ │
│  │  Complete 5 word problem games                            │ │
│  │  [Progress bar: 60%]                                      │ │
│  │                                                            │ │
│  │  ⭐ Science Explorer         2/5 complete                 │ │
│  │  Complete 5 science games                                 │ │
│  │  [Progress bar: 40%]                                      │ │
│  │                                                            │ │
│  │  [3 more in-progress badges...]                           │ │
│  │                                                            │ │
│  └──────────────────────────────────────────────────────────┘ │
│                                                                │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │  Locked (11)                                              │ │
│  │                                                            │ │
│  │  🔒 Algebra Ace              Requirements:                │ │
│  │  Complete 8 algebra games                                 │ │
│  │                                                            │ │
│  │  [10 more locked badges...]                               │ │
│  │                                                            │ │
│  └──────────────────────────────────────────────────────────┘ │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

---

## STEP 4: GAME PLAY EXPERIENCE

### 4.1 Game Loading Screen

**URL/Route:** `/student/play/{game-id}`
**Time:** 2-5 seconds

#### Screen Layout

```
┌────────────────────────────────────────────────┐
│                                                │
│                                                │
│         [Animated game logo/character]         │
│                                                │
│           Loading Fraction Adventure...        │
│                                                │
│           [████████░░] 80%                     │
│                                                │
│                                                │
└────────────────────────────────────────────────┘
```

---

### 4.2 Game Introduction / Story Setup

**URL/Route:** `/student/play/{game-id}/intro`
**Time:** 1-2 minutes
**Skippable:** Yes (for returning players)

#### Screen Layout

```
┌────────────────────────────────────────────────────────────────┐
│  [Skip Intro →]                                                │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│     [Full-screen animated illustration]                        │
│                                                                │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │                                                            │ │
│  │  🚀 Welcome, Space Cadet Aarav!                          │ │
│  │                                                            │ │
│  │  Captain Fraction needs your help! The Number Galaxy     │ │
│  │  is in trouble. Asteroid fields are blocking the path    │ │
│  │  to Planet Prime.                                         │ │
│  │                                                            │ │
│  │  Your mission: Navigate through the asteroid fields      │ │
│  │  by solving fraction puzzles. Each correct answer        │ │
│  │  clears a path forward!                                   │ │
│  │                                                            │ │
│  │  Ready for your mission?                                  │ │
│  │                                                            │ │
│  │           [🚀 START MISSION →]                            │ │
│  │                                                            │ │
│  └──────────────────────────────────────────────────────────┘ │
│                                                                │
│  [Audio: Spaceship sounds, background music]                  │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

**User Action:** Tap "START MISSION" → Go to first question

---

### 4.3 Game Play Interface (Core Assessment)

**URL/Route:** `/student/play/{game-id}/question/{question-num}`
**Time:** 15-25 minutes (entire game)
**Question Count:** 12-20 questions (adaptive)

#### Screen Layout (Example Question)

```
┌────────────────────────────────────────────────────────────────┐
│  [❚❚ Pause]                                    Progress: ▓▓▓░░│
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  [Game Scene Illustration]                                     │
│  🚀 Spaceship approaching asteroid field                       │
│                                                                │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │                                                            │ │
│  │  🎮 Story Context:                                        │ │
│  │                                                            │ │
│  │  You see two asteroids ahead! The first asteroid          │ │
│  │  covers 2/5 of the path, and the second covers 1/5        │ │
│  │  of the path.                                              │ │
│  │                                                            │ │
│  │  Question: What fraction of the total path is blocked?    │ │
│  │                                                            │ │
│  │  ┌────────────────────────────────────────────┐          │ │
│  │  │  A) 1/5                                     │          │ │
│  │  └────────────────────────────────────────────┘          │ │
│  │                                                            │ │
│  │  ┌────────────────────────────────────────────┐          │ │
│  │  │  B) 2/5                                     │          │ │
│  │  └────────────────────────────────────────────┘          │ │
│  │                                                            │ │
│  │  ┌────────────────────────────────────────────┐          │ │
│  │  │  C) 3/5                                     │  ← Selected│ │
│  │  └────────────────────────────────────────────┘          │ │
│  │                                                            │ │
│  │  ┌────────────────────────────────────────────┐          │ │
│  │  │  D) 4/5                                     │          │ │
│  │  └────────────────────────────────────────────┘          │ │
│  │                                                            │ │
│  │           [SUBMIT ANSWER →]                               │ │
│  │                                                            │ │
│  │  💡 Need a hint?                                          │ │
│  │                                                            │ │
│  └──────────────────────────────────────────────────────────┘ │
│                                                                │
│  [Background music playing softly]                             │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

#### Screen Elements

**Top Bar:**
- Pause button (pauses game, saves state)
- Progress indicator (visual bars, NOT "Question 3 of 15")

**Game Scene:**
- Animated illustration relevant to question
- Characters/objects that relate to the story

**Question Panel:**
- **Story context:** Question embedded in narrative
- **Question:** Clear, grade-appropriate language
- **Answer options:** 4 multiple-choice (A/B/C/D)
- **Submit button:** Only active when answer selected
- **Hint button:** Available (doesn't penalize)

---

### 4.4 Immediate Feedback (Correct Answer)

**Time:** 3-5 seconds per question

#### Screen Layout

```
┌────────────────────────────────────────────────────────────────┐
│  [❚❚ Pause]                                    Progress: ▓▓▓░░│
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  [Animated celebration: Asteroid explodes, path clears]        │
│                                                                │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │                                                            │ │
│  │  ✅ Excellent work, Aarav! 🎉                            │ │
│  │                                                            │ │
│  │  You're right! When you add 2/5 + 1/5, you get 3/5       │ │
│  │  of the path blocked. The spaceship can navigate         │ │
│  │  through the remaining 2/5!                               │ │
│  │                                                            │ │
│  │  +10 XP earned! 🌟                                        │ │
│  │                                                            │ │
│  │           [CONTINUE →]                                    │ │
│  │                                                            │ │
│  └──────────────────────────────────────────────────────────┘ │
│                                                                │
│  [Sound: Success chime, positive reinforcement]               │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

**User Action:** Tap "CONTINUE" → Next question
**Animation:** Smooth transition to next scenario

---

### 4.5 Immediate Feedback (Incorrect Answer)

**Time:** 5-8 seconds per question

#### Screen Layout

```
┌────────────────────────────────────────────────────────────────┐
│  [❚❚ Pause]                                    Progress: ▓▓▓░░│
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  [Animation: Spaceship wobbles, alert signal]                  │
│                                                                │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │                                                            │ │
│  │  ⚠️ Not quite, but that's okay! 💡                       │ │
│  │                                                            │ │
│  │  Let's think about it: When we add fractions with the    │ │
│  │  same denominator, we add the numerators.                │ │
│  │                                                            │ │
│  │  2/5 + 1/5 = (2+1)/5 = 3/5                               │ │
│  │                                                            │ │
│  │  The correct answer was C) 3/5                           │ │
│  │                                                            │ │
│  │  [Visual: Fraction addition shown with diagrams]         │ │
│  │                                                            │ │
│  │           [GOT IT! →]                                     │ │
│  │                                                            │ │
│  └──────────────────────────────────────────────────────────┘ │
│                                                                │
│  [Sound: Gentle alert, encouraging tone]                      │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

**User Action:** Tap "GOT IT" → Next question
**Tone:** Encouraging, not punitive
**No visible score deduction** (students don't see score)

---

### 4.6 Mid-Game Checkpoint (Optional)

**Frequency:** Every 5-7 questions
**Time:** 15-20 seconds

#### Screen Layout

```
┌────────────────────────────────────────────────────────────────┐
│                                                                │
│     [Animated scene: Spaceship docked at space station]        │
│                                                                │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │                                                            │ │
│  │  🚀 Checkpoint Reached!                                   │ │
│  │                                                            │ │
│  │  Great progress, Aarav! You've cleared half of the       │ │
│  │  asteroid field. Captain Fraction is impressed! 💪       │ │
│  │                                                            │ │
│  │  Take a quick break if you need one, or keep going!      │ │
│  │                                                            │ │
│  │  ┌──────────────┐     ┌──────────────┐                  │ │
│  │  │ TAKE A BREAK │     │  CONTINUE →  │                  │ │
│  │  └──────────────┘     └──────────────┘                  │ │
│  │                                                            │ │
│  └──────────────────────────────────────────────────────────┘ │
│                                                                │
│  [Background music continues softly]                           │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

**User Actions:**
- "TAKE A BREAK" → Save state, return to home (can resume later)
- "CONTINUE" → Next question

---

### 4.7 Game Completion / Celebration

**URL/Route:** `/student/play/{game-id}/complete`
**Time:** 20-30 seconds

#### Screen Layout

```
┌────────────────────────────────────────────────────────────────┐
│                                                                │
│     [Full-screen celebration animation]                        │
│     🎉 Confetti, fireworks, victory music 🎉                   │
│                                                                │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │                                                            │ │
│  │  🏆 Mission Complete! 🏆                                  │ │
│  │                                                            │ │
│  │  Fantastic work, Aarav! You successfully navigated       │ │
│  │  through the Number Galaxy and helped Captain Fraction!   │ │
│  │                                                            │ │
│  │  ✨ +200 XP                                               │ │
│  │  🏅 Badge Earned: Fraction Explorer                       │ │
│  │  📈 Math Level: 12 → 13                                   │ │
│  │                                                            │ │
│  │  [Animated badge reveal]                                  │ │
│  │                                                            │ │
│  │  ┌──────────────────────────────────────────┐            │ │
│  │  │     🎮 PLAY ANOTHER GAME                 │            │ │
│  │  └──────────────────────────────────────────┘            │ │
│  │                                                            │ │
│  │  ┌──────────────────────────────────────────┐            │ │
│  │  │     🏠 BACK TO HOME                      │            │ │
│  │  └──────────────────────────────────────────┘            │ │
│  │                                                            │ │
│  └──────────────────────────────────────────────────────────┘ │
│                                                                │
│  [Sound: Victory fanfare, celebration sounds]                 │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

**Key Elements:**
- **Celebration animation:** Confetti, fireworks
- **XP earned:** Visible reward
- **Badge/achievement unlock:** If applicable
- **Level up notification:** If level threshold reached
- **CTA buttons:** Play another game OR return home

**User Actions:**
- "PLAY ANOTHER GAME" → Game Library with recommendations
- "BACK TO HOME" → Home Dashboard (updated with progress)

---

## STEP 5: PAUSE / SAVE STATE

### 5.1 Pause Menu (During Game)

**Triggered by:** Pause button during gameplay
**Time:** As needed

#### Screen Layout

```
┌────────────────────────────────────────────────┐
│                                                │
│     [Dimmed game background]                   │
│                                                │
│  ┌──────────────────────────────────────────┐ │
│  │                                            │ │
│  │          Game Paused ⏸                    │ │
│  │                                            │ │
│  │  Your progress has been saved!            │ │
│  │                                            │ │
│  │  ┌──────────────────────────────────┐    │ │
│  │  │      RESUME GAME →               │    │ │
│  │  └──────────────────────────────────┘    │ │
│  │                                            │ │
│  │  ┌──────────────────────────────────┐    │ │
│  │  │      RESTART GAME                │    │ │
│  │  └──────────────────────────────────┘    │ │
│  │                                            │ │
│  │  ┌──────────────────────────────────┐    │ │
│  │  │      EXIT TO HOME                │    │ │
│  │  └──────────────────────────────────┘    │ │
│  │                                            │ │
│  │  Volume: [████████░░]                     │ │
│  │  Music:  [ON | OFF]                       │ │
│  │                                            │ │
│  └──────────────────────────────────────────┘ │
│                                                │
└────────────────────────────────────────────────┘
```

**User Actions:**
- "RESUME GAME" → Return to question
- "RESTART GAME" → Restart from beginning (confirmation required)
- "EXIT TO HOME" → Save state, return to home dashboard

---

## STEP 6: LOGOUT

### 6.1 Logout from Profile

**Triggered by:** Clicking "Logout" in profile dropdown
**Time:** Immediate

#### Logout Confirmation (Optional)

```
┌────────────────────────────────────────────────┐
│                                                │
│  ┌──────────────────────────────────────────┐ │
│  │                                            │ │
│  │     👋 See you soon, Aarav!               │ │
│  │                                            │ │
│  │     Are you sure you want to log out?     │ │
│  │                                            │ │
│  │  ┌──────────────┐   ┌──────────────┐     │ │
│  │  │   CANCEL     │   │   LOG OUT    │     │ │
│  │  └──────────────┘   └──────────────┘     │ │
│  │                                            │ │
│  └──────────────────────────────────────────┘ │
│                                                │
└────────────────────────────────────────────────┘
```

**After Logout:** → Redirected to Login Screen

---

## V1 Feature Summary (MVP)

### ✅ Included in V1

| Feature | Status | Priority |
| --- | --- | --- |
| **Login/Signup (school-based)** | ✅ V1 | P0 |
| **Avatar selection** | ✅ V1 | P1 |
| **Interactive tutorial** | ✅ V1 | P1 |
| **Home dashboard** | ✅ V1 | P0 |
| **Continue playing** | ✅ V1 | P0 |
| **Recommended games (basic)** | ✅ V1 | P0 |
| **Assigned by teacher** | ✅ V1 | P0 |
| **Game library/browse** | ✅ V1 | P0 |
| **Game preview** | ✅ V1 | P1 |
| **Game play interface** | ✅ V1 | P0 |
| **Story-based questions** | ✅ V1 | P0 |
| **Multiple choice answers** | ✅ V1 | P0 |
| **Immediate feedback** | ✅ V1 | P0 |
| **Hints (optional)** | ✅ V1 | P1 |
| **Pause/save state** | ✅ V1 | P0 |
| **Game completion celebration** | ✅ V1 | P0 |
| **Badges/achievements** | ✅ V1 | P1 |
| **Progress tracking (basic)** | ✅ V1 | P0 |
| **Profile page** | ✅ V1 | P1 |
| **Achievements page** | ✅ V1 | P1 |
| **Logout** | ✅ V1 | P0 |

### ⏭️ Deferred to V1.5+

| Feature | Version | Notes |
| --- | --- | --- |
| **Adaptive difficulty (IRT)** | V1.5 | Basic algorithm in V1, advanced IRT in V1.5 |
| **Friend leaderboard** | V1.5 | Social features deferred |
| **Parent dashboard access** | V1.5 | B2C launch |
| **Freemium tier** | V1.5 | B2C launch |
| **Hindi language** | V1.5 | Month 7+ |
| **Vernacular languages** | V2.0 | Month 13+ |
| **Practice mode** | V2.0 | Advanced feature |
| **AI tutor chatbot** | V2.0+ | Future innovation |

---

## Key User Flow Metrics (V1 Success Criteria)

| Metric | Target |
| --- | --- |
| **Signup completion rate** | 80%+ |
| **Tutorial completion rate** | 70%+ |
| **First game started within 5 min** | 70%+ |
| **First game completion rate** | 70%+ |
| **Avg. time per game session** | 20-25 min |
| **Return within 24 hours** | 60%+ |
| **DAU/MAU ratio** | 25-30% |
| **Games completed per student/month** | 2-3 |
| **Student satisfaction (post-game)** | 85%+ rate as "fun" |

---

## Technical Implementation Notes

### Session Management
- Auto-save every question (prevent data loss)
- Session timeout: 30 minutes of inactivity
- "Resume from where you left off" on login

### Performance Requirements
- Page load time: < 2 seconds
- Game load time: < 5 seconds
- Question transition: < 1 second
- Smooth animations: 60 FPS

### Offline Support (Future)
- V1: Requires internet connection
- V1.5+: Download games for offline play

### Cross-Device Sync
- State synced across web + mobile apps
- Student can start on tablet, continue on phone

---

## Next Steps

1. **Create wireframes** for each screen using `/mockup` skill
2. **Design game storyboards** for 3-5 sample games
3. **Task Frontend Engineer** to build UI components
4. **Task Backend Engineer** to build API endpoints
5. **Task UI/UX Engineer** to design game assets
6. **Task QA Engineer** to create test plans

---

**This is the V1 student journey. Let's build it!** 🚀
