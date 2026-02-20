# Skill: Build Recommendation Engine

## Purpose
Define how to build AceQuest's quiz and content recommendation engine. The engine suggests the right quiz, skill, or topic to each student at the right time — balancing curriculum coverage, ability-appropriate difficulty, engagement signals (time of day, streak, mood), and teacher-set learning goals. It combines collaborative filtering, content-based features, and IRT-informed difficulty targeting.

## Used By
- AI/ML Agent
- Backend Engineer Agent
- Product Agent

## Inputs
| Field | Type | Description |
|-------|------|-------------|
| `studentId` | string | UUID of the student |
| `gradeLevel` | number | Student's grade (1-8) |
| `theta` | number | Current IRT ability estimate |
| `recentTopics` | string[] | Topic IDs practised in the last 7 days |
| `weakSkills` | string[] | Skill IDs where theta < mastery threshold |
| `completedQuizIds` | string[] | Quiz IDs already completed |
| `sessionContext` | object | Time of day, device, session length target |
| `n` | number | Number of recommendations to return |

## Procedure / Template

### Step 1 — Feature Engineering

```python
# recommendation/features.py
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

def compute_student_features(student: dict, interactions: list[dict]) -> dict:
    """
    Compute features for a single student.
    student: DB record with gradeLevel, totalXP, currentStreak, etc.
    interactions: recent quiz submissions
    """
    now = datetime.utcnow()

    # Recency: how many days since each topic was practised
    topic_last_seen = {}
    for interaction in interactions:
        topic_id = interaction["quiz"]["topicId"]
        days_ago = (now - interaction["submittedAt"]).days
        if topic_id not in topic_last_seen or days_ago < topic_last_seen[topic_id]:
            topic_last_seen[topic_id] = days_ago

    # Performance trend: is score improving?
    if len(interactions) >= 2:
        recent_scores = [i["score"] for i in interactions[-5:]]
        score_trend = np.polyfit(range(len(recent_scores)), recent_scores, 1)[0]  # slope
    else:
        score_trend = 0.0

    # Engagement: session frequency (sessions per week)
    week_ago = now - timedelta(days=7)
    weekly_sessions = sum(1 for i in interactions if i["submittedAt"] > week_ago)

    return {
        "grade_level": student["gradeLevel"],
        "theta": student.get("theta", 0.0),
        "total_xp": student["totalXP"],
        "streak": student["currentStreak"],
        "score_trend": score_trend,
        "weekly_sessions": weekly_sessions,
        "topic_diversity": len(topic_last_seen),
        "hour_of_day": now.hour,
        "is_weekend": now.weekday() >= 5,
    }

def compute_quiz_features(quiz: dict, topic: dict, questions: list[dict]) -> dict:
    """Compute features for a candidate quiz."""
    avg_difficulty = np.mean([q["difficulty"] for q in questions]) if questions else 0
    std_difficulty = np.std([q["difficulty"] for q in questions]) if len(questions) > 1 else 0

    return {
        "topic_id": quiz["topicId"],
        "grade_level": quiz["gradeLevel"],
        "avg_difficulty": avg_difficulty,
        "std_difficulty": std_difficulty,
        "question_count": len(questions),
        "is_timed": quiz.get("timeLimit") is not None,
    }
```

### Step 2 — Scoring Function (Hybrid)

