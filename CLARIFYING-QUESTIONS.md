# Implementation Plan - Confirmed

## System Configuration

### 1. Diagnostic Flow Placement
- Make diagnostic the default entry point
- Add prominent "Skip diagnostic, browse all 30 questions →" button
- If skipped, go to current MarketingGoalSelector (browse all)
- Diagnostic completion leads to MatchedQuestions component

### 2. System Scope
- Diagnostic works ONLY with template-based questions from:
  `/backend/prompts/generated_templates/`
- Ignore questions from `chat_flows.py` (old system)
- Load all question_*.json files from all category subdirectories
- Filter by these categories only:
  - increase_sales
  - build_brand_awareness
  - drive_foot_traffic
  - generate_leads
  - launch_new_product
  - retain_customers

### 3. Expert Sidebar Display Logic
- Show expert sidebar ONLY when:
  - `uses_template === true` (template-based question)
  - AND `framework_insights` is available
- Hide expert sidebar for:
  - chat_flows-based questions
  - Questions without framework insights

## File Structure

Create these new files:
```
backend/
  diagnostic_engine.py          # NEW
  
frontend/src/
  components/
    DiagnosticFlow.js            # NEW
    MatchedQuestions.js          # NEW
    ExpertSidebar.js             # NEW
  styles/
    DiagnosticFlow.css           # NEW
    MatchedQuestions.css         # NEW
    ExpertSidebar.css            # NEW
```

Modify these existing files:
```
backend/
  app.py                         # ADD diagnostic endpoints
  
frontend/src/
  App.js                         # ADD diagnostic flow step
  components/
    ChatInterface.js             # ADD expert sidebar integration
    MarketingPlanView.js         # ADD framework showcase
  api/
    chatApi.js                   # ADD runDiagnostic()
```

## Implementation Phases

### Phase 1: Diagnostic Funnel
1. Create `backend/diagnostic_engine.py`
   - Load only template-based questions
   - Implement matching logic
2. Add endpoints to `backend/app.py`
   - `/api/diagnostic` (POST)
   - `/api/questions/all` (GET) - template questions only
3. Create `frontend/src/components/DiagnosticFlow.js`
   - 3-step diagnostic UI
   - Skip option prominent
4. Create `frontend/src/components/MatchedQuestions.js`
   - Display top 3 matches
   - Browse all option
5. Update `frontend/src/App.js`
   - Add diagnostic as step 0
   - Keep existing browse-all flow
6. Add `runDiagnostic()` to `frontend/src/api/chatApi.js`
7. Create CSS files

### Phase 2: Progressive Transparency
1. Add to `backend/app.py`:
   - `extract_framework_insights()`
   - `determine_budget_tier()`
   - `load_question_template()`
   - Update `/api/chat/message` to return framework_insights
2. Create `frontend/src/components/ExpertSidebar.js`
   - Display framework insights
   - Collapsible sidebar
3. Update `frontend/src/components/ChatInterface.js`
   - Integrate ExpertSidebar
   - Show only when uses_template === true
4. Create `frontend/src/styles/ExpertSidebar.css`

### Phase 3: Enhanced Results
1. Update `frontend/src/components/MarketingPlanView.js`
   - Add framework metadata box
   - Add "Why This is Better" section
2. Update `frontend/src/styles/MarketingPlanView.css`

## Key Implementation Details

### Diagnostic Categories Mapping
```python
DIAGNOSTIC_MAPPINGS = {
    "not_enough_customers": {
        "priority_categories": ["increase_sales", "generate_leads", "drive_foot_traffic"],
        "keywords": ["sales", "customers", "traffic", "leads"]
    },
    "no_visibility": {
        "priority_categories": ["build_brand_awareness", "drive_foot_traffic"],
        "keywords": ["brand", "awareness", "visibility", "know"]
    },
    "cant_keep_customers": {
        "priority_categories": ["retain_customers"],
        "keywords": ["retain", "loyalty", "repeat", "churn"]
    },
    "launching_something": {
        "priority_categories": ["launch_new_product"],
        "keywords": ["launch", "new", "product", "service"]
    }
}
```

### Template Detection
```python
# In backend/app.py - startChatSession
def start_chat_session():
    # ... existing code ...
    
    # Check if using template
    template = load_question_template(category, question_number)
    uses_template = template is not None
    
    return {
        'success': True,
        'session_id': session_id,
        'uses_template': uses_template,  # NEW
        'questions': template.get('questions', []) if uses_template else [],
        'anti_patterns': template.get('anti_patterns', []) if uses_template else [],
        # ... rest of response ...
    }
```

### Expert Sidebar Conditional Render
```javascript
// In ChatInterface.js
{showExpertSidebar && frameworkInsights && (
  
)}
```

## Testing Checklist

### Phase 1 Tests
- [ ] Diagnostic flow completes successfully
- [ ] Top 3 questions are relevant
- [ ] Skip button goes to browse-all
- [ ] Matched questions show reasoning
- [ ] Browse-all still works independently
- [ ] Only template questions appear in matches

### Phase 2 Tests
- [ ] Expert sidebar appears for template questions only
- [ ] Expert sidebar hidden for chat_flows questions
- [ ] Framework insights update in real-time
- [ ] Budget tier detection works correctly
- [ ] Anti-patterns display at right times
- [ ] Sidebar collapse/expand works

### Phase 3 Tests
- [ ] Framework metadata displays correctly
- [ ] "Why This is Better" section is compelling
- [ ] Copy/download functionality still works

## Error Handling

1. **If diagnostic fails:**
   - Fallback to browse-all (MarketingGoalSelector)
   - Show user-friendly error message

2. **If no questions match:**
   - Show default top 3 questions
   - Explain no perfect match found

3. **If framework insights fail:**
   - Chat still works
   - Sidebar shows skeleton or hides

4. **If template not found:**
   - Fallback to chat_flows if available
   - Don't show expert sidebar

## Success Criteria

Each phase is complete when:
- [ ] No console errors
- [ ] Mobile responsive
- [ ] Accessible (keyboard nav)
- [ ] Matches mockup design
- [ ] All tests pass
- [ ] Error states handled
- [ ] Performance acceptable (<3s)