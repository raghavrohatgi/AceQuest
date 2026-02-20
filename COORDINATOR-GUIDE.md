# Agentic Framework Coordinator Guide
## How to Orchestrate AI Agents as a Solo Founder

---

## Overview

As a solo founder, you act as the **Founder-Coordinator** who orchestrates three specialized AI agents:
- **Engineering Agent:** Builds the technical platform
- **Product Agent:** Defines what to build and designs user experience
- **Marketing Agent:** Drives growth and customer acquisition

This guide shows you how to effectively delegate work to these agents and coordinate their efforts.

---

## Your Role as Founder-Coordinator

### What You Do
✅ Set strategic vision and business goals
✅ Make final decisions on priorities and budget
✅ Coordinate agents to work together
✅ Provide business context and constraints
✅ Review and approve agent outputs
✅ Talk to users and gather real-world feedback
✅ Manage finances and fundraising
✅ Handle legal and compliance matters

### What You DON'T Do
❌ Write all the code yourself
❌ Create every design from scratch
❌ Write every marketing email
❌ Do every tactical task

**Key Principle:** You leverage AI agents for execution while you focus on strategy, coordination, and the human elements (user conversations, fundraising, etc.).

---

## The Agent Orchestra: How They Work Together

```
YOU (Conductor)
    ↓
    ├── PRODUCT AGENT → Creates requirements → ENGINEERING AGENT → Builds features
    │                                              ↓
    └── MARKETING AGENT ← Receives features to market ←┘
```

### Typical Workflow

1. **You** identify a business goal (e.g., "We need 500 student signups")
2. **Product Agent** researches and proposes features to achieve goal
3. **Engineering Agent** estimates effort and builds features
4. **Marketing Agent** creates campaigns to drive signups
5. **You** review progress, make adjustments, talk to users

---

## How to Task Each Agent

### General Tasking Pattern

1. **Open conversation with agent identity**
   ```
   "You are the [Engineering/Product/Marketing] Agent for my AceQuest..."
   ```

2. **Provide context**
   - What's the goal?
   - Why does this matter?
   - What are the constraints?

3. **Be specific about deliverables**
   - What exactly do you need?
   - In what format?
   - By when?

4. **Include relevant information**
   - Link to related work
   - Previous decisions
   - User feedback

5. **Request clarifying questions**
   - "What questions do you have?"
   - "What else do you need to know?"

### Example: Tasking Product Agent
```
You are the Product Agent for my AceQuest.

TASK: Define the assessment-taking experience for students in grades 3-5.

CONTEXT:
- This is our MVP core feature
- Users: 8-10 year old students
- Goal: Make assessments engaging, not stressful
- Must support multiple choice, true/false questions
- Need to work on tablets and laptops

CONSTRAINTS:
- COPPA compliant (no data collection without parent consent)
- Budget: Small startup, simple solutions preferred
- Timeline: Need spec in 2 weeks for development

DELIVERABLES:
1. User flow diagram
2. Wireframes (low-fi is fine)
3. User stories for engineering
4. Success metrics

What questions do you have?
```

---

## Weekly Coordination Rhythm

### Monday: Planning
- Review last week's progress
- Set this week's priorities
- Task each agent with weekly goals
- Align on dependencies

### Daily: Async Check-ins
- Check agent progress via chat
- Answer questions
- Unblock issues
- Make small decisions

### Wednesday: Mid-week Sync
- Review work-in-progress
- Adjust priorities if needed
- Ensure agents are aligned
- Address any blockers

### Friday: Review & Next Steps
- Review completed work
- Approve or request revisions
- Plan next week
- Celebrate wins

---

## Cross-Agent Coordination

### When Product & Engineering Need to Collaborate

**Scenario:** Product has feature idea, needs engineering feasibility check

```
Step 1: Task Product Agent
"Create a spec for [feature]"

Step 2: Share Product spec with Engineering Agent
"You are the Engineering Agent. Review this spec from Product Agent:
[paste spec]

Questions:
1. Is this technically feasible?
2. How long would this take?
3. What are the technical risks?
4. Any alternative approaches?"

Step 3: Share Engineering feedback with Product Agent
"You are the Product Agent. Engineering provided this feedback:
[paste feedback]

Please revise the spec considering this input."
```