```python
# recommendation/scorer.py
import numpy as np
from typing import List, Dict

def compute_relevance_score(
    student_features: dict,
    quiz_features: dict,
    topic_coverage: dict,   # {topic_id: days_since_last_practice}
    weak_skills: List[str],
    completed_quiz_ids: set,
) -> float:
    """
    Hybrid scoring combining:
    1. Difficulty fit (IRT-based)
    2. Curriculum coverage (unseen / long-since-seen topics)
    3. Weak skill targeting
    4. Novelty (penalise completed quizzes)
    """
    score = 0.0

    # 1. DIFFICULTY FIT (weight: 0.40)
    # Target difficulty = theta; score peaks when avg_difficulty ≈ theta
    diff_gap = abs(quiz_features["avg_difficulty"] - student_features["theta"])
    difficulty_fit = np.exp(-diff_gap)   # Gaussian kernel, peaks at 0 gap
    score += 0.40 * difficulty_fit

    # 2. CURRICULUM COVERAGE (weight: 0.30)
    # Prefer topics not practised recently
    days_since = topic_coverage.get(quiz_features["topic_id"], 999)
    recency_score = min(days_since / 7, 1.0)   # saturates at 7 days
    score += 0.30 * recency_score

    # 3. WEAK SKILL TARGETING (weight: 0.20)
    # Boost quizzes that address identified weak skills
    quiz_skill_id = quiz_features.get("skill_id")
    weak_skill_bonus = 1.0 if quiz_skill_id in weak_skills else 0.0
    score += 0.20 * weak_skill_bonus

    # 4. NOVELTY (weight: 0.10)
    # Penalise quizzes already completed in this topic this week
    novelty = 0.0 if quiz_features["quiz_id"] in completed_quiz_ids else 1.0
    score += 0.10 * novelty

    return float(score)

def rank_candidates(
    student_features: dict,
    candidate_quizzes: List[dict],
    topic_coverage: dict,
    weak_skills: List[str],
    completed_quiz_ids: set,
    n: int = 5,
) -> List[dict]:
    """Return top-n recommended quizzes sorted by relevance score."""
    scored = []
    for quiz in candidate_quizzes:
        s = compute_relevance_score(
            student_features, quiz, topic_coverage, weak_skills, completed_quiz_ids
        )
        scored.append({**quiz, "relevance_score": s})

    scored.sort(key=lambda x: x["relevance_score"], reverse=True)
    return scored[:n]
```

### Step 3 — Collaborative Filtering (Peer Similarity)

```python
# recommendation/collaborative.py
import numpy as np
from scipy.sparse import csr_matrix
from sklearn.decomposition import TruncatedSVD

class CollaborativeFilter:
    """
    Matrix Factorisation using SVD on the student × quiz interaction matrix.
    Latent factors capture peer-based "students like you also enjoyed..."
    """

    def __init__(self, n_factors: int = 20):
        self.n_factors = n_factors
        self.svd = TruncatedSVD(n_components=n_factors, random_state=42)
        self.student_vectors = None
        self.quiz_vectors = None
        self.student_index: dict = {}
        self.quiz_index: dict = {}

    def fit(self, interaction_df):
        """
        interaction_df: DataFrame with columns [student_id, quiz_id, score]
        """
        students = interaction_df["student_id"].unique()
        quizzes = interaction_df["quiz_id"].unique()

        self.student_index = {s: i for i, s in enumerate(students)}
        self.quiz_index = {q: i for i, q in enumerate(quizzes)}

        rows = [self.student_index[s] for s in interaction_df["student_id"]]
        cols = [self.quiz_index[q] for q in interaction_df["quiz_id"]]
        vals = interaction_df["score"].values / 100   # normalise to [0, 1]

        matrix = csr_matrix(
            (vals, (rows, cols)),
            shape=(len(students), len(quizzes))
        )

        self.student_vectors = self.svd.fit_transform(matrix)
        self.quiz_vectors = self.svd.components_.T  # (n_quizzes, n_factors)

    def predict_score(self, student_id: str, quiz_id: str) -> float:
        """Predict a student's affinity for a quiz using dot product."""
        if student_id not in self.student_index or quiz_id not in self.quiz_index:
            return 0.5   # cold-start default

        si = self.student_index[student_id]
        qi = self.quiz_index[quiz_id]
        return float(np.dot(self.student_vectors[si], self.quiz_vectors[qi]))
```

### Step 4 — Express API Endpoint

```typescript
// src/controllers/recommendation.controller.ts
import { Request, Response, NextFunction } from "express";
import { RecommendationService } from "../services/recommendation.service";
import { z } from "zod";

const QuerySchema = z.object({
  n: z.coerce.number().int().min(1).max(20).default(5),
  goal: z.enum(["remediation", "practice", "challenge"]).default("practice"),
});

export class RecommendationController {
  constructor(private readonly service: RecommendationService) {}

  getRecommendations = async (req: Request, res: Response, next: NextFunction) => {
    try {
      const { n, goal } = QuerySchema.parse(req.query);
      const studentId = req.user!.sub;

      const recommendations = await this.service.getRecommendations({
        studentId,
        n,
        sessionGoal: goal,
      });

      res.json({
        success: true,
        data: recommendations,
        meta: { count: recommendations.length, goal },
        timestamp: new Date().toISOString(),
      });
    } catch (error) {
      next(error);
    }
  };
}
```

