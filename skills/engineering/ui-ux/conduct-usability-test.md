# Skill: Conduct Usability Test

## Purpose
Define a structured procedure for conducting usability tests with K-8 students and their parents/teachers for AceQuest features. Usability tests uncover friction points, confusing UI patterns, and delight opportunities that analytics and automated testing cannot detect. Results directly inform design iterations.

## Used By
- UI/UX Designer Agent
- Product Agent
- QA Agent

## Inputs
| Field | Type | Description |
|-------|------|-------------|
| `featureUnderTest` | string | Feature being tested, e.g. "Quiz Game Board" |
| `participants` | object[] | Age, grade, device type, prior experience |
| `researchQuestions` | string[] | Questions the test aims to answer |
| `taskScenarios` | string[] | Task prompts given to participants |
| `successMetrics` | object[] | How success is measured per task |
| `moderationStyle` | `"think-aloud" \| "retrospective" \| "unmoderated"` | Protocol |

## Procedure / Template

### Step 1 — Define Research Questions

Frame 3–5 specific questions the test must answer. Avoid "Is this good?" — be specific.

Example research questions for the Quiz Game Board:
1. Can a Grade 3 student (age 8) independently find and start a quiz without adult help?
2. Do students understand the progress bar shows how many questions are left?
3. Do students know they can skip a question and come back to it?
4. Does the timer create anxiety that causes students to rush without reading?
5. Is the badge unlock animation understood as a reward, or is it confusing?

### Step 2 — Recruit Participants

| Segment | Count | Criteria |
|---------|-------|----------|
| Grade 1–2 students (age 6–8) | 3 | First-time AceQuest users, low reading level |
| Grade 4–5 students (age 9–11) | 3 | Existing users, moderate digital literacy |
| Grade 7–8 students (age 12–14) | 2 | Power users, high digital literacy |
| Parents of Grade 1–3 | 2 | Understand parent supervision flows |
| Teachers | 1 | To evaluate teacher-facing features |

**Minimum viable test:** 5 participants per segment surface ~80% of usability issues.

### Step 3 — Prepare Test Environment

```
Device setup:
- Android: Pixel 6a (representative mid-range Indian device)
- iOS: iPhone SE 3rd gen (representative budget iPhone)
- Desktop: 1366 × 768 laptop (common school computer resolution)

Prototyping:
- For new features: Figma prototype (interactive, no real data)
- For existing features: Staging environment with seeded test accounts

Test accounts:
- student.usability.g3@acequest.in / TestPass@123 (Grade 3)
- student.usability.g5@acequest.in / TestPass@123 (Grade 5)

Recording:
- Screen recording enabled (Lookback.io or Maze)
- Audio recording for think-aloud
- Moderator observes; second observer takes notes
```

### Step 4 — Task Scenarios

Write tasks as realistic goals, not instructions. Never tell participants what to click.

```
Task Script for Grade 5 Quiz Flow

"Imagine you just got home from school and you want to practice Mathematics 
on AceQuest. Your teacher said there are some new quizzes available. 
Can you find a maths quiz and answer all the questions?"

[Moderator: Do not guide — only clarify if participant is completely stuck after 2 minutes]

Success criteria:
✓ Navigates to a Mathematics quiz without prompting
✓ Answers at least 3 questions
✓ Understands how to submit or move to next question

---

Task 2: "Pretend you accidentally tapped the wrong answer. 
Can you change your answer before moving on?"

Success criteria:
✓ Discovers they can tap a different option before pressing Next
✓ Completes the change within 30 seconds
```

### Step 5 — Observation Framework (PURE Method)

Score each task:

| Score | Label | Observation |
|-------|-------|-------------|
| 0 | Fail | Could not complete task even with assistance |
| 1 | Pass with help | Completed after moderator prompt or assistance |
| 2 | Pass with hesitation | Completed independently but with visible confusion |
| 3 | Pass clean | Completed smoothly without hesitation |

Record for each participant + task:
- Time on task (seconds)
- Error count (wrong clicks/taps before finding correct action)
- Verbal comments (direct quotes during think-aloud)
- Emotional indicators (smiles, frustration, excitement)

### Step 6 — Moderation Guide

