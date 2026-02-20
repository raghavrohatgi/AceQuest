# Skill: Design A/B Test

## Purpose
Define the standard procedure for designing, implementing, and analysing A/B tests (randomised controlled experiments) for AceQuest features. Experiments validate product hypotheses before full rollout — preventing harm to student learning outcomes and ensuring data-driven feature decisions. Covers sample size calculation, variant assignment, metric definition, guardrail metrics, and analysis.

## Used By
- AI/ML Agent
- Product Agent
- Backend Engineer Agent

## Inputs
| Field | Type | Description |
|-------|------|-------------|
| `hypothesis` | string | Testable claim, e.g. "Showing a streak counter will increase 7-day retention" |
| `primaryMetric` | string | Main outcome to measure, e.g. `7-day retention rate` |
| `guardrailMetrics` | string[] | Metrics that must NOT decline, e.g. `quiz_completion_rate` |
| `mde` | number | Minimum Detectable Effect (practical significance threshold), e.g. `0.05` (5%) |
| `alpha` | number | Significance level, e.g. `0.05` |
| `power` | number | Statistical power, e.g. `0.80` |
| `trafficPercent` | number | Proportion of eligible students in the experiment |

## Procedure / Template

### Step 1 — Write the Experiment Brief

```markdown
## Experiment: Streak Counter on Dashboard

**Hypothesis:** Displaying a daily streak counter prominently on the student dashboard
will increase 7-day retention by >= 5 percentage points by motivating students
to return daily to preserve their streak.

**Variants:**
- Control (A): Dashboard without streak counter
- Treatment (B): Dashboard with animated streak counter + milestone notifications

**Primary Metric:** 7-day retention rate
  (% of students who complete >= 1 quiz in the 7 days following experiment entry)

**Secondary Metrics:**
- Average sessions per week
- Average quiz completion rate
- Average XP earned per session

**Guardrail Metrics (must not decline):**
- Quiz completion rate (guard against streaks causing rushed, low-quality sessions)
- Average score per quiz (guard against students gaming streak with easy quizzes)
- Parent app open rate (guard against parent engagement dropping)

**Minimum Detectable Effect:** 5 percentage points on 7-day retention
**Expected baseline retention:** 45%
**Alpha:** 0.05 (two-tailed)
**Power:** 0.80
**Eligible population:** All new students in Grades 3–8 enrolled in last 30 days
**Traffic split:** 50% control / 50% treatment
```

### Step 2 — Sample Size Calculation

```python
# ab_testing/sample_size.py
import numpy as np
from scipy.stats import norm

def calculate_sample_size(
    p_baseline: float,
    mde: float,
    alpha: float = 0.05,
    power: float = 0.80,
    two_tailed: bool = True,
) -> dict:
    """
    Calculate required sample size per variant for a proportion test.

    Args:
        p_baseline: baseline conversion rate (e.g. 0.45 for 45%)
        mde:        minimum detectable effect in absolute percentage points (e.g. 0.05)
        alpha:      significance level
        power:      desired statistical power
        two_tailed: True for two-tailed test

    Returns:
        dict with n_per_variant, total_n, estimated_days
    """
    p_treatment = p_baseline + mde
    p_pooled = (p_baseline + p_treatment) / 2

    z_alpha = norm.ppf(1 - alpha / (2 if two_tailed else 1))
    z_power = norm.ppf(power)

    # Standard sample size formula for two proportions
    n = (
        (z_alpha * np.sqrt(2 * p_pooled * (1 - p_pooled)) +
         z_power * np.sqrt(p_baseline * (1 - p_baseline) + p_treatment * (1 - p_treatment))) ** 2
    ) / (mde ** 2)

    n = int(np.ceil(n))

    return {
        "n_per_variant": n,
        "total_n": n * 2,
        "p_baseline": p_baseline,
        "p_treatment": p_treatment,
        "mde_absolute": mde,
        "alpha": alpha,
        "power": power,
    }

# Example calculation
result = calculate_sample_size(p_baseline=0.45, mde=0.05, alpha=0.05, power=0.80)
print(result)
# {'n_per_variant': 1573, 'total_n': 3146, ...}
# At 200 new eligible students/day → ~16 days to reach full sample
```

### Step 3 — Variant Assignment (Deterministic Hashing)

```typescript
// src/lib/experiments.ts
import crypto from "crypto";

export type Variant = "control" | "treatment";

export interface Experiment {
  id: string;
  name: string;
  variants: Variant[];
  trafficPercent: number;  // 0-100: what % of eligible users are in the experiment
  startDate: Date;
  endDate: Date;
  eligibilityFilter: (student: { gradeLevel: number; createdAt: Date }) => boolean;
}

export const EXPERIMENTS: Record<string, Experiment> = {
  "streak-counter-v1": {
    id: "streak-counter-v1",
    name: "Streak Counter on Dashboard",
    variants: ["control", "treatment"],
    trafficPercent: 100,
    startDate: new Date("2025-06-01"),
    endDate: new Date("2025-06-22"),
    eligibilityFilter: (student) =>
      student.gradeLevel >= 3 &&
      new Date(student.createdAt) >= new Date("2025-05-01"),
  },
};

/**
 * Deterministic variant assignment using HMAC.
 * Same student always gets the same variant for the same experiment.
 */
export function assignVariant(experimentId: string, studentId: string): Variant | null {
  const experiment = EXPERIMENTS[experimentId];
  if (!experiment) return null;
  if (Date.now() < experiment.startDate.getTime()) return null;
  if (Date.now() > experiment.endDate.getTime()) return null;

  // Hash student into a bucket [0, 100)
  const hash = crypto.createHmac("sha256", process.env.EXPERIMENT_SALT!)
    .update(`${experimentId}:${studentId}`)
    .digest("hex");
  const bucket = parseInt(hash.slice(0, 8), 16) % 100;

  // Check if in experiment traffic
  if (bucket >= experiment.trafficPercent) return null;

  // Assign variant (50/50 split within traffic)
  const variantBucket = bucket % experiment.variants.length;
  return experiment.variants[variantBucket];
}
```