```typescript
// src/services/recommendation.service.ts
import { prisma } from "../lib/prisma";
import { redis } from "../lib/redis";
import { pythonBridge } from "../lib/pythonBridge";
import { MASTERY_THRESHOLD } from "../data/curriculum/constants";

const CACHE_TTL = 300;  // 5 minutes

export class RecommendationService {
  async getRecommendations({ studentId, n, sessionGoal }: {
    studentId: string;
    n: number;
    sessionGoal: string;
  }) {
    const cacheKey = `cache:recommendations:${studentId}:${sessionGoal}`;
    const cached = await redis.get(cacheKey);
    if (cached) return JSON.parse(cached);

    // Gather context
    const [student, recentSubmissions, masteries] = await Promise.all([
      prisma.student.findUniqueOrThrow({ where: { id: studentId } }),
      prisma.quizSubmission.findMany({
        where: { studentId },
        orderBy: { submittedAt: "desc" },
        take: 20,
        include: { quiz: { select: { topicId: true } } },
      }),
      prisma.skillMastery.findMany({ where: { studentId } }),
    ]);

    const weakSkills = masteries
      .filter((m) => m.theta < MASTERY_THRESHOLD)
      .map((m) => m.skillId);

    const completedQuizIds = recentSubmissions.map((s) => s.quizId);

    const result = await pythonBridge.post("/recommend", {
      studentId,
      gradeLevel: student.gradeLevel,
      theta: masteries[0]?.theta ?? 0,
      recentTopics: [...new Set(recentSubmissions.map((s) => s.quiz.topicId))],
      weakSkills,
      completedQuizIds,
      sessionGoal,
      n,
    });

    await redis.set(cacheKey, JSON.stringify(result), "EX", CACHE_TTL);
    return result;
  }
}
```

### Step 5 — Cold-Start Handling

```python
# recommendation/cold_start.py

def handle_cold_start(student: dict, all_quizzes: list[dict]) -> list[dict]:
    """
    Fallback for new students with no interaction history.
    Returns grade-appropriate, easy quizzes ordered by quiz_id (curated order).
    """
    grade = student["gradeLevel"]
    candidates = [
        q for q in all_quizzes
        if q["gradeLevel"] == grade
        and q["status"] == "ACTIVE"
        and -1.5 < q["avg_difficulty"] < 0   # easy but not trivial
    ]
    # Sort by curated order (quiz sequence set by curriculum team)
    return sorted(candidates, key=lambda q: q.get("sequenceOrder", 999))[:5]
```

## Output
- `recommendation/features.py` — student and quiz feature computation
- `recommendation/scorer.py` — hybrid scoring function
- `recommendation/collaborative.py` — matrix factorisation model
- `recommendation/cold_start.py` — new student fallback
- `src/services/recommendation.service.ts` — Express integration
- `GET /api/v1/recommendations` — endpoint returning top-N quiz recommendations

## Quality Checks
- [ ] Difficulty fit uses IRT theta — not raw score percentage
- [ ] Collaborative filter handles cold-start (new student with 0 history)
- [ ] Completed quizzes penalised in novelty score — no repeat recommendations in same week
- [ ] Weak skill targeting boosts quizzes aligned to skills below mastery threshold
- [ ] Cache TTL = 5 min — avoids stale recommendations while reducing DB pressure
- [ ] Recommendation diversity checked: not all recommendations from same topic
- [ ] A/B test framework in place (see `design-ab-test.md`) before rolling out new scoring weights
- [ ] Offline evaluation: precision@5 >= 0.6 on held-out student-quiz interaction data

## Example

```
Student: Priya, Grade 5, theta = 0.8 (above average)
Weak skills: [fractions-multiply, percentages]
Recent topics: [mathematics-grade5] (practised 2 days ago)
Goal: practice

Recommendations returned:
1. "Percentages Challenge" (difficulty 0.9, weak skill match, 2-day gap → score 0.82)
2. "Fractions Multiplication" (difficulty 0.7, weak skill match, 3-day gap → score 0.78)
3. "Decimal Operations" (difficulty 0.8, no weak skill match, 5-day gap → score 0.65)
4. "English – Reading Comprehension" (different topic, 7-day gap → score 0.58)
5. "Science – Forces" (different topic, 14-day gap → score 0.55)
```
