# Form Schema Generator
## Transforming Stage 1 Output into UI-Ready JSON

---

## Overview

This document shows how to parse the Stage 1 AI output and convert it into a JSON schema that can drive a dynamic form in your web application.

---

## Input: Raw AI Output

The AI returns three sections:
1. `[ANTI-PATTERNS]` - List of common patterns to avoid
2. `[PROMPT_TEMPLATE]` - The prompt with {{variables}}
3. `[USER_QUESTIONS]` - Questions for each variable

---

## Output: JSON Schema

### Complete Schema Structure

```json
{
  "meta": {
    "domain": "groomsman speech",
    "userFraming": "Treat nuance as a feature, not noise",
    "generatedAt": "2025-10-24T10:30:00Z"
  },
  "antiPatterns": [
    "Overused 'funny memory' opener (e.g., 'I've known the groom since we were kids, and let me tell you…'). These sound templated and lack emotional specificity.",
    "Predictable structure — humor, sentiment, toast — with no real narrative or reflection on the relationship's meaning.",
    "Generic praise of the bride ('she's beautiful, smart, and perfect for him') instead of describing how she changes or complements the groom.",
    "Forced humor or cliché jokes ('I didn't think he'd ever settle down!') that sound borrowed from the internet.",
    "Treating the speech as a roast or stand-up routine rather than a moment of genuine tribute and connection."
  ],
  "promptTemplate": "Role:\nYou are a speechwriter helping craft a heartfelt, memorable first draft of a groomsman speech. A good groomsman speech is not a comedy routine — it's a reflection of genuine connection. It honors shared history, celebrates growth, and bridges humor with sincerity. Treat nuance as a feature, not noise: the small, specific moments reveal the emotional truth better than big declarations.\n\nTask:\nWrite a first draft of a groomsman speech for {{groomName}} and {{brideName}}, to be delivered by {{speakerName}}. The speech should reflect {{relationshipDescription}}, highlight {{coreMemory}}, and show how {{groomGrowth}} reveals who {{groomName}} is as a person. Include subtle humor inspired by {{humorStyle}} and a closing sentiment that ties back to {{speechTheme}}. Avoid {{avoidPatterns}} from common wedding-speech clichés.\n\nContext:\nThis is for a wedding with {{audienceType}} (e.g., close friends, family, mixed). The tone should balance sincerity with levity, grounded in authentic detail rather than general praise. Length should be around 3–5 minutes of spoken time. Explicitly avoid overused tropes listed in Part 1, and instead focus on sensory detail, emotional accuracy, and genuine admiration.\n\nReasoning:\nThis approach works because it translates lived experience into story. It makes the speech sound like you, not a template. The goal isn't perfection; it's emotional truth and relatability. Specific anecdotes and reflections will make the humor land naturally and the sentiment feel earned.\n\nOutput format:\n• Title: 'Groomsman Speech for {{groomName}} and {{brideName}}'\n• Body: 4–6 short paragraphs (each ~4–6 sentences)\n• Tone: Warm, self-aware, and personal with a natural rhythm for speaking aloud\n• Include a closing toast line (e.g., 'To {{groomName}} and {{brideName}}…')\n\nStop conditions:\n• Speech feels authentic, not performative\n• Humor feels organic to the relationship, not copied\n• Ends with a heartfelt toast\n• Avoids clichés and internet-standard phrasing",
  "formFields": [
    {
      "id": "speakerName",
      "variable": "{{speakerName}}",
      "question": "What's your name or how would you like to be introduced in the speech?",
      "type": "text",
      "required": true,
      "placeholder": "Best man Alex / Groomsman Sam / Brother Jake",
      "helpText": "The way the speaker is introduced affects tone and perspective (e.g., best friend vs. brother creates different intimacy levels).",
      "validation": {
        "minLength": 2,
        "maxLength": 100
      }
    },
    {
      "id": "groomName",
      "variable": "{{groomName}}",
      "question": "What's the groom's name?",
      "type": "text",
      "required": true,
      "placeholder": "Ethan / Michael / Chris",
      "helpText": "Personalizing the name ensures the speech feels tailored and sincere, not generic.",
      "validation": {
        "minLength": 2,
        "maxLength": 50
      }
    },
    {
      "id": "brideName",
      "variable": "{{brideName}}",
      "question": "What's the bride's name?",
      "type": "text",
      "required": true,
      "placeholder": "Anna / Jasmine / Taylor",
      "helpText": "Including the bride respectfully and specifically connects the speech to both halves of the couple.",
      "validation": {
        "minLength": 2,
        "maxLength": 50
      }
    },
    {
      "id": "relationshipDescription",
      "variable": "{{relationshipDescription}}",
      "question": "How do you know the groom, and what defines your relationship?",
      "type": "textarea",
      "required": true,
      "placeholder": "We've been friends since college and shared countless adventures — he's like a brother to me.",
      "helpText": "Context of the relationship shapes emotional tone and storytelling focus.",
      "validation": {
        "minLength": 20,
        "maxLength": 500
      }
    },
    {
      "id": "coreMemory",
      "variable": "{{coreMemory}}",
      "question": "What's one specific, memorable story or moment that captures who the groom is?",
      "type": "textarea",
      "required": true,
      "placeholder": "That time he stayed up all night helping me move apartments when my truck broke down.",
      "helpText": "Concrete details prevent generic praise and anchor emotion in lived experience.",
      "validation": {
        "minLength": 30,
        "maxLength": 800
      }
    },
    {
      "id": "groomGrowth",
      "variable": "{{groomGrowth}}",
      "question": "How has the groom changed or grown since meeting his partner?",
      "type": "textarea",
      "required": true,
      "placeholder": "He's calmer now, more patient — you can see how she brings out his best side.",
      "helpText": "Shows emotional evolution; turns the speech from nostalgia to tribute.",
      "validation": {
        "minLength": 20,
        "maxLength": 500
      }
    },
    {
      "id": "humorStyle",
      "variable": "{{humorStyle}}",
      "question": "What kind of humor suits your relationship or the audience?",
      "type": "select",
      "required": true,
      "options": [
        { "value": "playful_teasing", "label": "Playful teasing" },
        { "value": "dry_wit", "label": "Dry wit" },
        { "value": "self_deprecating", "label": "Self-deprecating" },
        { "value": "story_based", "label": "Story-based" },
        { "value": "minimal_humor", "label": "Minimal humor" }
      ],
      "helpText": "Sets the comedic boundaries and tone, avoiding forced or inappropriate jokes."
    },
    {
      "id": "speechTheme",
      "variable": "{{speechTheme}}",
      "question": "What's the central theme or feeling you want the speech to leave with?",
      "type": "select",
      "required": true,
      "options": [
        { "value": "loyalty", "label": "Loyalty" },
        { "value": "growth", "label": "Growth" },
        { "value": "friendship", "label": "Friendship" },
        { "value": "found_family", "label": "Found family" },
        { "value": "enduring_love", "label": "Enduring love" },
        { "value": "gratitude", "label": "Gratitude" }
      ],
      "helpText": "Creates narrative coherence and emotional direction for the speech."
    },
    {
      "id": "audienceType",
      "variable": "{{audienceType}}",
      "question": "Who will be in the audience?",
      "type": "select",
      "required": true,
      "options": [
        { "value": "mostly_family", "label": "Mostly family" },
        { "value": "mostly_friends", "label": "Mostly friends" },
        { "value": "mixed_crowd", "label": "Mixed crowd" },
        { "value": "small_intimate_group", "label": "Small intimate group" }
      ],
      "helpText": "Adjusts language and humor to audience comfort and relatability."
    },
    {
      "id": "avoidPatterns",
      "variable": "{{avoidPatterns}}",
      "question": "Are there any clichés, topics, or tones you want to avoid?",
      "type": "textarea",
      "required": false,
      "placeholder": "No embarrassing stories / Avoid sappy clichés / Don't mention exes",
      "helpText": "Prevents common pitfalls from the anti-pattern list and ensures emotional safety and taste.",
      "validation": {
        "maxLength": 500
      }
    },
    {
      "id": "speechTone",
      "variable": "{{speechTone}}",
      "question": "What overall tone should the speech carry?",
      "type": "select",
      "required": false,
      "options": [
        { "value": "heartfelt", "label": "Heartfelt" },
        { "value": "witty_warm", "label": "Witty and warm" },
        { "value": "reflective", "label": "Reflective" },
        { "value": "playful_sincere", "label": "Playful but sincere" }
      ],
      "helpText": "Guides rhythm, word choice, and emotional pacing to match the speaker's personality."
    }
  ]
}
```

