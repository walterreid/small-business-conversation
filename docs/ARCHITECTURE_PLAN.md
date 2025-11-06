# Architecture Plan: Meta-Prompt Generator → Chat-Based Marketing Tool

## Current State Analysis

### Existing Architecture
```
User Input (domain + framing)
    ↓
Flask Backend (/api/generate-template)
    ↓
OpenAI API (meta-prompt system)
    ↓
Structured Response ([ANTI-PATTERNS] [PROMPT_TEMPLATE] [USER_QUESTIONS])
    ↓
React Frontend (parses response)
    ↓
Dynamic Form (fills {{variables}})
    ↓
Final Prompt (for use elsewhere)
```

### Current File Structure
```
/
├── backend/
│   ├── app.py                    # Flask API with OpenAI integration
│   ├── requirements.txt          # Python dependencies
│   ├── prompts/
│   │   └── meta-prompt-system.md  # Meta-prompt template
│   └── .env                      # Environment variables
├── frontend/
│   ├── src/
│   │   ├── App.js                # Main React component (4-step flow)
│   │   ├── App.css               # Styling
│   │   ├── api.js                # API client
│   │   └── index.js
│   └── package.json
├── README.md
├── CLAUDE.md
└── DEPLOYMENT.md
```

---

## Target State: Chat-Based Marketing Tool

### New Architecture
```
User Selects Category
    ↓
Chat Interface (one question at a time)
    ↓
Flask Backend (/api/chat/* endpoints)
    ↓
Question Flow System (chat_flows.py)
    ↓
OpenAI Chat API (conversational)
    ↓
Marketing Plan Generation
```

### New File Structure
```
/
├── backend/
│   ├── app.py                    # ✅ MODIFY: Add chat routes, keep old routes
│   ├── chat_flows.py              # 🆕 CREATE: Question flows for each category
│   ├── chat_sessions.py          # 🆕 CREATE: Session management (optional)
│   ├── requirements.txt           # ✅ MODIFY: Add any new deps
│   ├── prompts/
│   │   ├── meta-prompt-system.md  # ⚠️ KEEP: For reference, may archive later
│   │   └── marketing-plan-prompt.md # 🆕 CREATE: Marketing plan generation prompt
│   └── data/
│       └── smb_stats.xlsx         # 🆕 ADD: Small business data (if provided)
├── frontend/
│   ├── src/
│   │   ├── App.js                # ✅ MODIFY: Replace flow with chat flow
│   │   ├── App.css               # ✅ MODIFY: Add chat styles
│   │   ├── api.js                # ✅ MODIFY: Add chat API functions
│   │   ├── components/           # 🆕 CREATE: New components folder
│   │   │   ├── ChatInterface.js   # 🆕 CREATE: Main chat UI
│   │   │   ├── ChatMessage.js     # 🆕 CREATE: Individual message bubble
│   │   │   ├── CategorySelector.js # 🆕 CREATE: Business category picker
│   │   │   └── MarketingPlanView.js # 🆕 CREATE: Final plan display
│   │   ├── styles/               # 🆕 CREATE: Separate styles
│   │   │   ├── ChatApp.css       # 🆕 CREATE: Chat-specific styles
│   │   │   └── CategorySelector.css # 🆕 CREATE: Category selector styles
│   │   └── api/
│   │       └── chatApi.js        # 🆕 CREATE: Chat API client
│   └── package.json              # ✅ MODIFY: Add react-router if needed
├── README.md                     # ✅ MODIFY: Update for new flow
├── CLAUDE.md                     # ✅ MODIFY: Update architecture docs
└── DEPLOYMENT.md                 # ✅ MODIFY: Update if needed
```

---

## Files to CREATE (New Components)

### Backend Files

