# CLAUDE.md
## AI Assistant Context & Guidance

This file helps AI assistants (like Cursor, Claude, ChatGPT) understand this project's context, philosophy, and how to help effectively.

---

## Project Mission

**What We're Building:**
A meta-prompt generator that creates custom, domain-specific prompt templates. Users describe what they need, and the system generates a structured prompt with fill-in-the-blank questions that prevent generic output.

**Why It Matters:**
Most people use AI with vague prompts and get generic results. This system helps them construct *specific, constraint-rich prompts* that embed "lived understanding" rather than academic theory.

**Core Innovation:**
Anti-brainstorming mechanism that identifies statistically common patterns and explicitly helps users avoid them, pushing responses toward the long tail of the distribution.

---

## Philosophy & Design Decisions

### 1. **Nuance as Feature, Not Noise**
This project values specificity over polish. A prompt that says "avoid journey/soulmate language" is better than one that says "be authentic." Concrete constraints > abstract advice.

### 2. **Permission Over Perfection**
The system uses "first draft" language and philosophical grounding (e.g., "Good vows are a gift, not a performance") to reduce user anxiety. The goal is to help people start, not to deliver perfection.

### 3. **Anti-Brainstorming**
We explicitly identify high-probability (overdone) patterns and help users move away from them. The statistically likely response is often the generic one.

### 4. **Two-Stage Architecture**
- **Stage 1**: Meta-prompt generates custom prompt template + questions (OpenAI API call)
- **Stage 2**: Client-side template filling (no API needed - just string replacement)

We keep Stage 2 client-side because it's instant and free. Only use AI when we need actual intelligence.

### 5. **Python Backend for Future-Proofing**
We chose Flask over Node.js because:
- Easy to add CrewAI later for multi-agent prompt generation
- Better ML/AI library ecosystem
- Simpler for researchers/data scientists to extend

---

## Architecture Overview

```
User Input ("I need wedding vows")
    ↓
Flask Backend (/api/generate-template)
    ↓
OpenAI API (with meta-prompt from meta-prompt-system.md)
    ↓
Raw AI Response ([ANTI-PATTERNS] [PROMPT_TEMPLATE] [USER_QUESTIONS])
    ↓
React Frontend (parses response)
    ↓
Dynamic Form Rendered (based on USER_QUESTIONS)
    ↓
User Fills Form
    ↓
Client-Side Template Filling (replace {{variables}})
    ↓
Final Prompt Ready to Use
```

**Key Files:**
- `backend/app.py`: Flask API with OpenAI integration, error handling, and CORS configuration
- `backend/prompts/meta-prompt-system.md`: The Stage 1 meta-prompt (our secret sauce)
- `frontend/src/App.js`: React component with complete 4-step flow and parsing logic
- `frontend/src/api.js`: API client with error handling and network detection
- `frontend/src/App.css`: Professional styling system with CSS variables and animations

---

## Current File Hierarchy & Implementation Status

### **🔧 Core Implementation Files (Production Ready)**

**`backend/app.py`** - Flask API server with OpenAI GPT-4o integration, comprehensive error handling, CORS configuration, and robust logging. Handles template generation and health checks with proper validation and user-friendly error messages.

**`frontend/src/App.js`** - Main React component implementing complete 4-step user flow (landing → loading → form → result), dynamic form rendering based on AI output, robust parsing logic with debug logging, client-side template filling, and comprehensive state management.

**`frontend/src/App.css`** - Professional styling system with CSS custom properties, gradient backgrounds, smooth animations, color-coded sections (warning/success/error/info), responsive design for all screen sizes, and accessibility features including reduced motion support.

**`frontend/src/api.js`** - Clean API client with comprehensive error handling for template generation and health checks, includes network error detection, user-friendly error messages, and proper JSON response parsing.

### **📋 Configuration Files (Ready for Deployment)**

**`backend/requirements.txt`** - Python dependencies including Flask, OpenAI client (updated to >=1.6.1 for compatibility), CORS support, environment variable loading, and production server (gunicorn).

**`frontend/package.json`** - React project configuration with proper port settings (3001) to avoid conflicts with backend (3000), proxy configuration for development, and standard React dependencies.

**`.gitignore`** - Comprehensive ignore patterns for Python, Node.js, environment files, IDE files, OS-specific files, and build artifacts to prevent sensitive data from being committed.

### **📚 Documentation Files (Current & Comprehensive)**