---

## Parsing Logic

### Step 1: Extract Anti-Patterns

```javascript
function parseAntiPatterns(rawOutput) {
  const antiPatternsSection = rawOutput.match(/\[ANTI-PATTERNS\]([\s\S]*?)\[PROMPT_TEMPLATE\]/);
  if (!antiPatternsSection) return [];
  
  const lines = antiPatternsSection[1].trim().split('\n');
  return lines
    .filter(line => line.trim().startsWith('•') || line.trim().startsWith('-'))
    .map(line => line.replace(/^[•\-]\s*/, '').replace(/^Common Pattern \d+:\s*/, '').trim());
}
```

### Step 2: Extract Prompt Template

```javascript
function parsePromptTemplate(rawOutput) {
  const templateSection = rawOutput.match(/\[PROMPT_TEMPLATE\]([\s\S]*?)\[USER_QUESTIONS\]/);
  if (!templateSection) return '';
  
  return templateSection[1].trim();
}
```

### Step 3: Extract and Structure Form Fields

```javascript
function parseFormFields(rawOutput) {
  const questionsSection = rawOutput.match(/\[USER_QUESTIONS\]([\s\S]*?)$/);
  if (!questionsSection) return [];
  
  const fieldBlocks = questionsSection[1].split(/Variable:/g).filter(block => block.trim());
  
  return fieldBlocks.map(block => {
    const lines = block.trim().split('\n');
    
    // Extract variable name
    const variableMatch = lines[0].match(/\{\{(\w+)\}\}/);
    const variableName = variableMatch ? variableMatch[1] : '';
    
    // Extract question
    const questionMatch = block.match(/Question:\s*["'](.+?)["']/);
    const question = questionMatch ? questionMatch[1] : '';
    
    // Extract type
    const typeMatch = block.match(/Type:\s*(\w+)/);
    const type = typeMatch ? typeMatch[1] : 'text';
    
    // Extract placeholder/options
    const placeholderMatch = block.match(/Placeholder\/Options:\s*["'](.+?)["']/);
    const placeholder = placeholderMatch ? placeholderMatch[1] : '';
    
    // Extract help text
    const helpTextMatch = block.match(/Why it matters:\s*(.+?)(?:\n|$)/);
    const helpText = helpTextMatch ? helpTextMatch[1].trim() : '';
    
    // Parse options if type is select
    let options = null;
    if (type === 'select' && placeholder) {
      options = placeholder.split('|').map(opt => ({
        value: opt.trim().toLowerCase().replace(/\s+/g, '_'),
        label: opt.trim()
      }));
    }
    
    const field = {
      id: variableName,
      variable: `{{${variableName}}}`,
      question: question,
      type: type,
      required: true, // Default to required, can be adjusted
      helpText: helpText
    };
    
    if (type === 'select' && options) {
      field.options = options;
    } else {
      field.placeholder = placeholder;
    }
    
    // Add validation rules
    if (type === 'text') {
      field.validation = { minLength: 2, maxLength: 100 };
    } else if (type === 'textarea') {
      field.validation = { minLength: 20, maxLength: 800 };
    }
    
    return field;
  });
}
```

