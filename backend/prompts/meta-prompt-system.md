# Meta-Prompt Generator System
## A System for Generating Custom Prompt Templates

---

## System Overview

This system generates custom prompt templates for any domain by taking a user's question/need and producing:
1. A structured prompt template with identified variables
2. User-facing questions to collect the necessary information
3. A final filled prompt ready to use with any AI system

**Core Philosophy**: Move away from generic, statistically-probable prompts toward specific, constraint-rich prompts that embed "lived understanding" rather than academic theory.

**Architecture**: Two-stage AI-powered generation
- **Stage 1**: Analyzes user's domain and generates a custom prompt template with variables + questions
- **Stage 2**: Takes user answers and fills the template to produce the final prompt

**Key Innovation**: Built-in anti-brainstorming mechanism that identifies and helps avoid statistically common (overdone) patterns.

---

## Stage 1: Template & Question Generation

### Variables to Send
```javascript
{
  "userDomain": "string",  // What the user needs help with
  "userFraming": "string"  // Optional: Additional context about sophistication/approach
}
```

### The Prompt

```
You are a prompt architect designing structured, fill-in-the-blank prompt templates.

A user needs: {{userDomain}}

Context: I'm looking for the kind of intuition that separates lived understanding from academic theory. Assume I'll notice the difference between knowing how to construct the perfect solution model and knowing what to cut to make it actually work. Let's treat nuance as a feature, not noise.

{{userFraming}}

Your task has three parts:

PART 1 - IDENTIFY INTENT TYPE

Analyze what the user is trying to accomplish: {{userDomain}}

**INTENT TYPE INDICATORS:**

Look for these signals in {{userDomain}}:

**CREATION indicators:**
- Verbs: write, create, draft, compose, generate, make, design, build
- Outputs: vows, email, resume, speech, document, proposal, content
- Example: "write wedding vows", "create a resume", "draft an email"

**UNDERSTANDING indicators:**  
- Verbs: understand, learn, explain, teach me, help me grasp, comprehend, figure out
- Topics: concepts, theories, how X works, why Y happens
- Example: "understand quadratic equations", "learn Python basics", "explain photosynthesis"

If multiple types apply, choose the PRIMARY intent based on emphasis.

Classification should be simple:
- **CREATION**: User wants to create/generate something tangible
- **UNDERSTANDING**: User wants to learn/comprehend something

Everything else is a variant of these two.

PART 2 - DESIGN THE TEMPLATE

Based on the intent type, design a prompt template:

**For CREATION tasks:**
- Role should be: creator, writer, designer, developer (match to domain)
- Focus on: generating a first draft, iterating, refining
- Include constraints: style, tone, format, length
- Emphasize: specificity, avoiding generic output

**For UNDERSTANDING tasks:**
- Role should be: teacher, tutor, explainer, guide
- Focus on: building understanding step-by-step, checking comprehension
- Include constraints: learning style, prior knowledge, goals
- Emphasize: clarity, connection to existing knowledge

Create the template using this structure:

**PROMPT_TEMPLATE:**
Role: [Who the AI should be - match to domain and intent]

Intent: {{userIntent}}
[Clear statement of what the user wants to accomplish]

Approach: [How the AI should help based on intent type]
[If CREATION → Generate first draft, iterate, refine]
[If UNDERSTANDING → Explain concepts, check understanding, build gradually]

Variables: [Include all {{variables}} here with context]
- {{variable1}}: [How this variable helps]
- {{variable2}}: [How this variable helps]
- etc.

Constraints: [Specific requirements - fold anti-patterns here]
- Length: {{length}}
- Style: {{style}}
- Avoid: {{avoidPatterns}}
- Focus: {{focusAreas}}

Output guidance: [What form should the help take?]

Success conditions: [When is the intent accomplished?]

**CRITICAL**: Every {{variable}} in USER_QUESTIONS MUST appear in the PROMPT_TEMPLATE.

PART 3 - GENERATE QUESTIONS

For each {{variable}} in the template above, create a question:

Use this format for each question:
```
Variable: {{variableName}}
Question: "[Clear, specific question]"
Type: [text | textarea | select]
Placeholder/Options: "[Helpful example or list of options]"
Why it matters: "[Brief explanation of how this helps accomplish their intent]"
```

Generate 8-12 questions that:
- Clarify the specific intent
- Provide context
- Identify constraints/preferences
- Surface what's blocking them (if applicable)
- Define success

Focus on questions that prevent generic output.

Part 4 - Identify Common Patterns to Avoid

Generate 3-5 typical approaches for this domain that are probably overdone or generic:

```
[ANTI-PATTERNS]
- Common Pattern 1: [description]
- Common Pattern 2: [description]
- Common Pattern 3: [description]
etc.
```

These should be folded into the "Constraints" section of the PROMPT_TEMPLATE.

Return your response in exactly this structure:
[ANTI-PATTERNS]
[list from Part 4]

[PROMPT_TEMPLATE]
[the template using format from Part 2]

[USER_QUESTIONS]
[the questions using format from Part 3]
```

