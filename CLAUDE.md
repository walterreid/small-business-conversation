# CLAUDE.md
## AI Assistant Context & Guidance

This file helps AI assistants (like Cursor, Claude, ChatGPT) understand this project's context, philosophy, and how to help effectively.

---

## Project Mission

**What We're Building:**
A chat-based small business marketing plan generator. Users select their business category, answer questions in a conversational flow, and receive a personalized marketing plan tailored to their specific needs and budget.

**Why It Matters:**
Most small businesses struggle with marketing because they don't know where to start or what strategies work for their industry. This tool guides them through a structured conversation to understand their business, then generates an actionable marketing plan with specific recommendations.

**Core Innovation:**
Conversational question flow that collects business-specific information, then uses AI to generate comprehensive, actionable marketing plans with budget-aware recommendations and 90-day action plans.

---

## Philosophy & Design Decisions

### 1. **Conversational Over Forms**
We use a chat interface instead of long forms. One question at a time feels less overwhelming and more engaging. Inspired by Bridesmaid for Hire's conversational flow.

### 2. **Category-Specific Intelligence**
Each business category (Restaurant, Retail, Professional Services, E-commerce, Local Services) has tailored questions and recommendations. A restaurant needs different marketing strategies than a local plumber.

### 3. **Budget-Aware Recommendations**
Marketing plans adapt to budget constraints. Under $500/month gets different recommendations than $5000+/month. We recommend channels that make sense for the budget.

### 4. **Actionable Over Generic**
Plans include specific tactics, timelines, and next steps. Not "do social media" but "post 3x/week on Instagram focusing on behind-the-scenes content, use these hashtags..."

### 5. **Python Backend for Future-Proofing**
We chose Flask over Node.js because:
- Easy to add data analysis (pandas for SMB stats)
- Better ML/AI library ecosystem
- Simpler for researchers/data scientists to extend

---

## Architecture Overview

```
User Selects Category (Restaurant, Retail, etc.)
    ↓
Chat Interface (one question at a time)
    ↓
Flask Backend (/api/chat/start, /api/chat/message)
    ↓
Question Flow System (chat_flows.py)
    ↓
OpenAI Chat API (conversational, maintains context)
    ↓
All Questions Answered
    ↓
Marketing Plan Generation (/api/chat/generate-plan)
    ↓
Structured Marketing Plan (Executive Summary, Channels, 90-Day Plan, Metrics)
```

**Key Files:**
- `backend/app.py`: Flask API with OpenAI integration, chat endpoints, session management
- `backend/chat_flows.py`: Question sequences for each business category
- `frontend/src/App.js`: React component with 3-step flow (category → chat → plan)
- `frontend/src/components/ChatInterface.js`: Chat UI using Chatscope UI Kit
- `frontend/src/components/CategorySelector.js`: Business category selection
- `frontend/src/components/MarketingPlanView.js`: Marketing plan display
- `frontend/src/api/chatApi.js`: Chat API client functions

---

## Current File Hierarchy & Implementation Status

### **🔧 Core Implementation Files (Production Ready)**

**`backend/app.py`** - Flask API server with OpenAI GPT-4o integration, chat endpoints (`/api/chat/start`, `/api/chat/message`, `/api/chat/generate-plan`), session management (in-memory), comprehensive error handling, CORS configuration, and robust logging.

**`backend/chat_flows.py`** - Question flow system defining structured questions for each business category (Restaurant, Retail Store, Professional Services, E-commerce, Local Services). Includes functions to get next question, check completion, and generate marketing plan prompts.

**`frontend/src/App.js`** - Main React component implementing 3-step user flow (category selection → chat interface → marketing plan view), state management, and navigation.

**`frontend/src/components/ChatInterface.js`** - Chat UI component using Chatscope UI Kit, handles session management, message sending/receiving, completion detection, and plan generation.

**`frontend/src/components/CategorySelector.js`** - Business category selection component with card-based UI, 5 categories with icons and descriptions.

