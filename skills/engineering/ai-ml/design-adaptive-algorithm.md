# Skill: Design Adaptive Learning Algorithm

## Purpose
Define the procedure for designing and implementing an adaptive learning algorithm for AceQuest. The algorithm personalises the sequence of questions and quizzes each student receives based on their demonstrated ability, response patterns, and curriculum objectives. It integrates with the IRT model (see `implement-irt-model.md`) and the recommendation engine to create a closed loop of assess → adapt → present → reassess.

## Used By
- AI/ML Agent
- Backend Engineer Agent
- Product Agent

## Inputs
| Field | Type | Description |
| --- | --- | --- |
| `studentId` | string | UUID of the student |
| `topicId` | string | Current topic/subject being practiced |
| `recentResponses` | object[] | Last N question responses with correctness and time |
| `skillMastery` | object | Current IRT theta estimate per skill |
| `curriculum` | object | Ordered skill tree for the topic |
| `sessionGoal` | string | `"remediation" \ | "practice" \ | "challenge"` |

## Algorithm Design

### Step 1 — Conceptual Architecture

```
┌──────────────────────────────────────────────────────────┐
│                  ADAPTIVE ENGINE                         │
│                                                          │
│  ┌─────────────┐   ┌──────────────┐   ┌──────────────┐ │
│  │   Student   │   │  Question    │   │  Curriculum  │ │
│  │  Ability    │──▶│  Selector    │──▶│   Mapper     │ │
│  │  (θ / IRT)  │   │  (next-best) │   │  (skill DAG) │ │
│  └─────────────┘   └──────────────┘   └──────────────┘ │
│         ▲                  │                   │         │
│         │                  ▼                   ▼         │
│  ┌─────────────┐   ┌──────────────┐   ┌──────────────┐ │
│  │  Response   │   │  Question    │   │   Content    │ │
│  │  Processor  │◀──│  Presented   │   │    Bank      │ │
│  │  (θ update) │   │  to Student  │   │ (difficulty  │ │
│  └─────────────┘   └──────────────┘   │  calibrated) │ │
│                                        └──────────────┘ │
└──────────────────────────────────────────────────────────┘
```

### Step 2 — Target Information Function (TIF)

Select the question that provides maximum information at the student's current ability level.

```python
# adaptive_engine/selector.py
import numpy as np
from dataclasses import dataclass
from typing import List

@dataclass
class Question:
    id: str
    difficulty: float        # IRT b parameter (-3 to 3)
    discrimination: float    # IRT a parameter (0.5 to 2.5)
    guessing: float          # IRT c parameter (0 to 0.35)

def irt_probability(theta: float, q: Question) -> float:
    """3-PL IRT model: probability of correct response."""
    exponent = q.discrimination * (theta - q.difficulty)
    return q.guessing + (1 - q.guessing) / (1 + np.exp(-exponent))

def information(theta: float, q: Question) -> float:
    """Fisher information for a question at ability theta."""
    p = irt_probability(theta, q)
    q_val = 1 - p
    numerator = (q.discrimination ** 2) * (p - q.guessing) ** 2
    denominator = (1 - q.guessing) ** 2 * p * q_val
    return numerator / denominator if denominator > 0 else 0

def select_next_question(
    theta: float,
    candidate_questions: List[Question],
    answered_ids: set[str],
    session_goal: str = "practice"
) -> Question:
    """
    Select the optimal next question using maximum Fisher information.
    Applies goal-based adjustment to theta before selection.
    """
    goal_offset = {
        "remediation": -0.5,    # present easier questions
        "practice":    0.0,     # target current ability
        "challenge":   +0.5,    # present harder questions
    }
    effective_theta = theta + goal_offset.get(session_goal, 0)

    eligible = [q for q in candidate_questions if q.id not in answered_ids]
    if not eligible:
        return None

    scored = [(q, information(effective_theta, q)) for q in eligible]
    return max(scored, key=lambda x: x[1])[0]
```

### Step 3 — Ability Estimation (EAP — Expected A Posteriori)

```python
# adaptive_engine/estimator.py
import numpy as np
from scipy.integrate import quad

def eap_estimate(
    responses: List[dict],   # [{question: Question, correct: bool}]
    prior_mean: float = 0.0,
    prior_std: float = 1.0
) -> tuple[float, float]:
    """
    EAP ability estimator using numerical integration.
    Returns (theta_estimate, standard_error).
    """
    def likelihood(theta: float) -> float:
        L = 1.0
        for r in responses:
            p = irt_probability(theta, r["question"])
            L *= p if r["correct"] else (1 - p)
        return L

    def prior(theta: float) -> float:
        return np.exp(-0.5 * ((theta - prior_mean) / prior_std) ** 2)

    theta_range = np.linspace(-4, 4, 200)
    weights = np.array([likelihood(t) * prior(t) for t in theta_range])
    normalizer = np.trapz(weights, theta_range)

    if normalizer < 1e-10:
        return prior_mean, prior_std   # fallback to prior

    theta_est = np.trapz(weights * theta_range, theta_range) / normalizer
    theta_var = np.trapz(weights * (theta_range - theta_est) ** 2, theta_range) / normalizer
    se = np.sqrt(theta_var)
    return float(theta_est), float(se)
```

### Step 4 — Stopping Rules

```python
# adaptive_engine/stopping.py

MIN_QUESTIONS = 5
MAX_QUESTIONS = 20
SE_THRESHOLD = 0.3    # stop when standard error is small enough

def should_stop(
    n_answered: int,
    standard_error: float,
    time_elapsed_s: int,
    session_time_limit_s: int = 600
) -> tuple[bool, str]:
    """
    Returns (stop, reason).
    """
    if n_answered < MIN_QUESTIONS:
        return False, "minimum_not_reached"

    if n_answered >= MAX_QUESTIONS:
        return True, "max_questions_reached"

    if standard_error < SE_THRESHOLD:
        return True, "sufficient_precision"

    if time_elapsed_s >= session_time_limit_s:
        return True, "time_limit_reached"

    return False, "continue"
```

