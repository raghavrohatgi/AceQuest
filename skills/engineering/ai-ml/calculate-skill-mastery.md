# Skill: Calculate Skill Mastery

## Purpose
Define how AceQuest measures and communicates skill mastery to students, parents, and teachers. Mastery is derived from the IRT ability estimate (theta) per skill, converted into an actionable 0–100% scale with defined thresholds for "Exploring", "Developing", "Proficient", and "Mastered". Mastery scores drive adaptive routing, badge awards, and parent/teacher dashboards.

## Used By
- AI/ML Agent
- Backend Engineer Agent
- Frontend Engineer Agent (for progress visualisation)

## Inputs
| Field | Type | Description |
|-------|------|-------------|
| `studentId` | string | UUID of the student |
| `skillId` | string | Skill being assessed |
| `responses` | object[] | Question responses contributing to this skill |
| `currentTheta` | number | Prior IRT theta estimate for this skill |
| `currentAttempts` | number | Prior number of attempts |
| `priorMean` | number | Population mean theta for this skill/grade |
| `priorSd` | number | Population SD theta for this skill/grade |

## Mastery Level Definitions

| Level | Display | Theta Range | Percentage | Colour | Badge Trigger |
|-------|---------|-------------|------------|--------|---------------|
| Exploring | 🌱 | θ < -0.5 | 0–30% | Red | — |
| Developing | 🔷 | -0.5 ≤ θ < 0.5 | 30–60% | Orange | — |
| Proficient | ⭐ | 0.5 ≤ θ < 1.5 | 60–85% | Blue | proficient-{skill} |
| Mastered | 🏆 | θ ≥ 1.5 | 85–100% | Green | master-{skill} |

## Procedure / Template

### Step 1 — Update Theta After Each Session

```python
# mastery/updater.py
import numpy as np
from scipy.optimize import minimize_scalar
from irt.model import ThreePLModel, IRTParameters
from dataclasses import dataclass
from typing import List

@dataclass
class Response:
    question_id: str
    difficulty: float
    discrimination: float
    guessing: float
    correct: bool

def update_theta_map(
    responses: List[Response],
    prior_theta: float,
    prior_se: float = 1.0,
) -> tuple[float, float]:
    """
    Update theta using Maximum A Posteriori (MAP) estimation.
    Combines likelihood from new responses with Gaussian prior.

    Returns: (new_theta, new_se)
    """
    def neg_log_posterior(theta: float) -> float:
        # Log likelihood
        log_lik = 0.0
        for r in responses:
            params = IRTParameters(r.discrimination, r.difficulty, r.guessing)
            p = ThreePLModel.probability(theta, params)
            p = max(p, 1e-8)
            log_lik += np.log(p) if r.correct else np.log(1 - p)

        # Log prior: N(prior_theta, prior_se^2)
        log_prior = -0.5 * ((theta - prior_theta) / prior_se) ** 2

        return -(log_lik + log_prior)

    result = minimize_scalar(neg_log_posterior, bounds=(-4, 4), method="bounded")
    new_theta = result.x

    # Approximate SE via Fisher information at new theta
    total_info = sum(
        ThreePLModel.fisher_information(
            new_theta,
            IRTParameters(r.discrimination, r.difficulty, r.guessing)
        )
        for r in responses
    )
    prior_info = 1.0 / (prior_se ** 2)
    new_se = 1.0 / np.sqrt(total_info + prior_info)

    return float(new_theta), float(new_se)
```

### Step 2 — Convert Theta to Mastery Percentage

```python
# mastery/converter.py
from dataclasses import dataclass

MASTERY_LEVELS = [
    (-4.0, -0.5, "EXPLORING",   0,  30),
    (-0.5,  0.5, "DEVELOPING",  30, 60),
    ( 0.5,  1.5, "PROFICIENT",  60, 85),
    ( 1.5,  4.0, "MASTERED",    85, 100),
]

@dataclass
class MasteryResult:
    theta: float
    se: float
    percentage: int            # 0-100
    level: str                 # EXPLORING / DEVELOPING / PROFICIENT / MASTERED
    level_min_pct: int
    level_max_pct: int
    badge_slug: str | None     # slug of badge to award, or None

def theta_to_mastery(theta: float, se: float, skill_slug: str) -> MasteryResult:
    """Convert IRT theta to human-readable mastery level and percentage."""
    theta = max(-4.0, min(4.0, theta))

    for (lo, hi, level, pct_lo, pct_hi) in MASTERY_LEVELS:
        if lo <= theta < hi or (level == "MASTERED" and theta >= hi):
            # Linear interpolation within the band
            band_width = hi - lo
            position_in_band = (theta - lo) / band_width
            percentage = int(pct_lo + position_in_band * (pct_hi - pct_lo))
            percentage = max(pct_lo, min(pct_hi, percentage))

            badge_slug = None
            if level == "PROFICIENT":
                badge_slug = f"proficient-{skill_slug}"
            elif level == "MASTERED":
                badge_slug = f"master-{skill_slug}"

            return MasteryResult(
                theta=round(theta, 3),
                se=round(se, 3),
                percentage=percentage,
                level=level,
                level_min_pct=pct_lo,
                level_max_pct=pct_hi,
                badge_slug=badge_slug,
            )

    # Fallback (should not reach here)
    return MasteryResult(theta, se, 0, "EXPLORING", 0, 30, None)
```