#### 1. `backend/chat_flows.py` ⭐ **CRITICAL**
**Purpose**: Define question sequences for each business category
**Structure**:
```python
QUESTION_FLOWS = {
    "restaurant": [
        {"id": "business_name", "question": "...", "type": "text"},
        {"id": "cuisine_type", "question": "...", "type": "text"},
        # ... more questions
    ],
    "retail_store": [...],
    "professional_services": [...],
    "ecommerce": [...],
    "local_services": [...]
}

def get_next_question(category, answered_questions):
    """Returns next unanswered question or None if complete"""
    
def generate_marketing_plan_prompt(category, answers):
    """Builds prompt for OpenAI to generate marketing plan"""
```

#### 2. `backend/chat_sessions.py` (Optional for Phase 2-4)
**Purpose**: Session management (can use in-memory dict initially)
**Structure**:
```python
SESSIONS = {}  # {session_id: {category, answers, conversation_history}}

def create_session(category):
    """Create new session, return session_id"""
    
def get_session(session_id):
    """Retrieve session data"""
    
def update_session(session_id, question_id, answer):
    """Store answer and update conversation"""
```

#### 3. `backend/prompts/marketing-plan-prompt.md` (Phase 8)
**Purpose**: Template for generating marketing plans
**Content**: Structured prompt that uses collected answers + SMB data

#### 4. `backend/data/smb_stats.xlsx` (Phase 8)
**Purpose**: Small business statistics and insights
**Note**: User will provide this file

---

### Frontend Files

#### 1. `frontend/src/components/ChatInterface.js` ⭐ **CRITICAL**
**Purpose**: Main chat UI component
**Features**:
- Message history display
- Text input with send button
- Typing indicator
- Auto-scroll to bottom
- Session management

#### 2. `frontend/src/components/ChatMessage.js`
**Purpose**: Individual message bubble
**Features**:
- User vs AI message styling
- Markdown support for AI responses
- Timestamp (optional)
- Avatar icons

#### 3. `frontend/src/components/CategorySelector.js` ⭐ **CRITICAL**
**Purpose**: Business category selection screen
**Features**:
- Card-based selection (like Bridesmaid for Hire)
- Categories: Restaurant, Retail Store, Professional Services, E-commerce, Local Services
- Visual icons
- Hover/selected states

#### 4. `frontend/src/components/MarketingPlanView.js`
**Purpose**: Display final marketing plan
**Features**:
- Formatted plan display
- Copy to clipboard
- Download option
- Feedback buttons

#### 5. `frontend/src/styles/ChatApp.css`
**Purpose**: Chat-specific styling
**Features**:
- Message bubble styles
- Input area styling
- Typing indicator animation
- Mobile responsive

#### 6. `frontend/src/styles/CategorySelector.css`
**Purpose**: Category selector styling
**Features**:
- Card grid layout
- Hover effects
- Selected state styling

#### 7. `frontend/src/api/chatApi.js` ⭐ **CRITICAL**
**Purpose**: Chat API client functions
**Functions**:
- `startChatSession(category)`
- `sendChatMessage(sessionId, message)`
- `generateMarketingPlan(sessionId)`
- `getChatSession(sessionId)`

---

## Files to MODIFY (Existing Code)

### Backend

#### `backend/app.py`
**Changes**:
- ✅ **KEEP**: Existing routes (`/api/generate-template`, `/health`, `/api/feedback`, `/api/try-prompt`)
- 🆕 **ADD**: New chat routes:
  - `POST /api/chat/start`
  - `POST /api/chat/message`
  - `POST /api/chat/generate-plan`
  - `GET /api/chat/session/:session_id`
- ✅ **KEEP**: OpenAI client initialization
- ✅ **KEEP**: CORS configuration
- ✅ **KEEP**: Error handling patterns

**Strategy**: Add new routes without breaking existing ones. Can comment out old routes later.

---

### Frontend

#### `frontend/src/App.js`
**Changes**:
- ✅ **KEEP**: Error handling utilities (reuse pattern)
- ✅ **KEEP**: State management patterns
- 🔄 **REPLACE**: 4-step flow with 3-step chat flow:
  - Step 1: Category selection (new)
  - Step 2: Chat interface (new)
  - Step 3: Marketing plan result (adapted from Step 4)