### When Marketing Needs Product Info

**Scenario:** Marketing wants to promote a new feature

```
Step 1: Get feature details from Product
"You are the Product Agent. Marketing needs to promote the new
gamification feature. Provide:
1. Key benefits for students and parents
2. How it works (simple explanation)
3. Competitive advantages
4. Screenshots or mockups
5. Success metrics we can reference"

Step 2: Task Marketing with Product info
"You are the Marketing Agent. We're launching this feature:
[paste Product info]

Create:
1. Social media announcement posts
2. Email to parents
3. Landing page copy
4. Blog post

Target: Parents of students grades 3-8
Tone: Exciting but trustworthy"
```

---

## Decision-Making Framework

### You Decide (Always):
- Strategic direction and pivots
- Budget allocation and spending limits
- Hiring decisions
- Pricing and business model
- Major partnerships
- Fundraising strategy
- What to build next (high-level)

### Product Agent Decides:
- Feature prioritization within roadmap
- UX/UI design
- User research methods
- Success metrics for features
- Release timing

### Engineering Agent Decides:
- Technical implementation
- Architecture and tech stack
- DevOps and infrastructure
- Development estimates
- Technical debt priorities

### Marketing Agent Decides:
- Marketing channel mix
- Campaign creative and copy
- Content calendar
- Social media strategy
- Ad targeting (within budget)

### Collaborative Decisions:
- Go-to-market timing (You + Marketing + Product)
- Feature scope (You + Product + Engineering)
- Major technical investments (You + Engineering)
- Target market changes (You + Product + Marketing)

---

## Managing Agent Work Products

### File Organization

```
/your-startup
  /agents
    - engineering-agent.md (agent definitions)
    - product-agent.md
    - marketing-agent.md
  /tasks
    - task-001-assessment-engine.md (active tasks)
    - task-002-landing-page.md
  /outputs
    /engineering
      - /code (actual codebase)
      - /docs (technical docs)
    /product
      - /requirements (PRDs, specs)
      - /designs (wireframes, mockups)
      - /research (user research)
    /marketing
      - /campaigns
      - /content
      - /analytics
  /context
    - company-profile.md
    - product-roadmap.md
    - user-personas.md
    - meeting-notes.md
```

### Task Tracking Template

Create a markdown file for each major task:

```markdown
# Task: [Task Name]

**Status:** In Progress / Blocked / Done
**Priority:** P0 / P1 / P2
**Owner:** Engineering / Product / Marketing / Coordination
**Due Date:** [Date]

## Context
[Why we're doing this]

## Goal
[What success looks like]

## Assigned To
- [ ] Product Agent: [Specific deliverables]
- [ ] Engineering Agent: [Specific deliverables]
- [ ] Marketing Agent: [Specific deliverables]

## Dependencies
[What needs to happen first]

## Progress Log
**[Date]:** [Update]
**[Date]:** [Update]

## Decisions Made
- [Decision 1]
- [Decision 2]

## Next Steps
- [ ] Action 1
- [ ] Action 2
```

---

## Common Scenarios & Solutions

### Scenario 1: Agents Give Different Advice

**Example:** Product wants a complex feature, Engineering says it's too much work, Marketing says users don't care.

**Solution:**
1. Gather all perspectives in writing
2. Identify the core disagreement
3. Define decision criteria (user value, effort, business impact)
4. Make the call based on your strategic priorities
5. Communicate decision and reasoning to all agents

### Scenario 2: You're Overwhelmed

**Solution:**
1. Focus on P0 (must-have) items only
2. Ask Product Agent to ruthlessly prioritize
3. Ask Engineering Agent for MVP version
4. Ask Marketing Agent for one high-impact channel
5. Push everything else to next month

### Scenario 3: Agent Needs Info You Don't Have

**Example:** Engineering needs detailed designs, Product hasn't created them yet.