**`CLAUDE.md`** - Detailed AI assistant guidance covering project philosophy, architecture, implementation details, common issues, troubleshooting, and how to help effectively - essential for maintaining and extending the project.

**`README.md`** - Complete project documentation including setup instructions, API endpoints, deployment guide, troubleshooting, testing procedures, current implementation status, and future roadmap - ready for public consumption.

**`backend/prompts/meta-prompt-system.md`** - The core intellectual property containing the meta-prompt template that instructs GPT-4 to generate structured prompt templates with anti-patterns, philosophical grounding, and user questions.

### **🗂️ Project Structure Files (Organized)**

**`backend/`** - Complete backend directory with Flask app, requirements, environment setup, and prompts folder containing the meta-prompt system.

**`frontend/`** - Complete React frontend with source files, public assets, build configuration, and node_modules (ignored) ready for development and production deployment.

**`form-schema-generator.md`** - Additional documentation file (supplementary material for the project).

### **🎯 Current Project Status**

✅ **Fully Functional**: Complete end-to-end meta-prompt generation system  
✅ **Production Ready**: Professional UI, comprehensive error handling, responsive design  
✅ **Well Documented**: Comprehensive guides for users and developers  
✅ **Deployment Ready**: Configuration files prepared for Render deployment  
✅ **Version Controlled**: Proper .gitignore and project structure  
✅ **Debug Ready**: Debug console and logging for troubleshooting  

**Port Configuration:**
- Backend: Port 3000 (configurable via PORT environment variable)
- Frontend: Port 3001 (configured in package.json to avoid conflicts)
- Proxy: Frontend proxies API calls to backend during development

---

## Critical Implementation Details

### The Meta-Prompt Template

The meta-prompt in `meta-prompt-system.md` is the core IP. It instructs GPT-4 to:
1. Identify anti-patterns (common/overdone approaches)
2. Determine variables needed for specificity
3. Generate a structured prompt template with {{variables}}
4. Create user questions for each variable

**Important**: The meta-prompt must produce output in this exact format:
```
[ANTI-PATTERNS]
- Common Pattern 1: ...
- Common Pattern 2: ...

[PROMPT_TEMPLATE]
Role: ...
Task: ...
Context: ...
Reasoning: ...
Output format: ...
Stop conditions: ...

[USER_QUESTIONS]
Variable: {{variableName}}
Question: "..."
Type: text | textarea | select
Placeholder/Options: "..."
Why it matters: "..."
```

If the format changes, the parsing logic in `App.js` breaks.

### Parsing Logic (Frontend)

The `parseAIOutput()` function in `App.js` uses regex to extract:
- Anti-patterns (lines starting with `- Common Pattern`)
- Prompt template (text between `[PROMPT_TEMPLATE]` and `[USER_QUESTIONS]`)
- Form fields (blocks starting with `Variable:`)

**Edge Cases to Watch:**
- AI might not follow exact format
- Variable names might have inconsistent casing
- Options might be separated by `|` or `/`
- Optional fields might say "optional" or "(optional)"

The parsing is flexible but not bulletproof. If GPT-4 gets creative with formatting, things break.

### Template Filling (Client-Side)

Simple regex replacement:
```javascript
Object.keys(values).forEach(key => {
  const regex = new RegExp(`\\{\\{${key}\\}\\}`, 'g');
  filledTemplate = filledTemplate.replace(regex, values[key]);
});
```

**Why Client-Side?**
- Instant (no API latency)
- Free (no token cost)
- Simple (just string replacement)

We only need AI for *intelligence*. Template filling is mechanical.

---

## Common Issues & Solutions

### Issue 1: "Parsing Failed - Can't Find Sections"

**Cause**: AI didn't follow the output format exactly

**Debug**:
1. Log the raw API response
2. Check if section headers are present
3. Look for formatting variations

**Fix**: Make the regex more flexible, or add fallback parsing

**Prevention**: Use GPT-4 (not 3.5-turbo) - it follows instructions better

### Issue 2: "Variables Not Being Replaced"

**Cause**: Variable names in template don't match form field IDs

**Debug**:
1. Log `formValues` object
2. Log all `{{variables}}` found in template
3. Compare for mismatches

**Fix**: Ensure parsing extracts variable names consistently

### Issue 3: "Form Fields Not Rendering"

**Cause**: `formFields` array is empty or malformed

**Debug**:
1. Check if `[USER_QUESTIONS]` section was parsed
2. Log the `schema.formFields` array
3. Verify field types are recognized

**Fix**: Adjust parsing logic to handle format variations

