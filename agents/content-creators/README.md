# Subject Matter Expert (SME) Agents
## Content Creation Team for AceQuest

---

## 📚 Overview

These specialized agents create high-quality, curriculum-aligned educational content for AceQuest. All content follows **CBSE Board** curriculum and **NCERT syllabus** for Indian students.

---

## 👨‍🏫 SME Team (12 Agents)

### Mathematics Teachers (4 Agents)

| Agent | Grades | Age | Key Topics |
|-------|--------|-----|------------|
| **[Math Teacher 1-3](math/math-teacher-grades-1-3.md)** | 1-3 | 6-9 yrs | Numbers, basic operations, shapes, measurement |
| **[Math Teacher 4-5](math/math-teacher-grades-4-5.md)** | 4-5 | 9-11 yrs | Large numbers, fractions, decimals, geometry |
| **[Math Teacher 6-8](math/math-teacher-grades-6-8.md)** | 6-8 | 11-14 yrs | Algebra, integers, geometry, data handling |
| **[Math Teacher 9-10](math/math-teacher-grades-9-10.md)** | 9-10 | 14-16 yrs | Advanced algebra, trigonometry, board prep |

### English Teachers (4 Agents)

| Agent | Grades | Age | Key Topics |
|-------|--------|-----|------------|
| **[English Teacher 1-3](english/english-teacher-grades-1-3.md)** | 1-3 | 6-9 yrs | Alphabet, phonics, simple grammar, stories |
| **[English Teacher 4-5](english/english-teacher-grades-4-5.md)** | 4-5 | 9-11 yrs | Grammar, comprehension, creative writing |
| **[English Teacher 6-8](english/english-teacher-grades-6-8.md)** | 6-8 | 11-14 yrs | Literature, advanced grammar, formal writing |
| **[English Teacher 9-10](english/english-teacher-grades-9-10.md)** | 9-10 | 14-16 yrs | Board exam English, literature analysis |

### Science Teachers (4 Agents)

| Agent | Grades | Age | Key Topics |
|-------|--------|-----|------------|
| **[Science Teacher 1-3](science/science-teacher-grades-1-3.md)** | 1-3 | 6-9 yrs | EVS, living things, environment, health |
| **[Science Teacher 4-5](science/science-teacher-grades-4-5.md)** | 4-5 | 9-11 yrs | Plants, animals, matter, natural phenomena |
| **[Science Teacher 6-8](science/science-teacher-grades-6-8.md)** | 6-8 | 11-14 yrs | Physics, chemistry, biology basics |
| **[Science Teacher 9-10](science/science-teacher-grades-9-10.md)** | 9-10 | 14-16 yrs | Board exam science (PCB), practicals |

---

## 🎯 What SME Agents Do

### Content Creation
- Write assessment questions (MCQ, short answer, long answer)
- Create word problems with Indian context
- Design diagram-based questions
- Develop case studies
- Write explanations and solutions

### Quality Assurance
- Ensure 100% NCERT alignment
- Verify accuracy of content
- Check age-appropriateness
- Maintain curriculum standards
- Follow CBSE exam patterns

### Pedagogical Excellence
- Design questions that test understanding (not just recall)
- Create distractors that reveal common misconceptions
- Write encouraging, clear explanations
- Use culturally relevant contexts
- Build progression across difficulty levels

---

## 📋 How to Use SME Agents

### Step 1: Choose the Right Agent
Based on:
- **Subject:** Math, English, or Science
- **Grade Level:** Match the student's grade
- **Topic:** Refer to agent's curriculum expertise

### Step 2: Task the Agent

```
You are the [Math/English/Science] Teacher for Grades [X-Y].

TASK: Create [number] questions on [topic]

SPECIFICATIONS:
- Grade: [Specific grade]
- Topic: [NCERT chapter/topic]
- Difficulty: [Easy/Medium/Hard or distribution]
- Question Type: [MCQ/Short answer/Long answer]

NCERT ALIGNMENT:
- Textbook: [Book name]
- Chapter: [Chapter number and name]
- Learning Outcome: [What students should learn]

REQUIREMENTS:
1. Follow CBSE/NCERT curriculum exactly
2. Use age-appropriate language
3. Indian context (names, situations, culture)
4. Clear, unambiguous questions
5. Accurate answers with explanations
6. Mark common misconceptions

DELIVERABLES:
[JSON format with question details - see agent file]
```

### Step 3: Review Content
- Check curriculum alignment
- Verify accuracy
- Test age-appropriateness
- Review Indian context relevance

---

## 🇮🇳 Indian Context Guidelines

### Names
Use common Indian names representing diversity:
- **Boys:** Rohan, Arjun, Aarav, Ravi, Karan, Aditya, Amit
- **Girls:** Priya, Ananya, Riya, Meera, Diya, Kavya, Sneha

### Contexts
- **Currency:** Rupees (₹), paise
- **Festivals:** Diwali, Holi, Eid, Pongal, Onam, Christmas
- **Food:** Ladoos, samosas, dosas, parathas, mangoes
- **Sports:** Cricket, badminton, kabaddi, kho-kho
- **Places:** Local markets, schools, temples, parks

### Cultural Sensitivity
- Inclusive of all religions
- Diverse regional representation
- Gender-neutral where possible
- Urban and rural contexts
- Secular and respectful

---

## 📊 Content Quality Standards

### Accuracy (100% Required)
- Mathematically/scientifically correct
- Grammatically correct
- No ambiguity in questions
- Verified answers and explanations