**Solution:**
1. Task Product Agent with creating needed artifact
2. Set clear deadline
3. Tell Engineering Agent to expect it by [date]
4. Document the dependency

### Scenario 4: Work Quality Isn't Good Enough

**Solution:**
1. Provide specific feedback on what's wrong
2. Give examples of what "good" looks like
3. Ask agent to revise
4. Be clear about quality standards upfront
5. Iterate until it meets standards

---

## Tips for Effective Agent Management

### 1. Be Specific
❌ "We need marketing stuff"
✅ "Create 3 blog posts targeting parents, SEO-optimized, 1000 words each, about helping kids with math anxiety"

### 2. Provide Context
Always explain WHY you need something, not just WHAT.

### 3. Set Clear Deadlines
Agents work better with time constraints.

### 4. Use Templates
The agent definition files contain prompt templates - use them!

### 5. Document Decisions
Keep a decisions log so agents have context.

### 6. Iterate
First draft is rarely perfect. Review and request revisions.

### 7. Batch Similar Work
Task multiple related items at once for consistency.

### 8. Save Good Examples
When an agent produces great work, save it as a reference for future tasks.

### 9. Create Feedback Loops
Share user feedback with agents to improve their outputs.

### 10. Celebrate Wins
Acknowledge good work (even from AI agents - it helps you stay motivated!).

---

## Your First Week with Agents

### Day 1: Setup
- Read all three agent definition files
- Set up folder structure
- Create company profile document
- Define your business goals

### Day 2: Product Planning
- Task Product Agent with creating user personas
- Task Product Agent with drafting MVP features
- Review and provide feedback

### Day 3: Technical Planning
- Share Product's MVP features with Engineering Agent
- Ask for technical architecture proposal
- Ask for effort estimates

### Day 4: Marketing Foundation
- Task Marketing Agent with brand positioning
- Task Marketing Agent with GTM strategy
- Ask for landing page copy

### Day 5: Coordination
- Review all agent outputs
- Create integrated plan
- Identify dependencies
- Make decisions on priorities
- Set next week's goals

---

## Measuring Success

### For Yourself (Founder-Coordinator)
- Are you spending time on high-value activities (strategy, users, fundraising)?
- Are you making decisions quickly (<48 hours)?
- Is the business moving forward each week?
- Do you feel less overwhelmed?

### For Agent System
- Are deliverables high quality?
- Are deadlines being met?
- Are agents staying aligned?
- Is rework rate low (<20%)?
- Are you achieving business goals?

---

## When Things Go Wrong

### Red Flags
- 🚩 Agents constantly need clarification
- 🚩 Deliverables don't meet needs
- 🚩 Work isn't aligned across agents
- 🚩 You're doing all the work anyway
- 🚩 Progress is too slow

### Fixes
1. **Unclear deliverables** → Use specific prompts and templates
2. **Low quality** → Provide examples, raise standards, iterate
3. **Misalignment** → Better coordination, document decisions
4. **You doing everything** → Trust agents more, delegate fully
5. **Slow progress** → Focus on fewer priorities, increase urgency

---

## Advanced: Multi-Agent Projects

For complex projects requiring all three agents:

### 1. Kickoff Meeting (with yourself!)
- Define project goal and success criteria
- Identify what each agent needs to do
- Map dependencies
- Set milestones

### 2. Sequential Tasking
Product → Engineering → Marketing (typical flow)

### 3. Parallel Tasking
When work is independent, task all agents at once

### 4. Integration Points
Schedule moments where agents' work comes together

### 5. Review & Iterate
Check alignment, gather feedback, adjust

---

## Final Thoughts

**Remember:** You're not trying to replace a full team. You're leveraging AI agents to:
- Move faster than you could alone
- Cover multiple disciplines
- Execute on tactics while you focus on strategy
- Scale your impact as a solo founder

**The magic happens when:**
- You provide clear direction
- Agents execute with expertise
- Work flows between agents smoothly
- You focus on what only humans can do

**Start small, learn the system, then scale up.**

You've got this! 🚀
