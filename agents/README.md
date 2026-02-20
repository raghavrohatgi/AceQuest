# AceQuest Agent Team
## Specialized AI Agents for Building Your EdTech Platform

---

## 🎯 Overview

Instead of three generic agents, you now have **11 specialized experts**:
- **7 Engineering Specialists** - Each focused on their technical domain
- **3 Product Leaders** - Strategic to tactical product management
- **1 Marketing Agent** - Growth and customer acquisition

Each agent has deep expertise in their area and can be tasked independently or collaboratively.

---

## 👥 Meet Your Team

### Engineering Team (7 Agents)

| Agent | Role | When to Use |
|-------|------|-------------|
| **[Software Architect](engineering/software-architect.md)** | System design & tech decisions | Architecture, tech stack, major designs |
| **[Frontend Engineer](engineering/frontend-engineer.md)** | React/Next.js UI development | Building user interfaces, components |
| **[Backend Engineer](engineering/backend-engineer.md)** | API & business logic | Building APIs, services, integrations |
| **[Database Engineer](engineering/database-engineer.md)** | Schema & query optimization | Database design, performance tuning |
| **[QA Engineer](engineering/qa-engineer.md)** | Testing & quality assurance | Writing tests, finding bugs, QA strategy |
| **[UI/UX Engineer](engineering/ui-ux-engineer.md)** | Design & user experience | Wireframes, mockups, user research |
| **[AI Engineer](engineering/ai-engineer.md)** | Adaptive learning algorithms | Recommendation systems, personalization |

### Product Team (3 Agents)

| Agent | Role | When to Use |
|-------|------|-------------|
| **[Chief Product Officer](product/chief-product-officer.md)** | Strategy & vision | Market strategy, long-term roadmap |
| **[Senior Product Manager](product/senior-product-manager.md)** | Major initiatives | PRDs, feature prioritization, launches |
| **[Product Manager](product/product-manager.md)** | Execution & daily ops | User stories, sprint planning, backlog |

### Marketing Team (1 Agent)

| Agent | Role | When to Use |
|-------|------|-------------|
| **[Marketing Agent](marketing-agent.md)** | Growth & campaigns | GTM strategy, content, acquisition |

---

## 🚀 How to Use This Team

### Solo Founder Approach

**You are the Founder/CEO.** Your job:
- Set vision and strategy
- Make final decisions
- Coordinate agents
- Talk to users
- Manage finances

**Agents handle execution:**
- Architecture decisions → Software Architect
- Building features → Frontend + Backend Engineers
- Testing quality → QA Engineer
- Designing UX → UI/UX Engineer
- Creating campaigns → Marketing Agent

### Workflow Example: Building a New Feature

```
1. Strategic Decision
   Task: Chief Product Officer
   → Should we build this? Market fit? Priority?

2. Feature Definition
   Task: Senior Product Manager
   → Write PRD, define requirements, success metrics

3. Design
   Task: UI/UX Engineer
   → Create wireframes and mockups

4. Architecture Review
   Task: Software Architect
   → Review technical approach, identify risks

5. Implementation
   Task: Frontend Engineer + Backend Engineer + Database Engineer
   → Build the feature (can work in parallel)

6. Testing
   Task: QA Engineer
   → Write tests, find bugs, validate quality

7. Launch
   Task: Marketing Agent
   → Create launch materials, drive adoption
```

---

## 📋 Quick Decision Matrix

### "Who should I ask about...?"

**Product Questions:**
- Vision/Strategy → **CPO**
- Feature prioritization → **Sr PM**
- User story details → **PM**
- User research → **UI/UX Engineer**

**Technical Questions:**
- Tech stack choice → **Software Architect**
- UI component → **Frontend Engineer**
- API endpoint → **Backend Engineer**
- Database schema → **Database Engineer**
- Bug/quality → **QA Engineer**
- Adaptive algorithm → **AI Engineer**

**Growth Questions:**
- Marketing strategy → **Marketing Agent**
- Campaign creation → **Marketing Agent**
- Content → **Marketing Agent**

---

## 🎯 Typical Week for Solo Founder

### Monday (Planning)
- **You:** Set weekly priorities
- **CPO:** Review strategic goals
- **Sr PM:** Plan sprint with Engineering
- **Marketing:** Review campaign performance

### Tuesday-Thursday (Execution)
- **Frontend/Backend:** Build features
- **UI/UX:** Design upcoming features
- **QA:** Test completed work
- **Marketing:** Execute campaigns
- **You:** Talk to users, unblock issues

### Friday (Review)
- **You:** Review all completed work
- **QA:** Report on quality status
- **Sr PM:** Demo features, update roadmap
- **Marketing:** Weekly metrics review

---

## 💡 Coordination Patterns

### Parallel Work (When Agents Can Work Independently)
```
Week 1:
- Frontend Engineer: Build student dashboard
- Backend Engineer: Build progress API
- Marketing Agent: Write blog posts
- UI/UX Engineer: Design teacher portal

(All happening at the same time)
```