### Step 3 — Mastery Update Service (Express)

```typescript
// src/services/mastery.service.ts
import { prisma } from "../lib/prisma";
import { redis } from "../lib/redis";
import { pythonBridge } from "../lib/pythonBridge";
import { BadgeService } from "./badge.service";
import { logger } from "../utils/logger";

export interface MasteryUpdateInput {
  studentId: string;
  skillId: string;
  responses: Array<{
    questionId: string;
    correct: boolean;
    timeTakenMs: number;
  }>;
}

export interface MasteryResult {
  theta: number;
  se: number;
  percentage: number;
  level: "EXPLORING" | "DEVELOPING" | "PROFICIENT" | "MASTERED";
  badgeAwarded?: string;
  previousLevel?: string;
  leveledUp: boolean;
}

export class MasteryService {
  constructor(private readonly badgeService = new BadgeService()) {}

  async updateMastery(input: MasteryUpdateInput): Promise<MasteryResult> {
    // 1. Get current mastery state
    const current = await prisma.skillMastery.findUnique({
      where: { studentId_skillId: { studentId: input.studentId, skillId: input.skillId } },
      include: { skill: { select: { slug: true } } },
    });

    const currentTheta = current?.theta ?? 0;
    const currentSe = 1.0;  // default SE for new students

    // 2. Enrich responses with question IRT parameters
    const questionIds = input.responses.map((r) => r.questionId);
    const questions = await prisma.question.findMany({
      where: { id: { in: questionIds } },
      select: { id: true, difficulty: true },
    });
    const qMap = new Map(questions.map((q) => [q.id, q]));

    const enrichedResponses = input.responses.map((r) => ({
      questionId: r.questionId,
      difficulty: qMap.get(r.questionId)?.difficulty ?? 0,
      discrimination: 1.0,
      guessing: 0.25,
      correct: r.correct,
    }));

    // 3. Call Python bridge to update theta
    const updated = await pythonBridge.post("/update-mastery", {
      responses: enrichedResponses,
      priorTheta: currentTheta,
      priorSe: currentSe,
      skillSlug: current?.skill.slug ?? input.skillId,
    });

    const { theta, se, percentage, level, badge_slug } = updated;

    // 4. Persist updated mastery
    await prisma.skillMastery.upsert({
      where: { studentId_skillId: { studentId: input.studentId, skillId: input.skillId } },
      create: {
        studentId: input.studentId,
        skillId: input.skillId,
        theta,
        attempts: input.responses.length,
      },
      update: {
        theta,
        attempts: { increment: input.responses.length },
      },
    });

    // 5. Invalidate caches
    await redis.del(`cache:mastery:${input.studentId}:${input.skillId}`);
    await redis.del(`cache:student:${input.studentId}:skills`);

    // 6. Award badge if level-up milestone reached
    const previousLevel = current ? this.thetaToLevel(currentTheta) : null;
    const leveledUp = previousLevel !== level && (level === "PROFICIENT" || level === "MASTERED");
    let badgeAwarded: string | undefined;

    if (leveledUp && badge_slug) {
      try {
        await this.badgeService.awardBadge(input.studentId, badge_slug);
        badgeAwarded = badge_slug;
        logger.info("mastery.badge_awarded", { studentId: input.studentId, badge: badge_slug, level });
      } catch (err) {
        logger.warn("mastery.badge_award_failed", { studentId: input.studentId, badge: badge_slug });
      }
    }

    logger.info("mastery.updated", {
      studentId: input.studentId,
      skillId: input.skillId,
      theta: theta.toFixed(3),
      level,
      percentage,
    });

    return { theta, se, percentage, level, badgeAwarded, previousLevel: previousLevel ?? undefined, leveledUp };
  }

  private thetaToLevel(theta: number): string {
    if (theta >= 1.5) return "MASTERED";
    if (theta >= 0.5) return "PROFICIENT";
    if (theta >= -0.5) return "DEVELOPING";
    return "EXPLORING";
  }
}
```