### NCERT Alignment (100% Required)
- Matches learning outcomes
- Covers specified chapters
- Uses NCERT terminology
- Follows progression

### Age-Appropriateness
- Language complexity suitable for grade
- Concepts at appropriate level
- Familiar contexts and examples
- Engaging but educational

### Pedagogical Quality
- Tests understanding, not just recall
- Distractors represent real misconceptions
- Explanations aid learning
- Difficulty progression logical

---

## 📁 Question Format (JSON)

```json
{
  "question_text": "Clear, complete question",
  "question_type": "mcq/fill_blank/short_answer/long_answer/true_false",
  "options": ["A", "B", "C", "D"],
  "correct_answer": "B" or "text answer",
  "explanation": "Student-friendly explanation",
  "difficulty": "easy/medium/hard",
  "subject": "math/english/science",
  "topic": "Specific NCERT topic",
  "grade": 1-10,
  "ncert_chapter": "Chapter name",
  "learning_objective": "What this tests",
  "common_mistakes": ["Misconception 1", "Misconception 2"],
  "marks": 1-5,
  "time_estimate": 30,
  "tags": ["keyword1", "keyword2"],
  "indian_context": true/false
}
```

---

## 🎓 Content Creation Workflow

```
1. Product Manager
   → Defines content needs (grade, subject, topic, quantity)

2. SME Agent
   → Creates questions per specifications
   → Follows NCERT curriculum
   → Uses proper format

3. QA Review
   → Checks accuracy
   → Verifies NCERT alignment
   → Tests age-appropriateness

4. Database
   → Questions imported
   → Tagged appropriately
   → Ready for assessments

5. AI Engineer
   → Assigns difficulty ratings
   → Maps to skills
   → Enables adaptive selection
```

---

## ✅ Quality Checklist

Before finalizing content:

**Curriculum Alignment**
- [ ] Matches NCERT chapter and learning outcomes
- [ ] Appropriate for specified grade level
- [ ] Follows CBSE guidelines
- [ ] Uses correct terminology from NCERT

**Content Quality**
- [ ] Question is clear and unambiguous
- [ ] Answer is 100% correct
- [ ] Explanation is student-friendly
- [ ] Difficulty level appropriate

**Context & Language**
- [ ] Age-appropriate vocabulary
- [ ] Indian names and contexts
- [ ] Culturally sensitive
- [ ] Gender-neutral where possible

**Pedagogy**
- [ ] Tests understanding, not just recall
- [ ] Distractors represent real errors
- [ ] Explanation aids learning
- [ ] Difficulty matches grade level

---

## 📈 Success Metrics

### Content Quality
- Accuracy: 100%
- NCERT alignment: 100%
- Age-appropriateness: Pass by educators

### Student Performance
- Engagement: 75%+ completion rate
- Learning: 15%+ improvement in scores
- Satisfaction: NPS 60+ from parents/teachers

### Operational
- Content delivery: On time, on spec
- Review pass rate: 90%+ first time
- Coverage: All NCERT chapters mapped

---

## 🤝 Collaboration

### SME Agents Work With:

**Product Team:**
- **Sr PM:** Defines content requirements
- **PM:** Specifies topics and quantities

**Engineering Team:**
- **Database Engineer:** Schema for question storage
- **AI Engineer:** Difficulty and skill tagging
- **QA Engineer:** Content quality review

**Other SMEs:**
- Cross-grade coordination for progression
- Cross-subject coordination for integration

---

## 📚 NCERT Textbooks Reference

### Mathematics
- **Grades 1-5:** Math-Magic
- **Grades 6-8:** Mathematics (NCERT)
- **Grades 9-10:** Mathematics (NCERT)

### English
- **Grades 1-3:** Marigold
- **Grades 4-5:** Marigold
- **Grades 6:** Honeysuckle & A Pact with the Sun
- **Grade 7:** Honeycomb & An Alien Hand
- **Grade 8:** Honeydew & It So Happened
- **Grade 9:** Beehive & Moments
- **Grade 10:** First Flight & Footprints Without Feet

### Science
- **Grades 1-5:** Looking Around (EVS)
- **Grades 6-10:** Science (NCERT)

---

## 🔄 Content Updates

### Regular Reviews
- Quarterly review of content accuracy
- Annual NCERT syllabus updates
- Ongoing CBSE pattern changes
- Student performance analysis

### Continuous Improvement
- Analyze question performance
- Update based on feedback
- Refine difficulty levels
- Expand question bank

---

## 💡 Tips for Quality Content

### For Younger Grades (1-5)
- Use simple, everyday language
- Include pictures or visual descriptions
- Make math relatable (toys, fruits, family)
- Keep instructions clear and short

### For Middle Grades (6-8)
- Increase complexity gradually
- Connect to real-world applications
- Develop critical thinking
- Prepare for board exam patterns

### For Board Grades (9-10)
- Follow exact CBSE pattern
- Include marking schemes
- Cover all important topics
- Practice with variety of question types

---

## 🚀 Ready to Create Content?

1. **Choose your SME agent** based on subject and grade
2. **Open their agent file** for detailed guidance
3. **Use their prompt template** for consistent quality
4. **Review against standards** before finalizing
5. **Import to question bank** and tag appropriately

---

**Remember: Quality content is the foundation of effective learning. Every question should help a child learn, not just test them.**

*Building AceQuest, one great question at a time!* 📝✨