### Issue 4: "CORS Error When Calling Backend"

**Cause**: Backend CORS not configured for frontend domain

**Debug**: Check browser console for specific CORS error

**Fix**: 
1. Add frontend URL to CORS origins in `app.py`
2. Restart Flask server
3. Clear browser cache

### Issue 5: "API Key Invalid"

**Cause**: Environment variable not loaded or malformed

**Debug**:
1. Check `.env` file exists in `/backend`
2. Verify `OPENAI_API_KEY=sk-...` format
3. Ensure no extra quotes or spaces
4. Check if `python-dotenv` is installed

**Fix**: Reload environment variables, restart server

---

## How to Help Effectively

### When User Asks for Help With:

**"The parsing is breaking"**
→ Ask to see the raw API response
→ Check what format the AI actually returned
→ Suggest regex adjustments or fallback handling

**"I want to add a new feature"**
→ Understand if it's frontend or backend
→ Check if it fits the two-stage architecture
→ Suggest where in the codebase it should go

**"The prompts aren't good enough"**
→ This is a meta-prompt quality issue
→ The fix is in `meta-prompt-system.md`, not in code
→ Suggest specific improvements to the meta-prompt instructions

**"I want to add CrewAI"**
→ This goes in the backend
→ Create new file: `backend/crew_agents.py`
→ Keep the existing `/api/generate-template` as fallback
→ Add new endpoint: `/api/generate-template-crew`

**"Deployment issues"**
→ Check `render.yaml` configuration
→ Verify environment variables in Render dashboard
→ Ensure build commands are correct
→ Check CORS includes production URL

### What NOT to Do

**Don't** suggest complete rewrites unless truly necessary
**Don't** add complexity for edge cases that haven't happened yet
**Don't** change the output format without updating parsing logic
**Don't** add dependencies without checking if they're really needed
**Don't** break local development when improving production setup

### Code Style Preferences

- **Python**: Follow PEP 8, use type hints where helpful
- **JavaScript**: Modern ES6+, functional components for React
- **Comments**: Explain *why*, not *what* (code shows what)
- **Error handling**: Log errors, show friendly messages to users
- **Keep it simple**: Boring code that works > clever code that breaks

---

## Testing Checklist

Before suggesting code changes, mentally verify:

- [ ] Does this work locally? (both dev servers running)
- [ ] Does this work in production? (Render deployment)
- [ ] Does this break existing functionality?
- [ ] Is error handling adequate?
- [ ] Are environment variables handled correctly?
- [ ] Will users understand what went wrong if it fails?

## Test Suite

### Comprehensive Test Coverage

The project includes a comprehensive test suite in `/test/` directory (not committed to git) that validates:

**Test Scenarios (10 total):**
- **Creation Intent**: Wedding vows, apology letters
- **Understanding Intent**: Math learning, language learning  
- **Problem-Solving Intent**: Code debugging, relationship issues
- **Decision-Making Intent**: Job offers, investment decisions
- **Guidance Intent**: Business planning, presentation coaching

**Validation Tests:**
1. **Variable Coverage** - All form field variables appear in template
2. **Intent Classification** - Correct intent type identified
3. **Template Structure** - New intent-based format followed
4. **Anti-Patterns** - At least 3 anti-patterns generated
5. **Form Fields Quality** - Minimum 6 fields with placeholders

### Running Tests

```bash
# Prerequisites: Backend running on localhost:3000
cd test && ./run-tests.sh
```

### Current Test Results (Intent-Based Meta-Prompt)

**Status**: ❌ **0% Success Rate** - Critical issues identified

**Major Issues Found:**
1. **Intent Classification Failure** - AI defaults to "creation" for all intents
2. **Variable Coverage Issues** - Many variables missing from templates
3. **Template Structure Problems** - Some responses missing required sections
4. **Select Field Handling** - Select fields need options, not placeholders

**Root Cause**: The intent-based meta-prompt needs refinement to properly:
- Classify different intent types
- Ensure all variables appear in templates
- Follow the new template structure consistently

### Test-Driven Development

Use the test suite to:
- Validate meta-prompt changes before deployment
- Identify parsing issues early
- Ensure consistent behavior across intent types
- Catch regressions in template generation

---

## Current State & Known Limitations

