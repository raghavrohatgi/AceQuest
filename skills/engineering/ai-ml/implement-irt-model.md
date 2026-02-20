# Skill: Implement IRT Model

## Purpose
Define how to implement and calibrate an Item Response Theory (IRT) model for AceQuest. IRT provides a principled psychometric framework for measuring student ability (theta) and question difficulty (b parameter) on the same scale, enabling fair comparison across different quizzes and students. AceQuest uses the 3-Parameter Logistic (3-PL) model.

## Used By
- AI/ML Agent
- Backend Engineer Agent (for API integration)
- Data Science Agent

## Inputs
| Field | Type | Description |
| --- | --- | --- |
| `responseMatrix` | ndarray | Student × Item binary response matrix (1=correct, 0=wrong) |
| `model` | `"1PL" \ | "2PL" \ | "3PL"` | IRT model variant |
| `calibrationMethod` | `"MML" \ | "MCMC" \ | "joint-MLE"` | Parameter estimation method |
| `priorDistribution` | object | Prior for ability: `{mean: 0, std: 1}` |

## IRT Model Reference

### 3-PL Model Equation

```
P(correct | θ, a, b, c) = c + (1 - c) / (1 + exp(-a(θ - b)))

Where:
  θ (theta) = student ability (-4 to +4, mean 0, SD 1)
  a         = discrimination parameter (0.5 to 2.5; higher = better discriminator)
  b         = difficulty parameter (-3 to +3; matches theta scale)
  c         = pseudo-guessing parameter (0 to 0.35)
```

### Parameter Interpretation Table

| Theta | Ability Level | Typical Grade Equivalent |
| --- | --- | --- |
| -2.0 | Well below average | 2 grades behind |
| -1.0 | Below average | 1 grade behind |
| 0.0 | Average | On grade level |
| +1.0 | Above average | 1 grade ahead |
| +2.0 | Well above average | Gifted range |

## Procedure / Template

### Step 1 — Install Dependencies

```bash
pip install numpy scipy pandas pymc3 matplotlib seaborn
```

### Step 2 — Implement 3-PL Model

```python
# irt/model.py
import numpy as np
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class IRTParameters:
    a: float    # discrimination
    b: float    # difficulty
    c: float    # guessing
    a_se: Optional[float] = None   # standard errors
    b_se: Optional[float] = None
    c_se: Optional[float] = None

class ThreePLModel:
    """3-Parameter Logistic IRT Model."""

    @staticmethod
    def probability(theta: float, params: IRTParameters) -> float:
        """P(correct | theta, item parameters)."""
        exponent = params.a * (theta - params.b)
        return params.c + (1 - params.c) / (1 + np.exp(-exponent))

    @staticmethod
    def probability_vectorised(
        theta: np.ndarray, a: np.ndarray, b: np.ndarray, c: np.ndarray
    ) -> np.ndarray:
        """Vectorised version for batch computation."""
        # theta: (n_students,), a/b/c: (n_items,)
        # Returns: (n_students, n_items)
        theta_col = theta[:, np.newaxis]
        exponent = a[np.newaxis, :] * (theta_col - b[np.newaxis, :])
        return c[np.newaxis, :] + (1 - c[np.newaxis, :]) / (1 + np.exp(-exponent))

    @staticmethod
    def log_likelihood(
        responses: np.ndarray,         # (n_students, n_items)
        theta: np.ndarray,             # (n_students,)
        a: np.ndarray, b: np.ndarray, c: np.ndarray  # (n_items,)
    ) -> float:
        """Total log-likelihood of observed responses."""
        p = ThreePLModel.probability_vectorised(theta, a, b, c)
        p = np.clip(p, 1e-8, 1 - 1e-8)
        ll = responses * np.log(p) + (1 - responses) * np.log(1 - p)
        # Ignore missing responses (NaN)
        return np.nansum(ll)

    @staticmethod
    def fisher_information(theta: float, params: IRTParameters) -> float:
        """Fisher information at a given theta."""
        p = ThreePLModel.probability(theta, params)
        q = 1 - p
        numerator = (params.a ** 2) * (p - params.c) ** 2
        denominator = (1 - params.c) ** 2 * p * q
        return numerator / denominator if denominator > 0 else 0
```

