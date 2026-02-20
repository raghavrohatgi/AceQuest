# Skill: revise-question

## Purpose
Take a question that failed `ai-qa-review` and revise it based on the specific failure reason. Called by the SME agent that originally generated the question. Maximum 2 revision rounds per question — if it fails again, reject it.

## Used By
- All SME agents (after receiving NEEDS_REVISION from `ai-qa-review`)

## Inputs

| Input | Type | Description |
| --- | --- | --- |
| `question` | object | The original question JSON object |
| `revision_note` | string | Specific failure reason from `ai-qa-review` (the `revision_note` field) |
| `checks_failed` | array | List of check names that failed (e.g. `["MISCONCEPTION_NAMED", "EXPLANATION_TEACHES"]`) |
| `agent_identity` | string | Which SME agent is revising |
| `chapter_context` | string | Chapter title and concept for reference |

## Prompt

```
You are the {agent_identity} for AceQuest.

A question you generated has failed QA review and needs revision.

ORIGINAL QUESTION:
{question_json}

QA FAILURE REASON:
{revision_note}

CHECKS THAT FAILED:
{checks_failed}

CHAPTER CONTEXT: {chapter_title}, Concept: {concept_tag}

YOUR TASK:
Revise ONLY the aspects that failed the QA checks. Do not change:
- The concept being tested
- The question type (MCQ/FITB/Match)
- The bloom_level (unless BLOOM_ACCURATE failed — then fix it)
- The difficulty level

Specific guidance per failed check:

[If FACTUAL_ACCURACY failed]
The correct answer or question contains a factual error. Fix it so it aligns with NCERT/CBSE content.

[If DISTRACTORS_WRONG failed]
One or more wrong options could also be correct. Make all wrong options definitively incorrect.

[If MISCONCEPTION_NAMED failed]
The distractor_rationale fields are too generic. For each wrong option, name the exact error a student makes when they pick it.
Example of BAD: "Student may be confused"
Example of GOOD: "Student confuses the formula for area with perimeter, using length+breadth instead of length×breadth"

[If DISTRACTORS_PLAUSIBLE failed]
Some wrong options are obviously silly. Replace them with options that a student who partially understands the concept might genuinely choose.

[If SINGLE_CORRECT failed]
More than one option could be correct. Revise so there is exactly one unambiguous correct answer.

[If BLOOM_ACCURATE failed]
The bloom_level is mislabelled. Change it to: {bloom_level_correction}

[If AGE_APPROPRIATE failed]
The language is not suitable for Grade {grade}. Simplify vocabulary and sentence structure.

[If UNAMBIGUOUS failed]
The question can be interpreted in multiple ways. Rewrite the stem to have only one clear meaning.

[If EXPLANATION_TEACHES failed]
The explanation just restates the answer. Rewrite to explain WHY the correct answer is right AND why each wrong option is wrong (for MCQ).

[If IS_ORIGINAL failed]
This question too closely resembles an NCERT exercise. Change the numbers, names, or scenario while keeping the same concept tested.

Return the revised question as a single JSON object in the same schema. Set "version" to {current_version + 1}.
```

## Output

A revised question object with:
- `version` incremented by 1
- `status: "draft"` (will go back through `ai-qa-review`)
- `review_notes` updated to include the revision history

```json
{
  "id": "sci-6-ch4-mcq-007",
  "version": 2,
  "status": "draft",
  "review_notes": "v1 failed: MISCONCEPTION_NAMED. Revised distractor rationales to name specific errors.",
  ...
}
```

## Quality Checks

- [ ] Only the failing aspects were changed — concept, type, difficulty unchanged
- [ ] `version` was incremented
- [ ] `review_notes` documents what was changed
- [ ] Revised question is sent back through `ai-qa-review` before human review

## Notes
- Maximum 2 revision rounds. If a question fails QA twice, reject it (`status: "rejected"`) and log the failure pattern to improve the `generate-questions` prompt.
- If the same check keeps failing across multiple questions in a batch, it signals a systematic issue with the SME agent prompt — update the prompt, don't just keep revising individual questions.