### Step 4: Build Complete Schema

```javascript
function buildFormSchema(rawOutput, userDomain, userFraming) {
  return {
    meta: {
      domain: userDomain,
      userFraming: userFraming,
      generatedAt: new Date().toISOString()
    },
    antiPatterns: parseAntiPatterns(rawOutput),
    promptTemplate: parsePromptTemplate(rawOutput),
    formFields: parseFormFields(rawOutput)
  };
}
```

---

## UI Component Mapping

### Anti-Patterns Display

```jsx
// React component example
function AntiPatternsDisplay({ patterns }) {
  if (!patterns || patterns.length === 0) return null;
  
  return (
    <div className="anti-patterns-section">
      <h3>What We'll Help You Avoid</h3>
      <p className="intro">These are common patterns that make speeches feel generic:</p>
      <ul className="anti-patterns-list">
        {patterns.map((pattern, idx) => (
          <li key={idx}>{pattern}</li>
        ))}
      </ul>
    </div>
  );
}
```

### Dynamic Form Generator

```jsx
function DynamicFormField({ field, value, onChange }) {
  const renderField = () => {
    switch (field.type) {
      case 'text':
        return (
          <input
            type="text"
            id={field.id}
            value={value}
            onChange={(e) => onChange(field.id, e.target.value)}
            placeholder={field.placeholder}
            required={field.required}
            minLength={field.validation?.minLength}
            maxLength={field.validation?.maxLength}
          />
        );
      
      case 'textarea':
        return (
          <textarea
            id={field.id}
            value={value}
            onChange={(e) => onChange(field.id, e.target.value)}
            placeholder={field.placeholder}
            required={field.required}
            minLength={field.validation?.minLength}
            maxLength={field.validation?.maxLength}
            rows={4}
          />
        );
      
      case 'select':
        return (
          <select
            id={field.id}
            value={value}
            onChange={(e) => onChange(field.id, e.target.value)}
            required={field.required}
          >
            <option value="">-- Select --</option>
            {field.options.map(opt => (
              <option key={opt.value} value={opt.value}>
                {opt.label}
              </option>
            ))}
          </select>
        );
      
      default:
        return null;
    }
  };
  
  return (
    <div className="form-field">
      <label htmlFor={field.id}>
        {field.question}
        {field.required && <span className="required">*</span>}
      </label>
      {renderField()}
      {field.helpText && (
        <p className="help-text">{field.helpText}</p>
      )}
    </div>
  );
}

function DynamicForm({ schema, onSubmit }) {
  const [values, setValues] = useState({});
  
  const handleChange = (fieldId, value) => {
    setValues(prev => ({ ...prev, [fieldId]: value }));
  };
  
  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(values);
  };
  
  return (
    <form onSubmit={handleSubmit}>
      <AntiPatternsDisplay patterns={schema.antiPatterns} />
      
      <div className="form-fields">
        {schema.formFields.map(field => (
          <DynamicFormField
            key={field.id}
            field={field}
            value={values[field.id] || ''}
            onChange={handleChange}
          />
        ))}
      </div>
      
      <button type="submit">Generate Prompt</button>
    </form>
  );
}
```

