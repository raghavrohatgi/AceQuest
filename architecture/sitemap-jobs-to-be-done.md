# AceQuest Site Map & Jobs-to-be-Done

**Purpose:** Comprehensive map of all user-facing components with their jobs-to-be-done (JTBD)

**Last Updated:** 2026-02-09

---

## Platform Overview

AceQuest has **4 primary user types**, each with their own interface:

1. **Students** (Grades 3-8) → Game App
2. **Teachers** → Teacher Dashboard
3. **Parents** → Parent Dashboard
4. **School Admins** → Admin Portal

**Future:** Government officials → Government Analytics Dashboard (Phase 3)

---

## 1. STUDENT GAME APP

**Primary Users:** Grades 3-8 students (ages 8-14)
**Platform:** Web + iOS App + Android App
**Core Job:** "Help me complete fun games that secretly assess my learning"

### 1.1 Landing / Onboarding

**URL:** `/` or App Launch

**Jobs to be Done:**
- Show me what AceQuest is in language I understand (kid-friendly)
- Let me sign up easily (email, Google SSO, or school code)
- Get me excited about playing games, not taking tests
- Guide me through my first game without overwhelming me

**Key Features:**
- Welcome video (30-60 sec animation explaining AceQuest)
- Account creation (email/password or Google/Apple sign-in)
- School code entry (for B2B students)
- Tutorial/walkthrough for first-time users
- Avatar selection (personalize my character)

**Success Metrics:**
- 80%+ signup completion rate
- 70%+ complete first game within 5 minutes

---

### 1.2 Student Home Dashboard

**URL:** `/student/home` or App Home

**Jobs to be Done:**
- Show me what games I can play right now
- Let me see my progress and achievements
- Make me excited to continue playing
- Help me easily pick up where I left off

**Key Features:**
- **Recommended games** (AI-suggested based on learning gaps)
- **Continue playing** section (resume incomplete games)
- **My achievements** (badges, levels, milestones)
- **Daily streak** tracker (gamification for consistency)
- **Subject selection** (Math, English, Science quick filters)
- **Progress overview** (visual progress bars by subject)
- **Friend leaderboard** (opt-in, privacy-safe social comparison)

**Success Metrics:**
- 60%+ students return within 24 hours
- 3-4 games played per student per month
- 35-40% DAU/MAU ratio

---

### 1.3 Game Library / Browse

**URL:** `/student/games`

**Jobs to be Done:**
- Let me explore all available games
- Help me find games I'll enjoy based on my interests
- Show me which games I've completed vs. not started
- Make it easy to filter by subject, grade, or difficulty

**Key Features:**
- **Grid/card view** of all games (thumbnail, title, duration, subject)
- **Filters:** Subject (Math/English/Science), Grade level, Completion status
- **Sort by:** Newest, Most popular, Recommended for me
- **Search bar** (find games by name or topic)
- **Game preview** (hover to see description and sample screenshot)
- **Favorites/bookmark** games for later

**Success Metrics:**
- 50%+ students browse library at least once per week
- 30%+ games discovered via browse (vs. recommendations)

---

### 1.4 Game Play Interface

**URL:** `/student/play/{game-id}`

**Jobs to be Done:**
- Immerse me in a fun story-based game experience
- Ask me questions that feel like part of the game, not a test
- Give me immediate feedback so I learn as I play
- Track my progress without making me anxious about scores

**Key Features:**

#### Pre-Game Screen
- Game story/context introduction
- Duration estimate (15-25 minutes)
- Competencies being assessed (hidden from student; shown to teacher)
- "Start Game" CTA

#### In-Game Interface
- **Story narrative panel** (text + illustrations/animations)
- **Question embedded in story** (e.g., "Help the astronaut calculate fuel needed")
- **Multiple-choice or interactive answers** (drag-drop, drawing, typing)
- **Immediate feedback:**
  - Correct: Positive reinforcement ("Great thinking!"), story progresses
  - Incorrect: Gentle hint ("Try thinking about it this way..."), option to retry