```
Before session:
"There are no right or wrong answers — we're testing the app, not you. 
Please say out loud what you're thinking as you go."
[For young children: "It's like talking to yourself while you play a game."]

During session:
- Do not say "correct", "good job", or "wrong" — stay neutral
- If participant is silent: "What are you thinking right now?"
- If stuck for > 2 min: "What would you expect to happen if you tapped/clicked here?"
- Never point, gesture, or look at the area the participant should interact with

After each task:
- "How would you rate that on a scale of 1-5? 1 = very hard, 5 = very easy."
- "Was anything surprising?"

After all tasks (5-minute debrief):
- "What did you like most?"
- "What was most confusing?"
- "If you could change one thing, what would it be?"
```

### Step 7 — Single Ease Question (SEQ) Scoring

After each task, ask: "How difficult was this task?" (1 = Very Difficult, 7 = Very Easy)

Target SEQ score for AceQuest tasks: >= 6.0 (age-appropriate for K-8)

### Step 8 — Analyse Results

```python
# usability_analysis.py
import statistics

results = {
    "start_quiz": {
        "grades_3": [3, 2, 3, 3, 2],    # PURE scores per participant
        "grades_5": [3, 3, 3, 3, 3],
        "seq_grades_3": [5, 6, 7, 6, 5],  # SEQ scores (1-7)
        "time_seconds": [45, 120, 38, 52, 90],
    },
    "change_answer": {
        "grades_3": [1, 0, 2, 1, 0],
        "seq_grades_3": [3, 2, 4, 3, 2],
        "time_seconds": [180, 240, 90, 200, 300],
    },
}

for task, data in results.items():
    pure_mean = statistics.mean(data["grades_3"])
    seq_mean = statistics.mean(data["seq_grades_3"])
    avg_time = statistics.mean(data["time_seconds"])
    fail_rate = data["grades_3"].count(0) / len(data["grades_3"]) * 100
    print(f"Task: {task}")
    print(f"  PURE Mean: {pure_mean:.1f}/3   SEQ: {seq_mean:.1f}/7   Avg Time: {avg_time:.0f}s   Fail Rate: {fail_rate:.0f}%")
```

### Step 9 — Report Template

```markdown
# Usability Test Report: Quiz Game Board
**Date:** 2025-06-01  |  **Participants:** 9  |  **Sessions:** 45 min each

## Key Findings

### Critical Issues (Fix before launch)
1. **Change answer not discoverable** — Grade 3 fail rate 40%
   - 3/5 Grade 3 participants could not change their answer
   - "I thought I was stuck with my first tap" — Aarav, Grade 3
   - **Recommendation:** Add a "Change answer" affordance or undo animation

### Major Issues (Fix in next sprint)
2. **Timer causes anxiety** — 4/9 participants rushed and skipped reading
   - "It kept going so fast I just pressed anything" — Priya, Grade 4
   - **Recommendation:** Give option to hide timer; add warning at 30s, not constant countdown

### Minor Issues (Backlog)
3. **Progress bar label unclear** — 3 participants thought it tracked score, not questions
   - Add "Question 3 of 10" text label above bar

## Metrics Summary
| Task | PURE (Grade 3) | SEQ (Grade 3) | Avg Time | Fail Rate |
|------|---------------|---------------|----------|-----------|
| Start quiz | 2.6/3 | 5.8/7 | 69 s | 0% |
| Change answer | 1.2/3 | 2.8/7 | 202 s | 40% |
| Submit quiz | 2.8/3 | 6.4/7 | 41 s | 0% |

## Recommendations Priority Matrix
| Issue | Impact | Effort | Priority |
|-------|--------|--------|----------|
| Change answer discovery | High | Low | P1 |
| Timer anxiety | High | Medium | P1 |
| Progress bar label | Medium | Low | P2 |
```

## Output
- Moderation guide document
- Raw observation notes (per participant × task)
- Usability test report (markdown, linked to Figma)
- Prioritised recommendation list filed as design tickets

## Quality Checks
- [ ] Research questions are specific and answerable from observation (not opinion)
- [ ] Tasks written as goals ("find a maths quiz"), not instructions ("click Mathematics")
- [ ] Minimum 5 participants per user segment
- [ ] SEQ collected after every task
- [ ] All sessions recorded with participant consent
- [ ] Report filed within 3 business days of final session
- [ ] Critical issues (PURE < 2 or SEQ < 4) must block launch