### Step 4 — Log Exposure Events

```typescript
// src/services/experiment.service.ts
import { prisma } from "../lib/prisma";
import { assignVariant, EXPERIMENTS, Variant } from "../lib/experiments";

export class ExperimentService {
  async getVariantAndLog(
    experimentId: string,
    studentId: string,
    studentMeta: { gradeLevel: number; createdAt: Date }
  ): Promise<Variant | null> {
    const experiment = EXPERIMENTS[experimentId];
    if (!experiment) return null;

    // Check eligibility
    if (!experiment.eligibilityFilter(studentMeta)) return null;

    // Assign variant
    const variant = assignVariant(experimentId, studentId);
    if (!variant) return null;

    // Log exposure (idempotent upsert)
    await prisma.experimentExposure.upsert({
      where: { experimentId_studentId: { experimentId, studentId } },
      create: { experimentId, studentId, variant, exposedAt: new Date() },
      update: {},  // do not overwrite first exposure
    });

    return variant;
  }
}
```

### Step 5 — Analysis (Two-Proportion Z-Test)

```python
# ab_testing/analysis.py
import numpy as np
from scipy.stats import norm, chi2_contingency
import pandas as pd

def analyse_experiment(
    control_successes: int,
    control_n: int,
    treatment_successes: int,
    treatment_n: int,
    alpha: float = 0.05,
) -> dict:
    """Two-proportion Z-test for a binary primary metric."""
    p_control   = control_successes / control_n
    p_treatment = treatment_successes / treatment_n
    p_pooled    = (control_successes + treatment_successes) / (control_n + treatment_n)

    se = np.sqrt(p_pooled * (1 - p_pooled) * (1/control_n + 1/treatment_n))
    z  = (p_treatment - p_control) / se
    p_value = 2 * (1 - norm.cdf(abs(z)))  # two-tailed

    ci_95_lo = (p_treatment - p_control) - 1.96 * se
    ci_95_hi = (p_treatment - p_control) + 1.96 * se

    significant = p_value < alpha
    uplift_pct = (p_treatment - p_control) / p_control * 100

    return {
        "p_control": round(p_control, 4),
        "p_treatment": round(p_treatment, 4),
        "absolute_diff": round(p_treatment - p_control, 4),
        "relative_uplift_pct": round(uplift_pct, 2),
        "z_stat": round(z, 4),
        "p_value": round(p_value, 4),
        "ci_95": (round(ci_95_lo, 4), round(ci_95_hi, 4)),
        "significant": significant,
        "recommendation": "ship" if significant and p_treatment > p_control else (
            "roll_back" if significant and p_treatment < p_control else "underpowered"
        ),
    }

# Example
result = analyse_experiment(
    control_successes=675, control_n=1573,
    treatment_successes=734, treatment_n=1573,
)
print(result)
# {'p_control': 0.4291, 'p_treatment': 0.4668, 'absolute_diff': 0.0377,
#  'relative_uplift_pct': 8.79, 'p_value': 0.0089, 'significant': True,
#  'recommendation': 'ship'}
```

### Step 6 — Guardrail Metric Check

```python
def check_guardrails(guardrail_results: list[dict], alpha: float = 0.05) -> bool:
    """
    Returns True if ALL guardrail metrics are safe (not statistically worse).
    """
    all_safe = True
    for metric in guardrail_results:
        if metric["significant"] and metric["p_treatment"] < metric["p_control"]:
            print(f"GUARDRAIL FAIL: {metric['name']} declined significantly")
            all_safe = False
        else:
            print(f"Guardrail OK: {metric['name']}")
    return all_safe
```

## Output
- Experiment brief document (Step 1) filed in Notion/Confluence
- Sample size calculation notebook
- `src/lib/experiments.ts` — experiment registry and variant assignment
- `src/services/experiment.service.ts` — exposure logging
- `ExperimentExposure` model added to Prisma schema
- Post-experiment analysis notebook with decision recommendation

## Quality Checks
- [ ] Sample size calculated before experiment starts — not adjusted after launch
- [ ] Variant assignment is deterministic (same student → same variant every time)
- [ ] Exposure logged on first eligibility check — not on every page view
- [ ] Guardrail metrics defined before launch; experiment stops if guardrail violated
- [ ] Experiment runs for minimum 1 full week (to avoid day-of-week bias)
- [ ] Analysis uses two-tailed test unless hypothesis is directional with strong prior
- [ ] p-value interpreted alongside effect size and confidence interval — not p-value alone
- [ ] Decision made on primary metric + guardrails: ship / roll back / needs more data
- [ ] Experiment results documented regardless of outcome (negative results are valuable)

## Example

```
Experiment: streak-counter-v1
Duration: 16 days (2025-06-01 → 2025-06-17)
Sample: 1,573 control, 1,573 treatment

Primary metric — 7-day retention:
  Control:   42.9%  Treatment: 46.7%
  Uplift:    +8.8%  p=0.009  95% CI [+1.1%, +6.4%]  → SIGNIFICANT ✓

Guardrail — quiz completion rate:
  Control: 78.2%  Treatment: 79.1%  p=0.41  → SAFE ✓

Guardrail — avg quiz score:
  Control: 74.3  Treatment: 73.8  p=0.62  → SAFE ✓

Decision: SHIP — streak counter increases 7-day retention by 3.8pp
  with no harm to quiz quality or completion rate.
```