### Step 5 — Express Integration (Service Layer)

```typescript
// src/services/adaptiveEngine.service.ts
import { prisma } from "../lib/prisma";
import { redis } from "../lib/redis";
import { pythonBridge } from "../lib/pythonBridge";  // calls Python microservice

export interface AdaptiveNextQuestion {
  id: string;
  difficulty: number;
  type: string;
  text: string;
  options: Array<{ id: string; text: string }>;
}

export class AdaptiveEngineService {
  async selectNextQuestion(
    studentId: string,
    topicId: string
  ): Promise<AdaptiveNextQuestion | null> {
    // 1. Get current ability estimate from DB (or default 0)
    const mastery = await prisma.skillMastery.findFirst({
      where: { studentId, skill: { topicId } },
      orderBy: { updatedAt: "desc" },
    });
    const theta = mastery?.theta ?? 0;

    // 2. Get answered question IDs (from this session, cached in Redis)
    const sessionKey = `session:${studentId}:${topicId}:answered`;
    const answeredJson = await redis.get(sessionKey);
    const answeredIds = new Set<string>(answeredJson ? JSON.parse(answeredJson) : []);

    // 3. Get candidate questions for this topic
    const candidates = await prisma.question.findMany({
      where: {
        quiz: { topicId, status: "ACTIVE" },
        id: { notIn: [...answeredIds] },
      },
      include: { options: { where: { isCorrect: false }, take: 3 }, quiz: false },
    });

    if (candidates.length === 0) return null;

    // 4. Call Python microservice to select optimal question
    const selected = await pythonBridge.post("/select-question", {
      theta,
      candidates: candidates.map((q) => ({
        id: q.id,
        difficulty: q.difficulty,
        discrimination: 1.0,   // default until calibrated
        guessing: 0.25,        // 4-option multiple choice
      })),
      sessionGoal: "practice",
    });

    // 5. Cache the selection to avoid repeats
    answeredIds.add(selected.id);
    await redis.set(sessionKey, JSON.stringify([...answeredIds]), "EX", 3600);

    return prisma.question.findUnique({
      where: { id: selected.id },
      include: { options: { select: { id: true, text: true } } },
    });
  }

  async updateAbilityEstimate(
    studentId: string,
    skillId: string,
    responses: Array<{ questionId: string; correct: boolean }>
  ): Promise<{ theta: number; se: number }> {
    const result = await pythonBridge.post("/update-ability", {
      studentId,
      skillId,
      responses,
    });

    await prisma.skillMastery.upsert({
      where: { studentId_skillId: { studentId, skillId } },
      create: { studentId, skillId, theta: result.theta, attempts: responses.length },
      update: {
        theta: result.theta,
        attempts: { increment: responses.length },
      },
    });

    return result;
  }
}
```

### Step 6 — Skill Tree / Curriculum DAG

```typescript
// src/data/curriculum/mathematics-grade5.ts
export const grade5MathCurriculum = {
  topicId: "mathematics-grade5",
  skills: [
    { id: "fractions-basic",    name: "Basic Fractions",      prerequisites: [] },
    { id: "fractions-addition", name: "Adding Fractions",     prerequisites: ["fractions-basic"] },
    { id: "fractions-multiply", name: "Multiplying Fractions",prerequisites: ["fractions-addition"] },
    { id: "decimals-basic",     name: "Decimal Numbers",      prerequisites: ["fractions-basic"] },
    { id: "decimals-operations",name: "Decimal Operations",   prerequisites: ["decimals-basic"] },
    { id: "percentages",        name: "Percentages",          prerequisites: ["fractions-multiply", "decimals-operations"] },
  ],
};

// Skill unlocked only when prerequisite theta >= mastery threshold
export const MASTERY_THRESHOLD = 1.0;  // IRT theta value
```

## Output
- `adaptive_engine/selector.py` — question selection algorithm
- `adaptive_engine/estimator.py` — EAP ability estimator
- `adaptive_engine/stopping.py` — stopping rules
- `src/services/adaptiveEngine.service.ts` — Express service integrating Python bridge
- `src/data/curriculum/<topic>.ts` — skill tree DAG

## Quality Checks
- [ ] Information function returns 0 for questions where denominator is 0 (guard against division by zero)
- [ ] EAP estimator falls back to prior when likelihood collapses
- [ ] Minimum 5 questions enforced before stopping
- [ ] SE threshold triggers stop (avoids over-testing students)
- [ ] Session answered IDs cached in Redis with TTL to avoid repeating questions
- [ ] Skill tree prerequisites enforced — students cannot access skill without mastering prerequisites
- [ ] Algorithm evaluated on held-out student data (see evaluate-model.md)
- [ ] Unit tests for `select_next_question`: highest-information question selected, answered IDs excluded

## Example

```python
theta = 0.5   # above average student
candidates = [
  Question("q1", difficulty=0.6, discrimination=1.2, guessing=0.25),  # near theta
  Question("q2", difficulty=2.0, discrimination=1.2, guessing=0.25),  # much harder
  Question("q3", difficulty=-1.0, discrimination=1.2, guessing=0.25), # much easier
]

selected = select_next_question(theta, candidates, answered_ids=set())
# selected = q1  — maximum information near theta = 0.5
# info(theta=0.5, q1) ≈ 0.82
# info(theta=0.5, q2) ≈ 0.11  (too hard)
# info(theta=0.5, q3) ≈ 0.09  (too easy)
```