**`frontend/src/components/MarketingPlanView.js`** - Marketing plan display component with copy/download functionality, usage instructions, and start over option.

**`frontend/src/api/chatApi.js`** - Chat API client with functions for starting sessions, sending messages, generating plans, and retrieving sessions.

### **📋 Configuration Files (Ready for Deployment)**

**`backend/requirements.txt`** - Python dependencies including Flask, OpenAI client, CORS support, environment variable loading, and production server (gunicorn).

**`frontend/package.json`** - React project configuration with proper port settings (3001), Chatscope UI Kit dependencies, and standard React dependencies.

**`.gitignore`** - Comprehensive ignore patterns for Python, Node.js, environment files, IDE files, OS-specific files, and build artifacts.

### **📚 Documentation Files (Current & Comprehensive)**

**`CLAUDE.md`** - Detailed AI assistant guidance covering project philosophy, architecture, implementation details, common issues, troubleshooting, and how to help effectively.

**`README.md`** - Complete project documentation including setup instructions, API endpoints, deployment guide, troubleshooting, and current implementation status.

**`docs/DEPLOYMENT.md`** - Render deployment guide with service configuration, environment variables, and troubleshooting.

**`docs/TROUBLESHOOTING.md`** - General troubleshooting guide for common issues.

**`docs/`** - Migration documentation folder containing:
- Architecture planning documents
- Phase-by-phase implementation summaries
- Troubleshooting guides
- Historical reference materials

### **🎯 Current Project Status**

✅ **Fully Functional**: Complete end-to-end chat-based marketing plan generation system  
✅ **Production Ready**: Professional UI with smooth animations, comprehensive error handling, responsive design  
✅ **Well Documented**: Comprehensive guides for users and developers  
✅ **Deployment Ready**: Configuration files prepared for Render deployment  
✅ **Version Controlled**: Proper .gitignore and project structure  
✅ **Chat-Based Flow**: Conversational interface using Chatscope UI Kit  

**Port Configuration:**
- Backend: Port 5001 (configurable via PORT environment variable, 5001 to avoid macOS AirPlay conflict)
- Frontend: Port 3001 (configured in package.json to avoid conflicts)
- Proxy: Frontend proxies API calls to backend during development

---

## Critical Implementation Details

### The Question Flow System

The question flows in `chat_flows.py` define structured questions for each business category. Each category has 9 questions covering:
- Business basics (name, type, location)
- Target audience
- Budget
- Current marketing
- Biggest challenges
- Unique value proposition
- Goals

**Question Structure:**
```python
{
    "id": "business_name",
    "question": "What's your restaurant's name?",
    "type": "text",  # text | textarea | select
    "required": True,
    "help_text": "This will be used throughout your marketing plan"
}
```

**Flow Management:**
- `get_next_question(category, answered_questions)` - Returns next unanswered question
- `is_flow_complete(category, answered_questions)` - Checks if all required questions answered
- `generate_marketing_plan_prompt(category, answers)` - Builds structured prompt for OpenAI

### Session Management

Sessions are stored in-memory (can be upgraded to database later):
```python
{
    "session_id": "uuid",
    "category": "restaurant",
    "answers": {
        "business_name": "Joe's Pizza",
        "cuisine_type": "Italian",
        # ... more answers
    },
    "conversation": [
        {"role": "assistant", "content": "...", "timestamp": "..."},
        {"role": "user", "content": "...", "timestamp": "..."}
    ],
    "current_question_id": "business_name",
    "created_at": "ISO timestamp"
}
```

### Marketing Plan Generation

The `generate_marketing_plan_prompt()` function builds a comprehensive prompt that includes:
- All collected answers
- Category-specific context
- Request for structured plan (Executive Summary, Target Audience, Channels, 90-Day Plan, Metrics)
- Budget-aware recommendations

---

## Common Issues & Solutions

### Issue 1: "Session Not Found"

**Cause**: Session expired or invalid session ID