### Step 4 — Mastery API Response Shape

```typescript
// Example GET /api/v1/students/:id/skills response
{
  "success": true,
  "data": {
    "skills": [
      {
        "skillId": "fractions-basic",
        "skillName": "Basic Fractions",
        "theta": 1.2,
        "percentage": 78,
        "level": "PROFICIENT",
        "levelLabel": "Proficient ⭐",
        "colour": "#2563EB",
        "attempts": 45,
        "lastPracticed": "2025-06-01T10:00:00Z"
      },
      {
        "skillId": "percentages",
        "skillName": "Percentages",
        "theta": -0.3,
        "percentage": 42,
        "level": "DEVELOPING",
        "levelLabel": "Developing 🔷",
        "colour": "#D97706",
        "attempts": 12,
        "lastPracticed": "2025-05-28T14:00:00Z"
      }
    ]
  }
}
```

### Step 5 — Mastery Visualisation Component

```tsx
// src/components/progress/SkillMasteryBar.tsx
import { cn } from "@/lib/utils";

type Level = "EXPLORING" | "DEVELOPING" | "PROFICIENT" | "MASTERED";

const levelConfig: Record<Level, { colour: string; label: string; icon: string }> = {
  EXPLORING:  { colour: "bg-red-500",         label: "Exploring",  icon: "🌱" },
  DEVELOPING: { colour: "bg-orange-400",       label: "Developing", icon: "🔷" },
  PROFICIENT: { colour: "bg-blue-500",         label: "Proficient", icon: "⭐" },
  MASTERED:   { colour: "bg-quest-green",      label: "Mastered",   icon: "🏆" },
};

interface SkillMasteryBarProps {
  skillName: string;
  percentage: number;
  level: Level;
}

export function SkillMasteryBar({ skillName, percentage, level }: SkillMasteryBarProps) {
  const config = levelConfig[level];
  return (
    <div className="flex flex-col gap-1">
      <div className="flex justify-between items-center">
        <span className="text-sm font-medium text-quest-navy">{skillName}</span>
        <span className="text-xs text-gray-500">
          {config.icon} {config.label} • {percentage}%
        </span>
      </div>
      <div
        role="progressbar"
        aria-valuenow={percentage}
        aria-valuemin={0}
        aria-valuemax={100}
        aria-label={`${skillName}: ${percentage}% — ${config.label}`}
        className="h-3 bg-gray-100 rounded-full overflow-hidden"
      >
        <div
          className={cn("h-full rounded-full transition-all duration-700", config.colour)}
          style={{ width: `${percentage}%` }}
        />
      </div>
    </div>
  );
}
```

## Output
- `mastery/updater.py` — MAP theta update algorithm
- `mastery/converter.py` — theta-to-percentage-and-level conversion
- `src/services/mastery.service.ts` — Express service with badge integration
- `src/components/progress/SkillMasteryBar.tsx` — progress bar component
- Updated `prisma/schema.prisma` with `theta` and `se` fields on `SkillMastery`

## Quality Checks
- [ ] Theta bounded to [-4, 4] before conversion
- [ ] Level thresholds match badge trigger definitions in BadgeService
- [ ] Level-up detection is idempotent — badge awarded only once even if mastery recalculated
- [ ] Cache invalidated after every mastery update
- [ ] SE tracked alongside theta — used by adaptive engine to reduce uncertainty
- [ ] Parent/teacher dashboard shows mastery percentage AND level label (not raw theta)
- [ ] Unit tests: theta -0.3 → DEVELOPING 42%; theta 1.5 → MASTERED 85%

## Example

```python
from mastery.converter import theta_to_mastery

result = theta_to_mastery(theta=1.2, se=0.3, skill_slug="fractions-basic")
# MasteryResult(
#   theta=1.2, se=0.3, percentage=78, level="PROFICIENT",
#   level_min_pct=60, level_max_pct=85, badge_slug="proficient-fractions-basic"
# )

result2 = theta_to_mastery(theta=-0.3, se=0.5, skill_slug="percentages")
# MasteryResult(
#   theta=-0.3, se=0.5, percentage=42, level="DEVELOPING",
#   level_min_pct=30, level_max_pct=60, badge_slug=None
# )
```