- ⚠️ **ARCHIVE**: Old parsing logic (keep commented for reference)
- ⚠️ **ARCHIVE**: Old form rendering (keep commented for reference)

**Strategy**: Comment out old code, add new flow. Can delete later in Phase 10.

#### `frontend/src/App.css`
**Changes**:
- ✅ **KEEP**: CSS variables (reuse for chat)
- ✅ **KEEP**: Gradient themes
- 🆕 **ADD**: Chat-specific styles (or import from ChatApp.css)
- ⚠️ **ARCHIVE**: Old form styles (comment out)

#### `frontend/src/api.js`
**Changes**:
- ✅ **KEEP**: Existing functions (for backward compatibility)
- 🆕 **ADD**: Import/export chat API functions
- **OR**: Create separate `chatApi.js` and keep `api.js` for old flow

**Strategy**: Create new `chatApi.js`, keep `api.js` intact for now.

---

## Files to REUSE (No Changes)

### Backend
- ✅ `backend/requirements.txt` - May need to add pandas for Excel (Phase 8)
- ✅ `backend/.env` - Same environment variables
- ✅ `backend/prompts/meta-prompt-system.md` - Keep for reference

### Frontend
- ✅ `frontend/package.json` - May add react-router-dom if needed
- ✅ `frontend/src/index.js` - No changes needed

### Documentation
- ✅ `README.md` - Update in Phase 10
- ✅ `CLAUDE.md` - Update in Phase 10
- ✅ `DEPLOYMENT.md` - Minimal changes needed

---

## Migration Strategy

### Phase-by-Phase Approach

**Phase 1-2**: Build new components alongside old code
- Create new components in `components/` folder
- Add new routes to `app.py`
- Old flow still works

**Phase 3-5**: Integrate new flow
- Connect chat components to backend
- Test new flow independently

**Phase 6**: Switch main flow
- Update `App.js` to use chat flow
- Old flow accessible via commented code

**Phase 10**: Cleanup
- Remove old code
- Update documentation
- Archive old prompts

---

## Key Design Decisions

### 1. **Keep Old Code Initially**
- Comment out, don't delete
- Allows rollback if needed
- Reference for patterns

### 2. **Separate Chat API**
- New `chatApi.js` file
- Keeps concerns separated
- Easier to test

### 3. **Component-Based Frontend**
- New `components/` folder
- Reusable chat components
- Easier to maintain

### 4. **Session Management**
- Start with in-memory dict
- Can upgrade to database later
- Simple for MVP

### 5. **Question Flow System**
- Centralized in `chat_flows.py`
- Easy to modify questions
- Category-specific logic

---

## Dependencies to Add

### Backend (Phase 8)
- `pandas` - For reading Excel file
- `openpyxl` - Excel file support

### Frontend (Optional)
- `react-router-dom` - If using URL routing
- `react-markdown` - For markdown in chat messages

---

## Testing Strategy

### Incremental Testing
1. **Phase 1**: Test UI components in isolation
2. **Phase 2**: Test API endpoints with curl/Postman
3. **Phase 5**: Test full chat flow
4. **Phase 9**: End-to-end testing

### Test Cases
- Category selection → Chat start
- Question flow (all questions answered)
- Marketing plan generation
- Error handling (network, API failures)
- Session persistence (refresh page)
- Mobile responsiveness

---

## Next Steps

1. ✅ **Phase 0 Complete**: Architecture planned
2. → **Phase 1**: Create chat UI components
3. → **Phase 2**: Add chat backend routes
4. → Continue through phases sequentially

---

## Notes

- **Backward Compatibility**: Old flow remains functional during transition
- **Rollback Plan**: All old code commented, not deleted
- **Performance**: In-memory sessions fine for MVP, can scale later
- **Data**: SMB Excel file will be provided in Phase 8

---

**Created**: Phase 0 - Architecture Planning
**Status**: Ready for Phase 1 implementation