**Debug**:
1. Check if session exists in `chat_sessions` dict
2. Verify session ID is being passed correctly
3. Check if session was created successfully

**Fix**: Start a new session, ensure session ID is stored in frontend state

### Issue 2: "No Questions Found for Category"

**Cause**: Invalid category or category not in QUESTION_FLOWS

**Debug**:
1. Check category value matches valid categories
2. Verify category is in `chat_flows.py` QUESTION_FLOWS
3. Check category normalization (lowercase, underscores)

**Fix**: Ensure category matches: restaurant, retail_store, professional_services, ecommerce, local_services

### Issue 3: "All Questions Not Answered"

**Cause**: User tried to generate plan before answering all required questions

**Debug**:
1. Check `is_flow_complete()` return value
2. Verify all required questions have answers
3. Check answer extraction logic

**Fix**: Ensure all required questions are answered before allowing plan generation

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

**"The chat flow isn't working"**
→ Check session management
→ Verify question flow logic in `chat_flows.py`
→ Check if answers are being stored correctly
→ Look at backend logs for errors

**"I want to add a new business category"**
→ Add category to `CategorySelector.js` BUSINESS_CATEGORIES
→ Create question flow in `chat_flows.py` QUESTION_FLOWS
→ Add category validation in backend endpoints

**"I want to modify the questions"**
→ Edit `chat_flows.py` QUESTION_FLOWS
→ Questions are category-specific
→ Ensure question IDs are unique
→ Test the flow after changes

**"The marketing plan isn't good enough"**
→ This is a prompt quality issue
→ The fix is in `generate_marketing_plan_prompt()` in `chat_flows.py`
→ Can also enhance with SMB data in Phase 8
→ Suggest specific improvements to the prompt structure

**"I want to add SMB data integration"**
→ This goes in Phase 8
→ Read Excel file with pandas
→ Extract insights and stats
→ Include in marketing plan prompt
→ Update `generate_marketing_plan_prompt()` to use data

**"Deployment issues"**
→ Check `render.yaml` configuration
→ Verify environment variables in Render dashboard
→ Ensure build commands are correct
→ Check CORS includes production URL

### What NOT to Do

**Don't** suggest complete rewrites unless truly necessary
**Don't** add complexity for edge cases that haven't happened yet
**Don't** change question flow structure without updating both frontend and backend
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
- [ ] Does the chat flow complete properly?
- [ ] Are all questions being asked and answered?

---

## Current State & Known Limitations

### What Works
✅ Complete end-to-end chat-based flow (category → chat → plan)
✅ OpenAI API integration with conversational chat
✅ Structured question flows for 5 business categories
✅ Session management (in-memory)
✅ Marketing plan generation with structured output
✅ Professional UI with Chatscope UI Kit
✅ Smooth animations and transitions
✅ Copy/download functionality for plans
✅ Mobile-responsive design
✅ Comprehensive error handling
✅ Local development environment with proper port configuration

### What Needs Work
⚠️ Session persistence (currently in-memory, lost on restart)
⚠️ SMB data integration (Phase 8)
⚠️ No user authentication or history tracking
⚠️ No analytics on which categories/plans work best
⚠️ No A/B testing of different question flows

### What's Intentionally Not Built Yet
🔮 Database for session persistence (keeping it simple for now)
🔮 User accounts (keeping it simple for now)
🔮 Payment/subscription (validating concept first)
🔮 Plan history/favorites (need real usage first)

---

## Future Vision

### Phase 8 (Next)
Integrate SMB statistics data to enhance marketing plan recommendations with real industry insights and benchmarks.

### Phase 9 (Later)
Testing and refinement based on real user feedback. Handle edge cases, improve error messages, optimize performance.

### Phase 10 (Later)
Cleanup and documentation. Remove old code references, update all docs, prepare for public launch.

### Future Enhancements
- Database for session persistence
- User accounts and plan history
- Analytics dashboard
- A/B testing of question flows
- Multi-language support
- Export plans as PDF