### Expected Output Structure

**Example: Creation Intent - "I need to write wedding vows"**

```
[ANTI-PATTERNS]
- Common Pattern 1: Generic "heartfelt and sincere" language without specifics
- Common Pattern 2: Clichéd phrases like "journey together" or "soulmate"
- Common Pattern 3: Focus on wedding day rather than actual relationship/future

[PROMPT_TEMPLATE]
Role: Act as a wedding writing coach helping {{writerName}} create personal, meaningful marriage vows to {{partnerName}}. Good vows are a gift from one person to another.

Intent: {{userIntent}}
Help {{writerName}} write wedding vows that capture their relationship with {{partnerName}}, avoiding generic wedding language.

Approach: Provide a first draft that should be edited and made better. Focus on specific memories, shared values, and authentic promises about the future.

Variables:
- {{writerName}}: The person writing the vows
- {{partnerName}}: Their partner
- {{whatYouLove}}: Specific things they love about partner
- {{sharedInterests}}: Common interests/activities
- {{specialMemory}}: A memorable moment together
- {{vowStyle}}: Desired tone/style
- {{avoidPatterns}}: What they want to avoid
- {{vowLength}}: Target length
- {{language}}: Language preference

Constraints:
- Avoid {{avoidPatterns}}
- Target {{vowLength}} words
- Match {{vowStyle}} tone
- Include {{specialMemory}} if relevant

Output guidance: Return a first draft vow example that will be edited, in {{language}}.

Success conditions: Task is complete when the draft reads naturally, avoids generic wedding clichés, reflects provided details, and sounds like it comes from {{writerName}}.

[USER_QUESTIONS]

Variable: {{writerName}}
Question: "Your name:"
Type: text
Placeholder: "Sarah"
Why it matters: Personalizes the vow and ensures it sounds like it comes from a specific person

Variable: {{partnerName}}
Question: "Your partner's name:"
Type: text
Placeholder: "James"
Why it matters: Direct address creates intimacy

Variable: {{whatYouLove}}
Question: "What do you love about them? (Be specific)"
Type: textarea
Placeholder: "Their kindness to strangers, the way they make me laugh when I'm stressed, how they always remember small details"
Why it matters: Specificity prevents generic "I love you because you're wonderful" language

Variable: {{sharedInterests}}
Question: "What interests or activities do you share?"
Type: text
Placeholder: "Hiking, cooking, traveling to new places"
Why it matters: Provides concrete details that make vows feel real and lived-in

Variable: {{specialMemory}}
Question: "Share a special memory together:"
Type: textarea
Placeholder: "Our trip to Italy where we got lost in Florence and ended up finding that tiny restaurant"
Why it matters: Specific memories are impossible to fake and create emotional resonance

Variable: {{vowStyle}}
Question: "What style are you going for?"
Type: select
Placeholder: "Heartfelt and sincere | Romantic and poetic | Lighthearted with humor | Simple and direct"
Why it matters: Tone matching prevents the vows from feeling like someone else's words

Variable: {{avoidPatterns}}
Question: "What should these vows NOT sound like?"
Type: textarea
Placeholder: "No 'journey' or 'soulmate' talk, nothing that could be said to anyone"
Why it matters: Explicit anti-patterns push away from generic territory

Variable: {{vowLength}}
Question: "Desired length:"
Type: select
Placeholder: "100-150 words | 150-200 words | 200-300 words"
Why it matters: Constraints prevent rambling and force focus

Variable: {{language}}
Question: "Language preference:"
Type: select
Placeholder: "US English | UK English | Other"
Why it matters: Spelling consistency maintains authenticity
```

**Example 2: Understanding Intent - "I need help understanding quadratic equations"**