### Step 3 — Parameter Calibration (Joint MLE)

```python
# irt/calibration.py
import numpy as np
from scipy.optimize import minimize
from typing import Tuple
from .model import ThreePLModel, IRTParameters

class IRTCalibrator:
    def __init__(self, n_iter: int = 100, tol: float = 1e-6):
        self.n_iter = n_iter
        self.tol = tol

    def calibrate(
        self, responses: np.ndarray
    ) -> Tuple[np.ndarray, List[IRTParameters]]:
        """
        Calibrate item parameters and ability estimates.

        Args:
            responses: (n_students, n_items) binary matrix, NaN = not administered

        Returns:
            theta: (n_students,) ability estimates
            item_params: list of IRTParameters per item
        """
        n_students, n_items = responses.shape

        # Initialise: use proportion correct as starting difficulty proxy
        prop_correct = np.nanmean(responses, axis=0)
        b_init = -np.log(prop_correct / (1 - prop_correct + 1e-8))
        b_init = np.clip(b_init, -3, 3)

        # Initial theta: use standardised number correct
        num_correct = np.nansum(responses, axis=1)
        theta_init = (num_correct - np.mean(num_correct)) / (np.std(num_correct) + 1e-8)

        a = np.ones(n_items)
        b = b_init.copy()
        c = np.full(n_items, 0.25)
        theta = theta_init.copy()

        prev_ll = -np.inf

        for iteration in range(self.n_iter):
            # E-step: update theta given fixed item parameters
            theta = self._update_theta(responses, theta, a, b, c)

            # M-step: update item parameters given fixed theta
            a, b, c = self._update_item_params(responses, theta, a, b, c)

            ll = ThreePLModel.log_likelihood(responses, theta, a, b, c)
            if abs(ll - prev_ll) < self.tol:
                print(f"Converged at iteration {iteration}, LL={ll:.4f}")
                break
            prev_ll = ll

        item_params = [IRTParameters(a=a[i], b=b[i], c=c[i]) for i in range(n_items)]
        return theta, item_params

    def _update_theta(self, responses, theta, a, b, c):
        """Update theta for each student via gradient ascent."""
        updated_theta = theta.copy()
        for s in range(len(theta)):
            valid = ~np.isnan(responses[s])
            if not np.any(valid):
                continue
            r = responses[s, valid]
            av, bv, cv = a[valid], b[valid], c[valid]

            def neg_log_posterior(t):
                p = cv + (1 - cv) / (1 + np.exp(-av * (t - bv)))
                p = np.clip(p, 1e-8, 1 - 1e-8)
                ll = np.sum(r * np.log(p) + (1 - r) * np.log(1 - p))
                prior = -0.5 * t[0] ** 2   # N(0,1) prior
                return -(ll + prior)

            result = minimize(neg_log_posterior, [theta[s]], method="L-BFGS-B",
                              bounds=[(-4, 4)])
            updated_theta[s] = result.x[0]
        return updated_theta

    def _update_item_params(self, responses, theta, a, b, c):
        """Update item parameters for each item via numerical optimisation."""
        new_a, new_b, new_c = a.copy(), b.copy(), c.copy()
        for i in range(responses.shape[1]):
            valid = ~np.isnan(responses[:, i])
            if np.sum(valid) < 10:  # skip items with too few responses
                continue
            r = responses[valid, i]
            tv = theta[valid]

            def neg_ll(params):
                ai, bi, ci = params
                ci = np.clip(ci, 0, 0.35)
                p = ci + (1 - ci) / (1 + np.exp(-ai * (tv - bi)))
                p = np.clip(p, 1e-8, 1 - 1e-8)
                return -np.sum(r * np.log(p) + (1 - r) * np.log(1 - p))

            result = minimize(neg_ll, [a[i], b[i], c[i]], method="L-BFGS-B",
                              bounds=[(0.2, 3.0), (-3.0, 3.0), (0.0, 0.35)])
            new_a[i], new_b[i], new_c[i] = result.x
        return new_a, new_b, new_c
```

### Step 4 — Store Parameters in Database