---

## Key Metrics to Track

(Not implemented yet, but when adding analytics, track these:)

- **Session completion rate**: % who complete all questions
- **Plan generation rate**: % who generate plans after completing questions
- **Category distribution**: Which business types use the tool most?
- **Time to completion**: How long from start to plan generation?
- **Return usage**: % who create multiple plans
- **Plan quality feedback**: User ratings on plan usefulness

---

## When User Says "This is Broken"

**Step 1: Reproduce**
- What category did they select?
- What question were they on?
- What did they expect?
- What actually happened?

**Step 2: Isolate**
- Is it frontend (chat UI/rendering) or backend (API/OpenAI)?
- Check browser console for JS errors
- Check backend logs for Python errors
- Check session state

**Step 3: Fix**
- If chat: check session management, question flow logic
- If API: check rate limits, error handling, OpenAI responses
- If UI: improve validation or error messages

**Step 4: Prevent**
- Add logging for this case
- Improve error messages
- Add validation if needed

---

## Philosophy on AI Assistance

This project *uses* AI (OpenAI API) to *help small businesses* create marketing plans. It's practical, actionable work.

When helping with this project:
- **Respect the conversational flow**: Changes to questions affect the entire user experience
- **Value specificity**: Generic marketing advice isn't helpful - plans must be tailored
- **Test your suggestions**: If you'd suggest code, trace through what would actually happen
- **Understand the user journey**: From category selection → answering questions → getting actionable plan is the magic

---

## Quick Reference

**Start local dev:**
```bash
# Terminal 1 - Backend (runs on port 5000)
cd backend
python3 app.py

# Terminal 2 - Frontend (runs on port 3001)
cd frontend
npm start
```

**Note**: Backend runs on port 5000, frontend on port 3001 to avoid conflicts. Frontend proxies API calls to backend during development.

**Deploy to Render:**
```bash
git add .
git commit -m "description"
git push origin main
# Render auto-deploys
```

**Update question flows:**
Edit `backend/chat_flows.py`, then:
```bash
git add backend/chat_flows.py
git commit -m "Updated question flows"
git push
```

**Check logs:**
- Local: Terminal output
- Render: Dashboard → Service → Logs tab

---

## Final Notes

This is v2.0 - a complete transformation from meta-prompt generator to chat-based marketing tool. The focus is on:

**Can we help small businesses create actionable marketing plans through a simple, conversational interface?**

That's the experiment. The code is just the apparatus.

When helping, optimize for *usefulness* not *complexity*. We want to know:
- Do businesses find the plans actionable?
- Which categories produce the best results?
- What questions are most valuable?
- Where do users drop off?
- How can we make plans more specific and useful?

Help us learn. That's more valuable than any feature.

---

## Project History & Migration

This project was migrated from a meta-prompt generator to a chat-based marketing tool. The migration documentation is preserved in the `/docs` folder for reference:

- **docs/ARCHITECTURE_PLAN.md** - Complete architecture planning from Phase 0
- **docs/PHASE_0_SUMMARY.md** - Quick reference for new structure
- **docs/PHASE_1_COMPLETE.md** through **docs/PHASE_9_COMPLETE.md** - Phase-by-phase implementation details
- **docs/FIX_CONNECTION_ISSUE.md** - Troubleshooting guide for port conflicts

### Migration Summary

**Original System**: Meta-prompt generator that created prompt templates for users to fill out  
**Current System**: Chat-based marketing plan generator that directly creates actionable plans

**Key Transformation**:
- Replaced form-based flow with conversational chat interface
- Added structured question flows for 5 business categories
- Implemented budget-aware recommendations
- Enhanced with category-specific marketing intelligence
- Added industry insights and best practices

The migration was completed in 10 phases, with each phase building on the previous one. All old code has been removed or archived, and the system now operates as a complete chat-based marketing tool.

---

**Last Updated**: 2025-11-06
**Version**: 2.0
**Status**: Chat-based marketing tool / Production ready