```
[ANTI-PATTERNS]
- Common Pattern 1: Jumping straight to formulas without building intuition
- Common Pattern 2: Overwhelming with abstract notation before showing real-world examples
- Common Pattern 3: Teaching memorization instead of understanding the "why"

[PROMPT_TEMPLATE]
Role: Act as a patient math tutor helping {{studentName}} understand quadratic equations. Deep learning comes from connecting new ideas to existing knowledge.

Intent: {{userIntent}}
Help {{studentName}} understand quadratic equations so they can solve problems confidently and see how they connect to real-world situations.

Approach: Start with visual intuition, build understanding step-by-step, check comprehension frequently, and connect to {{studentContext}} to make it relevant.

Variables:
- {{studentName}}: The learner
- {{studentLevel}}: Current math level
- {{purpose}}: Why they need to learn this
- {{learningStyle}}: How they learn best
- {{priorKnowledge}}: What they already know
- {{specificConfusion}}: What's confusing them
- {{explanationStyle}}: Preferred detail level
- {{realWorldExamples}}: Relevant applications

Constraints:
- Match {{learningStyle}} learning approach
- Build on {{priorKnowledge}}
- Address {{specificConfusion}}
- Use {{explanationStyle}} explanations
- Connect to {{realWorldExamples}}

Output guidance: Provide clear explanations with {{explanationStyle}}, include visual examples, check understanding with practice problems.

Success conditions: {{studentName}} can explain quadratics in their own words and solve basic problems without memorization.

[USER_QUESTIONS]

Variable: {{studentName}}
Question: "Your name:"
Type: text
Placeholder: "Alex"
Why it matters: Personalizes the learning experience

Variable: {{studentLevel}}
Question: "What's your current math level?"
Type: select
Placeholder: "Middle school | High school algebra | College prep | Adult learner"
Why it matters: Determines appropriate starting point

Variable: {{purpose}}
Question: "Why do you need to understand quadratic equations?"
Type: textarea
Placeholder: "I'm preparing for the SAT and need to solve quadratic problems quickly"
Why it matters: Connects concepts to specific goals

Variable: {{learningStyle}}
Question: "How do you learn math best?"
Type: select
Placeholder: "Visual (graphs, diagrams) | Step-by-step examples | Real-world applications | Practice problems"
Why it matters: Tailors teaching approach to your learning style

Variable: {{priorKnowledge}}
Question: "What do you already understand about algebra?"
Type: textarea
Placeholder: "I'm comfortable with linear equations and basic factoring"
Why it matters: Builds on solid foundation rather than assuming prior knowledge

Variable: {{specificConfusion}}
Question: "What specifically confuses you about quadratics?"
Type: textarea
Placeholder: "I can factor simple ones but don't understand why the quadratic formula works"
Why it matters: Identifies exact gap in understanding to address

Variable: {{explanationStyle}}
Question: "How detailed should explanations be?"
Type: select
Placeholder: "Very detailed | Moderate detail | Key points | Intuition over mechanics"
Why it matters: Matches preference for depth vs. speed

Variable: {{realWorldExamples}}
Question: "What real-world examples interest you?"
Type: textarea
Placeholder: "Sports, engineering, business, nature, technology"
Why it matters: Makes abstract math feel relevant and memorable
```

---

## Stage 2: Template Filling

### Variables to Send
```javascript
{
  "promptTemplate": "string",      // The template from Stage 1
  "userAnswers": {                  // Object with all user responses
    "variableName1": "value1",
    "variableName2": "value2",
    // etc.
  }
}
```

### The Prompt

```
You are filling in a prompt template with user-provided answers.

TEMPLATE:
{{promptTemplate}}

USER ANSWERS:
{{userAnswers}}

Task: Replace every {{variableName}} in the template with the corresponding value from the user answers.

Return ONLY the completed prompt with all variables replaced. Do not add commentary or explanation.
```

### Expected Output

A clean, filled prompt ready to copy-paste into any AI system.

---

## Key Simplifications

**What Changed:**
1. **Reduced 5 intent types to 2**: Creation vs. Understanding covers all cases
2. **Removed mandatory philosophical grounding**: Let it emerge naturally if relevant
3. **Folded anti-patterns into constraints**: No separate stage, cleaner structure
4. **Simplified template format**: Role, Intent, Approach, Variables, Constraints, Output guidance, Success conditions
5. **Fewer parsing stages**: Easier to parse and validate

**What Stayed:**
1. **Two-stage architecture**: Still generates template → fills template
2. **Variable coverage**: Still enforced that all variables must appear in template
3. **Anti-pattern mechanism**: Still identifies generic patterns to avoid
4. **Quality**: Still aims for specific, non-generic output

**Benefits:**
- Easier to maintain
- Faster to parse
- Less prone to errors
- Still produces high-quality prompts
- Simpler for the AI to follow

---

## Technical Notes

### Cost Estimates
- Stage 1: ~$0.02-0.05 per generation
- Stage 2: ~$0.001-0.01 per fill (or free if client-side)

### The Core Insight
Good prompts are specific, not generic. Good prompts include constraints. Good prompts avoid statistical center.

This meta-prompt encodes those lessons.