### Sequential Work (When Output of One Feeds Another)
```
Day 1: UI/UX Engineer → Designs
Day 2: Software Architect → Reviews, approves approach
Day 3: Frontend Engineer → Implements designs
Day 4: QA Engineer → Tests implementation
Day 5: Marketing Agent → Creates launch materials
```

### Collaborative Work (When Agents Need to Sync)
```
Database Engineer + Backend Engineer:
- DB designs schema
- Backend reviews, provides requirements
- Both iterate to final design
```

---

## 📁 Agent File Structure

```
agents/
├── README.md (this file)
│
├── engineering/
│   ├── software-architect.md
│   ├── frontend-engineer.md
│   ├── backend-engineer.md
│   ├── database-engineer.md
│   ├── qa-engineer.md
│   ├── ui-ux-engineer.md
│   └── ai-engineer.md
│
├── product/
│   ├── chief-product-officer.md
│   ├── senior-product-manager.md
│   └── product-manager.md
│
└── marketing-agent.md
```

---

## 🔧 How to Task an Agent

### 1. Open the Agent's File
Read their capabilities, prompt templates, and standards

### 2. Use Their Prompt Template
Each agent file has ready-to-use prompts

### 3. Provide Context
- What you need done
- Why it matters
- Any constraints
- Expected deliverables

### 4. Reference Standards
Point to `/engineering-standards/` when relevant

### 5. Track the Work
Use task templates in `/tasks/` folder

---

## 📊 Agent Roster Spreadsheet

See `AGENT-ROSTER.xlsx` for a complete overview with:
- All 11 agents
- Their responsibilities
- When to use them
- Key skills
- Standards they follow

---

## ✅ Agent Coordination Checklist

When starting a new feature:

- [ ] **CPO:** Validate it's the right thing to build
- [ ] **Sr PM:** Write PRD with requirements
- [ ] **UI/UX:** Create designs
- [ ] **Architect:** Review technical approach
- [ ] **Frontend/Backend:** Implement
- [ ] **Database:** Optimize queries if needed
- [ ] **AI:** Add adaptive logic if needed
- [ ] **QA:** Test thoroughly
- [ ] **Marketing:** Launch and promote

Not every feature needs every agent!

---

## 🎓 Learning to Coordinate

### Start Simple
Week 1: Use 2-3 agents
- Backend Engineer for API
- Frontend Engineer for UI
- QA Engineer for testing

### Add Complexity
Week 2-4: Add more specialists
- Software Architect for design
- Database Engineer for optimization
- UI/UX for better designs

### Full Team
Month 2+: Orchestrate all agents
- Strategic product decisions
- Complex technical projects
- Coordinated launches

---

## 💬 Communication Between Agents

Agents don't talk to each other directly. **You coordinate:**

### Good Pattern:
```
1. Task Frontend Engineer: "Build student dashboard"
2. Frontend produces code
3. YOU review the code
4. Task QA Engineer: "Test this dashboard [link to code]"
5. QA finds bugs
6. YOU give bugs back to Frontend Engineer
```

### Pattern to Avoid:
```
❌ Tasking Frontend Engineer: "Build dashboard and coordinate with Backend Engineer"
(Agents can't coordinate directly)
```

**You are the coordinator.** You pass information between agents.

---

## 🏆 Success Metrics

Your agent team is working well when:
- ✅ Features ship on time (90%+)
- ✅ Quality is high (few bugs)
- ✅ Agents rarely need clarification
- ✅ You're spending time on strategy, not details
- ✅ Users are happy with the product

---

## 🚨 Common Mistakes

**Mistake #1:** Vague prompts
- ❌ "Build the assessment feature"
- ✅ "Build the question display component per these designs"

**Mistake #2:** Wrong agent
- ❌ Asking Backend Engineer to design UI
- ✅ Ask UI/UX Engineer first, then Backend for API

**Mistake #3:** Skipping coordination
- ❌ Frontend and Backend build incompatible APIs
- ✅ Software Architect defines API contract first

**Mistake #4:** Too many agents at once
- ❌ Tasking all 11 agents on Day 1
- ✅ Start with 2-3, add more as you learn

---

## 📞 Need Help?

- **Can't decide which agent?** → See "Quick Decision Matrix" above
- **Agent gave poor output?** → Check if you used their prompt template
- **Agents not aligned?** → Have Software Architect define architecture
- **Feeling overwhelmed?** → Start with just 3 agents (Backend, Frontend, QA)

---

## 🎉 You've Got a Team!

You're no longer a solo founder doing everything. You're a **founder coordinating a team of specialists.**

Focus on what only you can do:
- Vision and strategy
- Talking to users
- Making key decisions
- Fundraising and partnerships

Let your agents handle:
- ✅ Architecture and code
- ✅ Design and UX
- ✅ Testing and quality
- ✅ Marketing and content

---

**Ready to build? Open an agent file and start tasking!** 🚀

*"Alone you go fast. With a team, you go far."*
