# Skill: evaluate-tech-stack

## Purpose

Systematically evaluate a technology choice (library, framework, service, infrastructure tool) before adopting it into the AceQuest codebase. Prevents premature adoption of the wrong tool, documents the trade-off analysis, and feeds directly into an ADR (Architecture Decision Record) when the choice is significant.

Use this skill when:
- Considering a new dependency that wasn't in the original tech stack
- Choosing between two viable alternatives for a new feature
- Re-evaluating an existing tool that is causing pain
- A team member proposes replacing something ("should we switch from X to Y?")

Do not use this skill for:
- Trivial package choices (icon packs, date formatting utilities with no architectural impact)
- Decisions already captured in an accepted ADR

## Used By

Software Architect Agent

## Inputs

| Input | Type | Description |
| --- | --- | --- |
| `decision_question` | string | The question being answered, e.g. "Which state management library should we use for the student game session?" |
| `context` | string | What feature or problem is driving the evaluation |
| `options` | list | 2–4 candidate tools/libraries/services to compare |
| `evaluation_criteria` | list | Factors that matter for AceQuest (see standard criteria below) |

## Standard Evaluation Criteria for AceQuest

Always include these unless clearly not relevant:

| Criterion | Why it matters |
| --- | --- |
| **TypeScript support** | AceQuest codebase is 100% TypeScript — first-class types required |
| **Next.js 14 App Router compatibility** | Must work with RSC, server actions, edge runtime where applicable |
| **Bundle size / performance impact** | Student-facing pages must load fast on low-bandwidth Indian networks |
| **Learning curve / team familiarity** | Small team — cannot afford deep learning curves on auxiliary tools |
| **Community & ecosystem maturity** | Avoid tools with <1K GitHub stars or abandoned maintenance |
| **Licence** | Must be MIT or Apache 2.0 — no GPL for production use |
| **Cost** | Prefer free tiers or predictable per-unit pricing |
| **Indian infrastructure compatibility** | Works with AWS ap-south-1 / Supabase / Vercel |

Add domain-specific criteria depending on the question (e.g. offline support, real-time capability, GDPR/DPDP compliance).

## Procedure

### Step 1 — Frame the Decision

Write 2–3 sentences answering:
- What problem are we solving?
- What would happen if we did nothing (current state)?
- Is this decision reversible, or will it create significant lock-in?

### Step 2 — Research Each Option

For each candidate tool, gather:

```
Tool: [Name + version]
Purpose: [What it does in one sentence]
GitHub Stars: [number, as of date]
Last Release: [date]
Licence: [MIT / Apache / etc]
Weekly Downloads (npm): [number]
Used by: [notable Indian or global ed-tech companies if known]
Known issues: [common complaints from community]
```

### Step 3 — Score Each Option

Rate each option across all evaluation criteria on a 3-point scale:

| Rating | Meaning |
| --- | --- |
| ✅ | Strong fit — meets or exceeds the criterion |
| ⚠️ | Acceptable — partially meets it, with caveats |
| ❌ | Poor fit — fails or significantly falls short |

Fill a comparison table:

```
| Criterion              | Option A | Option B | Option C |
|------------------------|----------|----------|----------|
| TypeScript support     |          |          |          |
| App Router compat      |          |          |          |
| Bundle size            |          |          |          |
| Team familiarity       |          |          |          |
| Community maturity     |          |          |          |
| Licence                |          |          |          |
| Cost                   |          |          |          |
| [Domain criterion 1]   |          |          |          |
| [Domain criterion 2]   |          |          |          |
| **Score (✅ count)**   |          |          |          |
```

### Step 4 — Build a Spike (Optional but Recommended)

If the decision is non-trivial, build a minimal spike — a throwaway proof-of-concept that tests the riskiest assumption about the leading option.

```
Spike scope: [what you will build — e.g. "Add auth middleware to a single API route"]
Time-box: [max 2 hours]
Success condition: [what you need to prove — e.g. "Token refresh works without page reload"]
Outcome: [what the spike showed]
```

### Step 5 — Recommend and Document

Write the recommendation:

```markdown
## Recommendation

**Adopt:** [Tool Name] vX.X

**Rationale:** [2–3 sentences tying the choice back to AceQuest's specific context and the highest-priority criteria.]

**Conditions:** [Any conditions on the adoption — e.g. "provided we keep bundle size below 50KB", "monitor cold start times after deployment", "re-evaluate if pricing changes"]

**Next step:** Create ADR `NNNN-[decision-title].md` using the create-adr skill.
```

---

## Output

A structured evaluation document (can be a section in an ADR draft or a standalone Markdown file):

```
/docs/decisions/drafts/[kebab-case-topic]-evaluation.md
```

Or, if proceeding directly to ADR, the evaluation feeds into the Options Considered and Comparison Table sections of the ADR template.

---

## Quality Checks

- [ ] At least 2 options compared (never evaluate only 1 candidate)
- [ ] All standard AceQuest criteria are scored, even if rated ✅ for all options
- [ ] Community maturity checked: GitHub stars, last release date, npm downloads recorded
- [ ] Licence verified — no GPL in production dependencies
- [ ] If a spike was recommended, it was time-boxed and the outcome is recorded
- [ ] Recommendation is specific ("use X") not vague ("X or Y are both fine")
- [ ] If the decision is reversible in <1 week of effort, note it — saves over-engineering

---

## Example

**Decision question:** Which animation library should we use for the game reward screen (coin burst, level-up animation)?

**Context:** The student game session completes and we want a celebratory animation. The screen must work on mid-range Android phones common in Tier 2/3 Indian cities.

**Options:** Framer Motion, GSAP, CSS animations (native)

| Criterion | Framer Motion | GSAP | CSS Animations |
| --- | --- | --- | --- |
| TypeScript support | ✅ | ✅ | ✅ |
| App Router compat | ✅ | ⚠️ SSR needs wrapper | ✅ |
| Bundle size | ⚠️ ~150KB | ⚠️ ~80KB | ✅ 0KB |
| Team familiarity | ✅ | ⚠️ | ✅ |
| Community maturity | ✅ | ✅ | ✅ |
| Licence | ✅ MIT | ⚠️ Free tier only | ✅ |
| Cost | ✅ Free | ⚠️ Commercial licence for SaaS | ✅ |
| Mobile performance (mid-range Android) | ⚠️ JS-driven | ✅ GPU-accelerated | ✅ GPU-accelerated |
| **Score (✅ count)** | **5** | **4** | **7** |

**Recommendation:** Use CSS animations (native) for the reward screen. They have zero bundle cost, run on the GPU (critical for mid-range Android), and the team is already familiar. Reserve Framer Motion for complex interactive transitions where it already adds value (page transitions), rather than pulling it in for a one-off particle effect. If CSS proves insufficient for a specific animation, spike Framer Motion for that single component.

**Next step:** No ADR needed — this is a reversible, low-impact choice. Document in component comments.