---

## Stage 2: Filling the Template

Once the form is submitted, you have two options:

### Option A: Client-Side (Fast, Free)

```javascript
function fillTemplate(template, values) {
  let filledTemplate = template;
  
  Object.keys(values).forEach(key => {
    const regex = new RegExp(`\\{\\{${key}\\}\\}`, 'g');
    filledTemplate = filledTemplate.replace(regex, values[key]);
  });
  
  return filledTemplate;
}
```

### Option B: AI-Powered (Handles Edge Cases)

```javascript
async function fillTemplateWithAI(template, values) {
  const response = await fetch('/api/fill-template', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      template: template,
      values: values
    })
  });
  
  const data = await response.json();
  return data.filledPrompt;
}
```

**Recommendation**: Start with Option A (client-side). Only use Option B if you need smart handling of missing fields or want to clean up the formatting.

---

## Complete User Flow Example

```javascript
// 1. User submits their domain
const userInput = {
  domain: "i need help writing a groomsman speech",
  framing: "Treat nuance as a feature, not noise"
};

// 2. Call Stage 1 API
const stage1Response = await fetch('/api/generate-template', {
  method: 'POST',
  body: JSON.stringify(userInput)
});
const rawOutput = await stage1Response.text();

// 3. Parse into schema
const schema = buildFormSchema(rawOutput, userInput.domain, userInput.framing);

// 4. Render form
<DynamicForm schema={schema} onSubmit={(values) => {
  // 5. Fill template (client-side)
  const finalPrompt = fillTemplate(schema.promptTemplate, values);
  
  // 6. Display result
  showResult(finalPrompt);
}} />
```

---

## Storage Considerations

### What to Store

```javascript
{
  userId: "user123",
  sessionId: "session456",
  timestamp: "2025-10-24T10:30:00Z",
  
  // Input
  userDomain: "i need help writing a groomsman speech",
  userFraming: "Treat nuance as a feature, not noise",
  
  // Generated
  schema: { /* full schema */ },
  
  // User responses
  userValues: { /* form values */ },
  
  // Output
  finalPrompt: "Role: You are a speechwriter...",
  
  // Metadata
  feedbackRating: null, // To be filled later
  wasPromptUsed: null,  // Track if they actually used it
  editsMade: null       // Track if they modified the prompt
}
```

### Why Store This

- **Analytics**: Which domains are most popular?
- **Quality tracking**: Which generated prompts get high ratings?
- **Iteration**: Learn what works and what doesn't
- **User history**: "View your past prompts"

---

## Testing the Schema

### Test Cases

**Test 1: Complete Form**
- Fill all required fields
- Verify template fills correctly
- Check no {{variables}} remain

**Test 2: Missing Required Fields**
- Try to submit with empty required fields
- Verify validation works

**Test 3: Select Fields**
- Verify options display correctly
- Check value mapping works

**Test 4: Anti-Patterns Display**
- Confirm patterns are visible
- Check formatting is readable

**Test 5: Long Text**
- Fill textarea with maximum length
- Verify it doesn't break layout

---

## Next Steps

1. **Build the parser**: Implement the parsing functions
2. **Test with real output**: Run the Stage 1 prompt and parse the result
3. **Build the form**: Create the dynamic form UI
4. **Test the flow**: End-to-end from input → form → filled prompt
5. **Iterate**: Adjust based on what breaks

---

## Open Questions

1. **Should we show anti-patterns before or after the form?**
   - Before: Sets context, but might be overwhelming
   - After: Feels like "here's what we avoided"

2. **How do we handle optional fields in the template?**
   - Leave empty {{variables}}?
   - Fill with default text?
   - Ask AI to handle gracefully?

3. **Should users be able to edit the generated prompt?**
   - Textarea for final edits before copying?
   - Or just copy-paste into their own editor?

4. **What if parsing fails?**
   - Fallback to generic template?
   - Show error and let user retry?
   - Manual review queue?

---

## Success Metrics

- **Parse success rate**: >95% of AI outputs parse correctly
- **Form completion rate**: >60% of users who start, finish
- **Copy rate**: >80% of users copy the final prompt
- **Return rate**: >30% of users come back for another prompt

This is gold if it works. And even if it doesn't, you'll learn why.