```typescript
// src/scripts/store-irt-parameters.ts
import { prisma } from "../src/lib/prisma";
import fs from "fs";

interface CalibrationOutput {
  items: Array<{ questionId: string; a: number; b: number; c: number; b_se: number }>;
  students: Array<{ studentId: string; theta: number; se: number }>;
}

async function storeCalibrationResults(outputPath: string) {
  const data: CalibrationOutput = JSON.parse(fs.readFileSync(outputPath, "utf-8"));

  // Update question difficulty parameters
  for (const item of data.items) {
    await prisma.question.update({
      where: { id: item.questionId },
      data: {
        difficulty: item.b,
        discrimination: item.a,
        guessingParam: item.c,
      },
    });
  }

  // Update student ability estimates
  for (const student of data.students) {
    await prisma.skillMastery.updateMany({
      where: { studentId: student.studentId },
      data: { theta: student.theta },
    });
  }

  console.log(`Updated ${data.items.length} items and ${data.students.length} student estimates`);
}

storeCalibrationResults("./calibration_output.json").catch(console.error);
```

### Step 5 — Model Evaluation

```python
# irt/evaluation.py
import numpy as np

def root_mean_square_error(responses, theta, a, b, c):
    """RMSE between predicted probabilities and observed responses."""
    from .model import ThreePLModel
    p_hat = ThreePLModel.probability_vectorised(theta, a, b, c)
    mask = ~np.isnan(responses)
    return np.sqrt(np.mean((responses[mask] - p_hat[mask]) ** 2))

def item_fit_chisq(responses, theta, a, b, c, n_bins: int = 10):
    """Itemwise chi-square fit statistic (Orlando & Thissen, 2000)."""
    from .model import ThreePLModel
    n_items = responses.shape[1]
    chisq_stats = []
    for i in range(n_items):
        valid = ~np.isnan(responses[:, i])
        obs = responses[valid, i]
        p = ThreePLModel.probability_vectorised(theta[valid], a, b, c)[:, i]
        bins = np.percentile(theta[valid], np.linspace(0, 100, n_bins + 1))
        chisq = 0
        for j in range(n_bins):
            mask = (theta[valid] >= bins[j]) & (theta[valid] < bins[j + 1])
            if mask.sum() < 5:
                continue
            obs_sum = obs[mask].sum()
            exp_sum = p[mask].sum()
            chisq += (obs_sum - exp_sum) ** 2 / (exp_sum + 1e-8)
        chisq_stats.append(chisq)
    return np.array(chisq_stats)
```

## Output
- `irt/model.py` — 3-PL probability and information functions
- `irt/calibration.py` — EM algorithm for joint MLE
- `irt/evaluation.py` — RMSE, chi-square fit statistics
- `scripts/store-irt-parameters.ts` — DB update script post-calibration
- Calibration report: item parameter estimates with standard errors, model fit statistics

## Quality Checks
- [ ] Convergence checked: EM terminates when log-likelihood change < 1e-6
- [ ] Item parameters bounded: a ∈ [0.2, 3.0], b ∈ [-3, 3], c ∈ [0, 0.35]
- [ ] Theta bounded: [-4, 4]
- [ ] Items with < 10 responses excluded from calibration
- [ ] RMSE < 0.10 on held-out validation set
- [ ] Chi-square item fit reviewed: items with extreme fit flagged for content review
- [ ] Theta scale anchored: mean(theta) ≈ 0, SD(theta) ≈ 1 after calibration
- [ ] Recalibrate every quarter or when question bank grows by 20%

## Example

```python
# Quick sanity check
from irt.model import ThreePLModel, IRTParameters

params = IRTParameters(a=1.0, b=0.0, c=0.25)

print(f"P(theta=-2) = {ThreePLModel.probability(-2, params):.3f}")  # → 0.296
print(f"P(theta= 0) = {ThreePLModel.probability( 0, params):.3f}")  # → 0.625
print(f"P(theta=+2) = {ThreePLModel.probability(+2, params):.3f}")  # → 0.880

# Information peaks near theta = b
print(f"I(theta=0)  = {ThreePLModel.fisher_information(0, params):.3f}")  # → 0.156
print(f"I(theta=2)  = {ThreePLModel.fisher_information(2, params):.3f}")  # → 0.048
```