### What Works
✅ Complete end-to-end flow (input → template → form → filled prompt)
✅ OpenAI API integration with comprehensive error handling
✅ Dynamic form generation from parsed AI output with field type detection
✅ Client-side template filling with variable replacement
✅ Professional UI with gradient backgrounds and smooth animations
✅ Anti-patterns display with warning styling
✅ Copy-to-clipboard functionality with success feedback
✅ Debug console for troubleshooting parsing issues
✅ Mobile-responsive design with accessibility features
✅ Form validation with required field checking
✅ Local development environment with proper port configuration
✅ Comprehensive logging and error messages
✅ Environment variable management and security
✅ Example Gallery - 5 example queries to teach users good prompt writing
✅ Better Error Messages - actionable guidance with suggestions
✅ Post-Generation Feedback - thumbs up/down collection
✅ Try This Prompt - generate example outputs from filled prompts

### What Needs Work
⚠️ Parsing could be more robust for format variations
⚠️ No user authentication or history tracking
⚠️ No analytics on which domains work best
⚠️ No A/B testing of different meta-prompts
⚠️ Intent classification needs refinement (currently defaults to creation)

### What's Intentionally Not Built Yet
🔮 CrewAI integration (waiting to see if needed)
🔮 Prompt library (need real usage first)
🔮 User accounts (keeping it simple for now)
🔮 Payment/subscription (validating concept first)

---

## Future Vision

### Phase 1 (Current)
Single-shot prompt generation. User describes need, gets prompt, uses it elsewhere.

### Phase 2 (Next)
Feedback loop. Track which prompts are rated highly, learn what works.

### Phase 3 (Later)
Multi-agent generation with CrewAI. Different agents handle domain analysis, pattern identification, template building, question design.

### Phase 4 (Dream)
The system learns from usage. Prompts get better over time. Users can share/remix prompts. Becomes a community-driven prompt library.

---

## Key Metrics to Track

(Not implemented yet, but when adding analytics, track these:)

- **Parse success rate**: % of AI responses that parse correctly
- **Form completion rate**: % who fill and submit the form
- **Prompt copy rate**: % who copy the final prompt
- **Domain distribution**: What are people asking for?
- **Time to completion**: How long from start to final prompt?
- **Return usage**: % who create multiple prompts

---

## When User Says "This is Broken"

**Step 1: Reproduce**
- What did they input?
- What did they expect?
- What actually happened?

**Step 2: Isolate**
- Is it frontend (parsing/rendering) or backend (API/OpenAI)?
- Check browser console for JS errors
- Check backend logs for Python errors

**Step 3: Fix**
- If parsing: adjust regex or add fallbacks
- If API: check rate limits, error handling
- If UI: improve validation or error messages

**Step 4: Prevent**
- Add logging for this case
- Improve error messages
- Add validation if needed

---

## Philosophy on AI Assistance

This project *uses* AI (OpenAI API) to *help humans use* AI (ChatGPT/Claude) better. It's meta-level work.

When helping with this project:
- **Respect the meta-level**: Changes to the meta-prompt affect all generated prompts
- **Value specificity**: Generic suggestions aren't helpful (ironic, right?)
- **Test your suggestions**: If you'd suggest code, trace through what would actually happen
- **Understand the user journey**: From vague need → structured prompt is the magic

---

## Quick Reference

**Start local dev:**
```bash
# Terminal 1 - Backend (runs on port 3000)
cd backend
python3 app.py

# Terminal 2 - Frontend (runs on port 3001)
cd frontend
npm start
```

**Note**: Backend runs on port 3000, frontend on port 3001 to avoid conflicts. Frontend proxies API calls to backend during development.

**Deploy to Render:**
```bash
git add .
git commit -m "description"
git push origin main
# Render auto-deploys
```

**Update meta-prompt:**
Edit `backend/prompts/meta-prompt-system.md`, then:
```bash
git add backend/prompts/meta-prompt-system.md
git commit -m "Improved meta-prompt"
git push
```

**Check logs:**
- Local: Terminal output
- Render: Dashboard → Service → Logs tab

---

## Final Notes

This is v1.0. It will evolve. The code matters less than the *idea*:

**Can we systematically generate prompts that are statistically unlikely but still coherent and useful?**

That's the experiment. The code is just the apparatus.

When helping, optimize for *learning* not *shipping*. We want to know:
- Does the anti-brainstorming mechanism actually work?
- Do generated prompts feel "lived in" or academic?
- Which domains produce the best results?
- Where does the parsing break?
- What makes users abandon the flow?

Help us learn. That's more valuable than any feature.

---

**Last Updated**: 2025-10-24
**Version**: 1.0
**Status**: Early development / Testing phase