- **Progress indicator** (visual progress bar, not "Question 5 of 20")
- **Pause/resume** functionality
- **Background music & sound effects** (age-appropriate, optional mute)
- **No visible score** during game (students don't see % correct)

#### Post-Game Screen
- **Completion celebration** (animation, confetti, "You did it!")
- **Badges/rewards earned** (e.g., "Math Explorer Badge")
- **Progress unlocked** (next game in series)
- **Encouraging message** (e.g., "You're getting stronger at fractions!")
- **"Play another game" CTA**

**Success Metrics:**
- 70%+ game completion rate (students finish games they start)
- 85%+ students rate game as "fun" or "very fun" (post-game survey)
- 30-40% reduction in test anxiety vs. traditional assessments

---

### 1.5 My Progress / Profile

**URL:** `/student/profile`

**Jobs to be Done:**
- Show me what I've achieved (badges, levels, completed games)
- Let me see my strengths in a positive way
- Help me understand what to work on next (without making me feel bad)
- Let me customize my profile (avatar, username)

**Key Features:**
- **Profile header:** Avatar, username, grade level, total games completed
- **Achievement wall:** All badges and trophies earned
- **Level/XP system:** Gamified progression (e.g., "Level 12 Math Wizard")
- **Completed games list** (with replay option)
- **Subjects overview:** Visual strengths in Math, English, Science (friendly language)
- **Daily streak calendar** (days active in last 30 days)
- **Settings:** Change avatar, notification preferences, logout

**Success Metrics:**
- 60%+ students check their profile at least once per week
- 40%+ students replay games to improve

---

### 1.6 Adaptive Practice Mode (Future - V2)

**URL:** `/student/practice`

**Jobs to be Done:**
- Let me practice specific topics I'm struggling with
- Give me questions at the right difficulty level for me
- Make practice feel like a game, not homework
- Help me improve without feeling judged

**Key Features:**
- AI-generated practice questions based on learning gaps
- Adaptive difficulty (IRT-based)
- Quick 5-10 minute practice sessions
- Immediate feedback and hints
- Progress tracking ("You've improved 20% in fractions this week!")

---

## 2. TEACHER DASHBOARD

**Primary Users:** Classroom teachers (Grades 3-8)
**Platform:** Web (desktop/tablet optimized)
**Core Job:** "Help me understand each student's learning gaps so I can personalize instruction efficiently"

### 2.1 Teacher Login / Onboarding

**URL:** `/teacher/login`, `/teacher/onboarding`

**Jobs to be Done:**
- Let me sign in securely with my school credentials
- Guide me through dashboard setup if I'm new
- Show me how to assign games and view results quickly

**Key Features:**
- Secure login (email/password + optional SSO with school LMS)
- First-time setup wizard:
  - Import student roster (CSV upload or manual entry)
  - Organize students into classes/sections
  - Set grade level and subjects
- Dashboard tutorial (interactive walkthrough)

**Success Metrics:**
- 90%+ teachers complete onboarding within 10 minutes
- 80%+ teachers assign first game within 24 hours of onboarding

---

### 2.2 Teacher Home Dashboard

**URL:** `/teacher/dashboard`

**Jobs to be Done:**
- Give me an at-a-glance view of how my classes are doing
- Alert me to students who need immediate attention
- Show me recent assessment results without overwhelming me
- Help me quickly assign games or view reports

**Key Features:**
- **Overview cards:**
  - Total students, active this week, average completion rate
  - Recent assessments (games assigned in last 7 days)
  - Alerts (students falling behind, low engagement)
- **Class performance heatmap** (competencies across all students)
- **Recent activity feed** (which students completed which games)
- **Quick actions:**
  - Assign new game
  - View class report
  - Message students/parents (future)
- **Upcoming assessments** (scheduled games)

**Success Metrics:**
- 85%+ teachers use dashboard weekly
- 70%+ teachers take action on alerts within 48 hours

---

### 2.3 My Classes / Student Roster

**URL:** `/teacher/classes`

**Jobs to be Done:**
- Let me see all my classes and students organized clearly
- Make it easy to manage multiple classes (if I teach several sections)
- Let me add/remove students or update information
- Show me each class's overall performance snapshot

**Key Features:**
- **Class list view** (all classes I teach)
- **Student roster per class:**
  - Name, grade, enrollment date
  - Last active date
  - Completion rate (% of assigned games completed)
  - Performance indicator (green/yellow/red for on-track/needs-help/struggling)
- **Bulk actions:** Assign game to entire class, export roster
- **Add/edit/remove students**
- **Class settings:** Grade level, subject focus, notification preferences

**Success Metrics:**
- 95%+ teacher accuracy in roster management
- 80%+ teachers organize students into classes within first week

---

### 2.4 Individual Student Profile

**URL:** `/teacher/students/{student-id}`

**Jobs to be Done:**
- Show me everything about one student's learning journey
- Help me identify specific competencies this student struggles with
- Give me actionable recommendations for interventions
- Let me track this student's progress over time

**Key Features:**
- **Student header:** Name, photo, grade, parent contact (if available)
- **Overall performance summary:**
  - Games completed, completion rate, last active
  - Strengths (top 3 competencies)
  - Growth areas (top 3 competencies needing work)
- **Competency breakdown by subject:**
  - Math: Number sense (85%), Geometry (60%), Fractions (45%)
  - English: Reading comprehension (75%), Grammar (80%), Vocabulary (55%)
  - Science: Life science (70%), Physical science (60%), Inquiry skills (80%)
  - Visual: Color-coded bars or radar chart
- **Learning gap analysis:**
  - Specific topics/competencies flagged as needing intervention
  - AI-suggested resources or activities to address gaps
- **Game history:** All completed games with scores and timestamps
- **Progress over time:** Line graph showing competency improvement (pre/post comparison)
- **Notes section:** Teacher can add private observations
- **Export report:** PDF for parent-teacher meetings

**Success Metrics:**
- 80%+ teachers view individual profiles before parent meetings
- 60%+ teachers use intervention suggestions

---

### 2.5 Competency Heatmap (Class-Wide)

**URL:** `/teacher/competencies`

**Jobs to be Done:**
- Show me which competencies my entire class has mastered vs. struggles with
- Help me identify patterns (whole-class issues vs. individual gaps)
- Guide my lesson planning by highlighting what to reteach
- Make it visual and quick to scan (I'm busy!)

**Key Features:**
- **Heatmap grid:**
  - Rows: Competencies (e.g., "Fractions - Addition/Subtraction")
  - Columns: Students (names or initials)
  - Cells: Color-coded (green = mastered, yellow = developing, red = needs help)
- **Filter by subject** (Math, English, Science)
- **Sort by:** Competency mastery (weakest first), student name
- **Click cell:** Drill down to see specific questions student answered incorrectly
- **Export heatmap** (PDF or image for sharing with school admin)

**Success Metrics:**
- 70%+ teachers use heatmap for lesson planning weekly
- 50%+ teachers report it saves 2-3 hours/week in planning

---

### 2.6 Assessment Library / Assign Games

**URL:** `/teacher/assessments`

**Jobs to be Done:**
- Let me browse all available games by subject, grade, competency
- Help me assign the right game to the right students (or whole class)
- Make assignment quick (I don't want to spend 20 minutes on this)
- Let me schedule games in advance or assign immediately

**Key Features:**
- **Game library grid:**
  - Thumbnail, title, subject, grade level, duration, competencies assessed
- **Filters:** Subject, Grade, Competency, Duration (5-10 min, 10-20 min, 20-30 min)
- **Search bar:** Find games by topic or keyword
- **Game preview:** View sample questions, story narrative, competency mapping
- **Assign game:**
  - Select students (individual, group, or whole class)
  - Set due date (optional)
  - Add instructions/notes for students (optional)
  - Schedule for later or assign now
- **Assignment history:** See which games I've assigned and when

**Success Metrics:**
- 90%+ teachers assign at least 1 game per week
- 80%+ teachers use filters to find appropriate games

---

### 2.7 Reports & Analytics

**URL:** `/teacher/reports`

**Jobs to be Done:**
- Generate reports for parent-teacher meetings, school admin, or my own records
- Compare class performance over time (growth tracking)
- Export data in formats I can use (PDF, Excel)
- Understand which interventions are working

**Key Features:**
- **Report types:**
  - Class summary report (overall performance by subject)
  - Individual student report (competency breakdown + recommendations)
  - Growth report (pre/post assessment comparison)
  - NEP 2020 compliance report (mapping to CBSE/ICSE frameworks)
- **Date range selector** (last week, last month, last term, custom)
- **Export options:** PDF, Excel, print-friendly
- **Analytics dashboard:**
  - Average completion rate over time (line graph)
  - Competency mastery distribution (bar chart)
  - Student engagement trends (DAU/MAU by week)
- **Comparison view:** Compare performance across classes (if I teach multiple)

**Success Metrics:**
- 70%+ teachers generate at least 1 report per month
- 60%+ teachers use growth reports for parent meetings

---

### 2.8 Settings & Support

**URL:** `/teacher/settings`

**Jobs to be Done:**
- Let me customize notification preferences (don't spam me!)
- Manage my profile and account settings
- Get help if I'm stuck or have questions
- Provide feedback on the platform

**Key Features:**
- **Profile settings:** Name, email, phone, school affiliation
- **Notification settings:**
  - Email alerts for completed assignments, low engagement, new features
  - Frequency (real-time, daily digest, weekly summary)
- **Class settings:** Manage rosters, grade levels, subject preferences
- **Help & Support:**
  - FAQ / Knowledge base
  - Video tutorials
  - Live chat support (during school hours)
  - Submit bug report or feature request
- **Privacy & security:** Change password, two-factor authentication
- **Logout**

---

## 3. PARENT DASHBOARD

**Primary Users:** Parents of Grades 3-8 students
**Platform:** Web + Mobile App (iOS/Android)
**Core Job:** "Help me understand my child's learning progress and how to support them at home"

### 3.1 Parent Login / Onboarding

**URL:** `/parent/login`, `/parent/signup`

**Jobs to be Done:**
- Let me sign up easily (email or Google/Apple)
- Connect my account to my child's student account
- Guide me through the dashboard so I know what I'm looking at
- Explain how AceQuest works in parent-friendly language

**Key Features:**
- Sign up/login (email/password or SSO)
- Child account linking:
  - Option 1: Enter child's student ID (provided by school)
  - Option 2: Enter child's email (if B2C user)
  - Option 3: Scan QR code from child's app
- Onboarding tutorial (video + interactive walkthrough)
- Freemium tier explanation (free vs. premium features)

**Success Metrics:**
- 85%+ parents complete signup within 5 minutes
- 90%+ successfully link to child's account on first attempt

---

### 3.2 Parent Home Dashboard

**URL:** `/parent/home`

**Jobs to be Done:**
- Show me how my child is doing at a glance
- Alert me if my child needs help or isn't engaging
- Make me feel informed without overwhelming me with data
- Encourage me to engage with my child's learning

**Key Features:**
- **Child overview card:**
  - Name, grade, photo (avatar)
  - Games played this week
  - Current streak (consecutive days active)
  - Overall progress indicator (green/yellow/red)
- **Recent activity feed:**
  - "Aarav completed 'Space Fractions' and earned a badge!"
  - "Priya improved 20% in reading comprehension this month!"
- **Strengths & growth areas:**
  - Top 3 strengths (plain language, e.g., "Great at multiplication!")
  - Top 3 areas for support (e.g., "Could use help with fractions")
- **Recommended actions:**
  - "Play a fractions game together this weekend"
  - "Ask Aarav about his Space Explorer badge!"
- **Quick links:** View detailed report, encourage child, manage subscription

**Success Metrics:**
- 60%+ parents check dashboard weekly
- 40%+ parents take at least 1 recommended action per month

---

### 3.3 Child Progress Report (Detailed)

**URL:** `/parent/progress/{child-id}`

**Jobs to be Done:**
- Show me detailed insights into my child's competencies
- Help me understand what each competency means (no jargon!)
- Show me growth over time so I can celebrate progress
- Give me specific, actionable ways to help at home

**Key Features:**
- **Competency breakdown by subject:**
  - Math: Visual bars showing mastery level (Fractions: 65%, Geometry: 80%)
  - English: Reading comprehension, Grammar, Vocabulary, Writing
  - Science: Life science, Physical science, Inquiry skills
  - **Plain language explanations:** Hover/tap for "What is this?" tooltips
- **Progress over time:**
  - Line graph showing competency improvement (last 3 months)
  - Milestone markers (e.g., "Mastered multiplication tables!")
- **Learning gap insights:**
  - "Your child is doing well in most areas, but fractions need more practice"
  - AI-generated summary in parent-friendly language
- **Recommended activities:**
  - "Try these at-home activities to help with fractions: [list of 3-5 activities]"
  - Links to free online resources or printable worksheets
- **Comparison (opt-in):**
  - "Your child is performing above grade level in 2 out of 3 subjects"
  - Benchmark against anonymized grade-level averages
- **Export report:** PDF for record-keeping or sharing with tutor

**Success Metrics:**
- 70%+ parents view detailed report at least once per month
- 50%+ parents report feeling confident understanding child's progress (survey)

---

### 3.4 Activity Recommendations

**URL:** `/parent/activities`

**Jobs to be Done:**
- Give me specific things I can do with my child to support their learning
- Make recommendations easy to understand and implement (I'm not a teacher!)
- Tie activities to my child's specific learning gaps
- Make it fun, not feel like homework

**Key Features:**
- **Personalized activity feed:**
  - Activities tailored to child's learning gaps (AI-generated)
  - Each activity card includes:
    - Title (e.g., "Fraction Pizza Party")
    - Duration (10-15 minutes)
    - Materials needed (minimal, household items)
    - Step-by-step instructions
    - Which competency it helps with
- **Filter by:** Subject, Duration, Materials available
- **Mark as completed:** Track which activities you've done
- **Rate activities:** Thumbs up/down to improve recommendations
- **Share activities:** Email or WhatsApp to spouse/family member

**Success Metrics:**
- 40%+ parents try at least 1 activity per month
- 70%+ parents rate activities as helpful (4+ stars)

---

### 3.5 Subscription & Settings

**URL:** `/parent/subscription`, `/parent/settings`

**Jobs to be Done:**
- Let me upgrade to premium if I want more features
- Manage my subscription and billing easily
- Customize notification preferences
- Add/remove children from my account

**Key Features:**

#### Subscription Management
- **Current plan:** Free vs. Premium (Monthly/Annual)
- **Upgrade CTA:** Show premium benefits (unlimited games, detailed reports, priority support)
- **Billing history:** View past invoices
- **Payment method:** Update credit card
- **Cancel subscription** (with retention offer)

#### Settings
- **Profile:** Name, email, phone
- **Children:** Add/remove children, update grade levels
- **Notifications:**
  - Weekly summary email (on/off)
  - Push notifications for milestones (on/off)
  - Language preference (English, Hindi, Tamil, Telugu, Marathi)
- **Privacy settings:** Data sharing preferences
- **Help & Support:** FAQ, contact support, provide feedback
- **Logout**

**Success Metrics:**
- 10-15% free-to-premium conversion rate (by Month 12)
- 80%+ premium subscriber retention after 3 months

---

### 3.6 Celebration & Encouragement

**URL:** `/parent/celebrate`

**Jobs to be Done:**
- Help me celebrate my child's achievements in a meaningful way
- Give me templates for encouragement messages
- Make it easy to share milestones with family (grandparents, etc.)

**Key Features:**
- **Achievement feed:** All badges, milestones, and wins
- **Celebration templates:**
  - "Congrats on mastering multiplication! Let's celebrate with ice cream!"
  - Pre-written messages to send to child within app
- **Share milestones:** Generate shareable image (social media or WhatsApp)
- **Encouragement prompts:** "Your child hasn't played in 3 days. Send them a nudge?"

**Success Metrics:**
- 50%+ parents send at least 1 encouragement message per month
- 30%+ parents share milestones externally

---

## 4. SCHOOL ADMIN PORTAL

**Primary Users:** School principals, vice principals, IT coordinators
**Platform:** Web (desktop optimized)
**Core Job:** "Help me manage hundreds of students and teachers efficiently, and prove ROI to school leadership"

### 4.1 Admin Login & Onboarding

**URL:** `/admin/login`, `/admin/onboarding`

**Jobs to be Done:**
- Secure login for school administrators
- Set up school-wide account (import roster, assign teachers)
- Configure school settings (grade levels, subjects, billing)

**Key Features:**
- Admin login (email/password, 2FA recommended)
- School setup wizard:
  - School profile (name, location, board affiliation)
  - Bulk import students and teachers (CSV upload)
  - Assign teachers to classes
  - Configure subjects and grade levels (Grades 3-8)
- Billing setup (enter payment details, select plan)

**Success Metrics:**
- 95%+ schools complete setup within 30 minutes
- 90%+ successful roster imports on first attempt

---

### 4.2 Admin Dashboard

**URL:** `/admin/dashboard`

**Jobs to be Done:**
- Give me a bird's-eye view of school-wide usage and performance
- Show me which teachers and classes are engaging vs. not
- Alert me to issues (low usage, technical problems)
- Prove ROI with data I can show leadership

**Key Features:**
- **Overview cards:**
  - Total students enrolled, active this week, completion rate
  - Total teachers, active teachers (% using dashboard weekly)
  - Games completed this month, avg. games per student
- **Usage trends:** Line graph of daily/weekly active users (students + teachers)
- **Performance summary:**
  - School-wide competency heatmap (aggregated across all classes)
  - Top-performing subjects vs. subjects needing support
- **Teacher engagement:** List of teachers with usage stats (% students assigned games)
- **Alerts:**
  - Low teacher adoption (< 50% teachers using platform)
  - Low student engagement (< 30% active weekly)
  - Billing issues (payment failed, subscription expiring)
- **Quick actions:** Add teacher/student, view reports, manage billing

**Success Metrics:**
- 80%+ admins check dashboard monthly
- 70%+ admins use data for school leadership meetings

---

### 4.3 Student & Teacher Management

**URL:** `/admin/users`

**Jobs to be Done:**
- Let me add, edit, or remove students and teachers easily
- Manage class assignments (which teacher teaches which class)
- Bulk operations for efficiency (I manage hundreds of users)

**Key Features:**
- **User list view:**
  - Tabs: Students, Teachers
  - Search and filter (by grade, class, active status)
- **Bulk actions:**
  - Add multiple users via CSV upload
  - Assign multiple students to a teacher
  - Deactivate users at end of academic year
- **Individual user management:**
  - Edit user details (name, email, grade, class)
  - Reset password
  - View user activity log
  - Delete user (with confirmation)
- **Class management:**
  - Create/edit/delete classes
  - Assign teachers to classes
  - Assign students to classes

**Success Metrics:**
- 90%+ user management tasks completed in < 5 minutes
- 95%+ accurate roster management

---

### 4.4 School-Wide Reports & Analytics

**URL:** `/admin/reports`

**Jobs to be Done:**
- Generate reports for school board, parent meetings, or accreditation
- Track ROI (are we getting value from this investment?)
- Compare performance across grades and classes
- Export data for external analysis

**Key Features:**
- **Report types:**
  - School-wide performance summary (all subjects, all grades)
  - Grade-level comparison (how is Grade 5 doing vs. Grade 6?)
  - Class-level comparison (which classes are excelling?)
  - Teacher engagement report (which teachers are using platform effectively?)
  - NEP 2020 compliance report (alignment with CBSE/ICSE frameworks)
- **ROI metrics:**
  - Teacher time saved (hrs/week)
  - Student engagement improvement (% increase in participation)
  - Learning outcomes improvement (pre/post assessment comparison)
- **Export options:** PDF, Excel, print-friendly
- **Scheduled reports:** Auto-send monthly summary to school leadership

**Success Metrics:**
- 70%+ admins generate at least 1 report per quarter
- 80%+ report platform value to school leadership based on data

---

### 4.5 Billing & Subscription

**URL:** `/admin/billing`

**Jobs to be Done:**
- View current subscription and usage
- Manage payment methods
- Download invoices for accounting
- Renew or upgrade subscription

**Key Features:**
- **Subscription overview:**
  - Current plan (Small/Medium/Large school tier)
  - Price, billing cycle (annual/quarterly)
  - Students included, additional student pricing
  - Next billing date
- **Usage tracking:** Current student count, license utilization
- **Payment methods:** Add/edit credit card or bank transfer details
- **Billing history:** Download past invoices (PDF)
- **Upgrade/downgrade:** Change plan tier
- **Renewal:** Auto-renewal settings, manual renewal option

**Success Metrics:**
- 95%+ on-time payment rate
- 85%+ schools renew after first year

---

### 4.6 Settings & Support

**URL:** `/admin/settings`

**Jobs to be Done:**
- Configure school-wide settings (grade levels, subjects, privacy)
- Get support when needed (technical issues, training requests)
- Manage admin users (if multiple admins at school)

**Key Features:**
- **School settings:**
  - School profile (name, logo, address, board affiliation)
  - Grade levels and subjects offered
  - Academic calendar (term dates for reporting)
  - Privacy settings (parent access, data sharing)
- **Admin users:** Add/remove additional school admins, set permissions
- **Integrations:** Connect to school LMS/SIS (Google Classroom, Teachmint, etc.)
- **Help & Support:**
  - Knowledge base, video tutorials
  - Request teacher training session
  - Live chat or email support
  - Submit bug report or feature request
- **Logout**

---

## 5. MARKETING & PUBLIC WEBSITE

**Primary Users:** Prospective schools, parents, teachers (not yet users)
**Platform:** Web (public-facing, SEO-optimized)
**Core Job:** "Convince me that AceQuest is worth trying for my school/child"

### 5.1 Homepage

**URL:** `/` (public)

**Jobs to be Done:**
- Immediately communicate what AceQuest is and why it's different
- Build trust (testimonials, validation, social proof)
- Drive conversions (sign up for free pilot, start B2C trial)
- Segment users (B2B vs. B2C) and direct them appropriately

**Key Features:**
- **Hero section:**
  - Headline: "Assessment Without Anxiety: Games That Diagnose Learning"
  - Subheadline: "IIT-validated, NEP 2020-aligned, 60-80% cheaper than incumbents"
  - Video demo (60-90 sec showing student playing game)
  - Dual CTAs: "Book a Demo (Schools)" | "Start Free Trial (Parents)"
- **Social proof:**
  - "Used by 10,000+ students across 50+ schools"
  - Logos of pilot schools
  - IIT validation badge
- **How it works (3-step visual):**
  - Step 1: Students play engaging story-based games
  - Step 2: AI analyzes responses and maps competencies
  - Step 3: Teachers/parents get actionable diagnostic reports
- **Key benefits:**
  - "30-40% reduction in test anxiety"
  - "15-20% improvement in learning outcomes"
  - "2-3 hours/week saved for teachers"
- **Testimonials:** Video or text from teachers, parents, students
- **Pricing transparency:** "Starting at ₹2 lakh/year for schools, ₹149/month for parents"
- **Trust indicators:** "IIT-validated | NCERT-aligned | DPDP Act compliant"
- **Footer:** Links to all other pages

**Success Metrics:**
- 50%+ visitors watch at least 30 sec of demo video
- 5-10% conversion to demo request (B2B) or trial signup (B2C)

---

### 5.2 For Schools Page

**URL:** `/for-schools`

**Jobs to be Done:**
- Convince school decision-makers that AceQuest solves their NEP 2020 assessment challenge
- Address objections (cost, implementation, psychometric credibility)
- Drive demo requests

**Key Features:**
- **Problem statement:** "NEP 2020 mandates competency assessment, but tools cost ₹4-5L/year"
- **Solution:** "AceQuest delivers IIT-validated assessment at ₹2-3L/year"
- **Key benefits for schools:**
  - NEP 2020 compliance made easy
  - Affordable (60-80% cheaper)
  - Teacher time savings (2-3 hrs/week)
  - Psychometric credibility (IIT-validated)
- **Case studies:** 2-3 pilot schools with before/after data
- **Pricing:** Transparent tier pricing (Small/Medium/Large schools)
- **Free pilot:** "Try free for 3-6 months, no credit card required"
- **CTA:** "Book a Demo" form

**Success Metrics:**
- 20-30% of school visitors request demo
- 50-60% of demos convert to pilot

---

### 5.3 For Parents Page

**URL:** `/for-parents`

**Jobs to be Done:**
- Convince parents that AceQuest helps them understand their child's learning gaps affordably
- Differentiate from BYJU's (not overwhelming, assessment-focused)
- Drive free trial signups

**Key Features:**
- **Problem statement:** "You want to help your child, but tutoring costs ₹2,000-5,000/month and you still don't know specific learning gaps"
- **Solution:** "AceQuest gives you psychometric-quality diagnostics for ₹149/month (or try free)"
- **Key benefits for parents:**
  - Identify learning gaps without expensive tutoring
  - Child enjoys it (games, not tests)
  - Plain-language reports you can understand
  - Affordable (90-95% cheaper than tutoring)
- **Testimonials:** Video from 2-3 parents showing before/after
- **Pricing:** Free tier (2-3 games/month) vs. Premium (₹149/month)
- **CTA:** "Start Free Trial" (no credit card for free tier)

**Success Metrics:**
- 15-20% of parent visitors sign up for free trial
- 10-15% free trial users convert to paid within 30 days

---

### 5.4 Pricing Page

**URL:** `/pricing`

**Jobs to be Done:**
- Show transparent pricing for B2B and B2C
- Address FAQs (what's included, discounts, payment terms)
- Drive conversions

**Key Features:**
- **B2B pricing table:** Small/Medium/Large school tiers with annual pricing
- **B2C pricing table:** Free, Premium Monthly, Premium Annual
- **Comparison matrix:** What's included in each tier
- **FAQs:** Payment terms, multi-year discounts, refund policy
- **CTAs:** "Book Demo" (B2B), "Start Free Trial" (B2C)

---

### 5.5 About Us Page

**URL:** `/about`

**Jobs to be Done:**
- Build trust (who's behind AceQuest?)
- Communicate mission and values
- Show expertise (team background, IIT partnership)

**Key Features:**
- **Mission statement:** From Mission.md
- **Founder story:** Why you started AceQuest
- **Team:** Photos and bios (if team grows)
- **IIT partnership:** Validation methodology
- **Press mentions:** Articles, awards, recognition

---

### 5.6 Blog / Resources

**URL:** `/blog`, `/resources`

**Jobs to be Done:**
- Educate prospects about NEP 2020, competency assessment, test anxiety
- Drive organic SEO traffic
- Position AceQuest as thought leader

**Key Features:**
- **Blog posts:** (examples)
  - "Understanding NEP 2020's Competency-Based Assessment Mandate"
  - "5 Ways to Reduce Test Anxiety in Your Child"
  - "How Game-Based Assessment Works: A Parent's Guide"
- **Resources:**
  - Free downloadable guides (e.g., "Parent's Guide to NEP 2020")
  - Sample assessment reports
  - FAQs

**Success Metrics:**
- 30-40% of organic traffic comes from blog
- 5-10% blog readers convert to trial/demo

---

### 5.7 Contact / Support

**URL:** `/contact`, `/support`

**Jobs to be Done:**
- Let prospects and users reach out easily
- Provide self-service support (FAQs, help docs)
- Build trust (responsive support team)

**Key Features:**
- **Contact form:** Name, email, message, inquiry type (demo, support, partnership)
- **Live chat widget:** (during business hours)
- **Support portal:** FAQ, help docs, video tutorials
- **Email:** support@acequest.in
- **Phone:** +91-XXXX-XXXXXX (optional)

---

## 6. GOVERNMENT ANALYTICS DASHBOARD (Future - Phase 3)

**Primary Users:** State education department officials, district education officers
**Platform:** Web (highly secure, government-grade)
**Core Job:** "Help me understand competency trends across thousands of schools to inform policy"

### 6.1 Government Login & Dashboard

**URL:** `/government/login`, `/government/dashboard`

**Jobs to be Done:**
- Secure access for government officials (SSO with government systems)
- Show district/state-level aggregated competency data
- Identify systemic gaps (which districts are struggling?)
- Track NEP 2020 implementation progress

**Key Features:**
- **Geographic heatmap:** Districts color-coded by average competency mastery
- **Subject-wise trends:** Math, English, Science performance across state
- **Grade-level analysis:** Which grades are excelling vs. struggling?
- **School comparison:** Rank schools/districts by performance
- **Intervention recommendations:** AI-suggested policy actions
- **Export reports:** For government leadership, public reporting

**Success Metrics:**
- 80%+ government users access dashboard monthly
- 50%+ report using data for policy decisions

---

## 7. ADMIN / INTERNAL TOOLS (Backend)

**Primary Users:** AceQuest internal team (Product, Engineering, Customer Success)
**Platform:** Web (internal, highly secure)
**Core Job:** "Manage platform operations, monitor health, support users"

### 7.1 Internal Admin Dashboard

**URL:** `/internal/admin` (restricted access)

**Jobs to be Done:**
- Monitor platform health (uptime, performance, errors)
- Manage users (support tickets, account issues)
- View business metrics (MRR, churn, conversions)
- Manage content (add/edit games, approve user-generated content)

**Key Features:**
- **Platform health:** Uptime, API latency, error rates
- **User management:** Search any user, view activity, reset accounts
- **Content management:** Add/edit/delete games, upload new assessments
- **Business metrics dashboard:** MRR, ARR, churn, CAC, LTV
- **Support tickets:** Queue of open support requests
- **Feature flags:** Enable/disable features for testing

---

## Site Map Summary

| User Type | # of Main Pages | Primary Platform | Core JTBD |
| --- | --- | --- | --- |
| **Students** | 6 | Web + Mobile App | Play fun games that secretly assess me |
| **Teachers** | 8 | Web (Desktop) | Understand student gaps, personalize instruction |
| **Parents** | 6 | Web + Mobile App | Understand my child's progress, support at home |
| **School Admins** | 6 | Web (Desktop) | Manage school-wide usage, prove ROI |
| **Public / Prospects** | 7 | Public Website | Learn about AceQuest, sign up for trial/demo |
| **Government** | 2 | Web (Secure) | Monitor state-wide competency trends (Phase 3) |
| **Internal Team** | 1 | Web (Internal) | Manage operations, support users |

**Total Pages/Screens Mapped:** ~36 major pages across 7 user types

---

## Next Steps

1. **Prioritize for MVP (Months 1-6):**
  - Student Game App (core 5 pages)
  - Teacher Dashboard (core 6 pages)
  - School Admin Portal (core 4 pages)
  - Public Website (homepage + for-schools + pricing)

2. **Phase 2 (Months 7-12):**
  - Parent Dashboard (all 6 pages)
  - Expanded public website (for-parents, blog, resources)

3. **Phase 3 (Months 13-18+):**
  - Government Dashboard
  - Advanced features (adaptive practice, marketplace, integrations)

4. **Create detailed wireframes** for each prioritized page using `/mockup` skill

5. **Task AI agents** to begin development based on this site map

---

**This site map is the blueprint. Let's build it.** 🚀
