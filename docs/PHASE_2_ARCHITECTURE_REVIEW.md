# Phase 2 Architecture & Engineering Review

## Executive Summary

**Status**: ✅ **APPROVED - Architecture Clarified**

The Phase 2 plan is sound and architecture is now fully understood. The core concept (pre-generating templates) is excellent and will achieve the stated cost savings. Templates serve a dual purpose: providing sidebar form questions AND chat context.

---

## 🏗️ Architecture Review

### ✅ Clarified Architecture (Post-Discussion)

**Key Understanding**: Templates are NOT replacing `chat_flows.py` - they're a NEW parallel system that provides:
1. **Sidebar Form Questions**: From `USER_QUESTIONS` section → rendered as form fields
2. **Chat Context**: From `PROMPT_TEMPLATE` section → filled with form answers → sent as JSON with chat messages
3. **Opening Dialog**: Light acknowledgment message from template

### ✅ Complete User Flow

**Main Flow (Pre-generated Template):**
1. User selects question/theme → "I need help writing an elevator pitch for my business"
2. System checks: Is this a known question? → Yes → Load pre-generated template
3. Show chat interface + sidebar form:
   - **Chat**: Opening dialog from template (light acknowledgment)
   - **Sidebar**: Form fields from template's `USER_QUESTIONS` (with placeholders + "use this" buttons)
4. User interaction:
   - Fills form fields OR types in chat OR both
   - Form validation: Allow partial answers (no blocking)
5. When user sends chat message:
   - Embed form answers as JSON into chat prompt
   - Send: `{user_message, form_answers: {question_id: answer}}`
6. AI processes:
   - Sees chat + form answers (JSON)
   - Asks for missing required info OR proceeds if complete
7. AI generates outcome (defined in later phase)

**Dynamic Flow (On-demand Generation):**
1. User asks NEW question (not in templates)
2. Use `meta-prompt-system.md` to generate template on-demand
3. Proceed with chat + sidebar form (same as above)

### ✅ Template Structure (Clarified)

```json
{
  "category": "elevator_pitch",  // or question_id
  "opening_dialog": "Hi! I'm here to help you write an elevator pitch...",
  "anti_patterns": ["Common pattern 1", "Common pattern 2"],
  "prompt_template": "Role: ... Variables: {{business_name}}, {{target_audience}}...",
  "questions": [
    {
      "id": "business_name",
      "question": "What's your business name?",
      "type": "text",
      "placeholder": "e.g., Acme Corp",
      "required": true,
      "why_matters": "Personalizes the pitch"
    }
  ]
}
```

**Usage:**
- `opening_dialog` → Chat opening message
- `questions` → Sidebar form fields (with placeholders + "use this" buttons)
- `prompt_template` → Context for AI (filled with form answers as JSON)

**Chat Message Format:**
```json
{
  "user_message": "I'm done filling out the form",
  "form_answers": {
    "business_name": "Acme Corp",
    "target_audience": "Small business owners",
    "budget": "$500-1000"
  }
}
```

### ✅ Integration Strategy (Clarified)

**Templates are a NEW system, not replacing `chat_flows.py`:**
- Templates provide sidebar form + chat context
- `chat_flows.py` remains for existing marketing plan flow (may be deprecated later)
- Templates are loaded when user selects a question/theme
- Form answers are embedded as JSON when user sends chat message
- Form updates only sent on new message (save tokens)

---

#### 2. **Template Data Model (Clarified)**

**Template Structure** (Phase 2):
```json
{
    "id": "business_name",
    "question": "What's your business name?",
    "type": "text",  // text, textarea, select
    "placeholder": "e.g., Acme Corp",
    "required": true,
    "why_matters": "Personalizes the pitch",
    "options": []  // Only for select type
}
```

**Key Features:**
- `placeholder` → Shown in form field, with "use this" button to populate
- `why_matters` → Explanation for user (shown in form)
- `required` → Validation (but doesn't block chat)
- `options` → For select type questions

**No transformation needed** - Templates are used directly for:
1. Rendering sidebar form fields
2. Embedding answers as JSON in chat context

---

#### 3. **Versioning & Rollback Strategy**

**Problem**: No mechanism to handle template versioning or rollback if generated templates are inferior.

**Recommendation**:
```python
# Template structure should include version
{
    "category": "restaurant",
    "version": "1.0.0",
    "meta_prompt_version": "v1.0",
    "generated_at": "2025-01-06T10:00:00Z",
    "generated_by": "generate_templates.py",
    ...
}

# Template loader should support version selection
def load_template(category: str, version: str = "latest") -> Optional[dict]:
    """Load specific version or latest"""
    if version == "latest":
        # Find latest version
        pass
    else:
        # Load specific version
        pass

# Keep backup of previous versions
# prompts/generated_templates/restaurant/
#   - v1.0.0.json
#   - v1.0.1.json
#   - latest.json (symlink)
```

**Action Required**: Add versioning to template structure and loader.

---

#### 4. **Template Validation Gaps**

**Problem**: Validation function exists but doesn't verify compatibility with `chat_flows.py`.

**Current Validation** (from plan):
- Check required fields present
- Verify questions have IDs, text, types
- Ensure no duplicate question IDs
- Verify all {{variables}} in template match question IDs

**Missing Validations**:
- Structure matches `chat_flows.py` format
- All required fields for runtime compatibility
- Type values are valid (`text`, `textarea`, `select`)
- Select questions have `options` array
- Question IDs are valid Python identifiers

**Recommendation**:
```python
def validate_template_for_runtime(template: dict) -> tuple[bool, list[str]]:
    """
    Validate template is compatible with chat_flows.py runtime.
    Returns (is_valid, error_messages)
    """
    errors = []
    
    # Check structure
    if "questions" not in template:
        errors.append("Missing 'questions' array")
        return False, errors
    
    # Validate each question
    question_ids = set()
    for q in template["questions"]:
        # Check required fields
        required = ["id", "question", "type"]
        for field in required:
            if field not in q:
                errors.append(f"Question missing required field: {field}")
        
        # Check ID uniqueness
        if q["id"] in question_ids:
            errors.append(f"Duplicate question ID: {q['id']}")
        question_ids.add(q["id"])
        
        # Check type validity
        if q["type"] not in ["text", "textarea", "select"]:
            errors.append(f"Invalid question type: {q['type']}")
        
        # Check select has options
        if q["type"] == "select" and "options" not in q:
            errors.append(f"Select question '{q['id']}' missing 'options'")
    
    return len(errors) == 0, errors
```

**Action Required**: Enhance validation to ensure runtime compatibility.

---

## 🔧 Engineering Review

### ⚠️ Critical Issues

#### 1. **Missing Dependencies**

**Problem**: `pandas` and `openpyxl` mentioned but not in `requirements.txt`.

**Current `requirements.txt`**:
```
flask==2.3.3
flask-cors==4.0.0
python-dotenv==1.0.0
openai>=1.6.1
gunicorn==21.2.0
```

**Recommendation**:
```txt
# Add to requirements.txt (optional dependencies for scripts)
pandas>=2.0.0  # For SMB data loading (optional)
openpyxl>=3.1.0  # For Excel reading (optional)
```

**Alternative**: Make SMB data loader optional with graceful fallback if Excel file not found.

**Action Required**: Add dependencies or make SMB loader optional.

---

#### 2. **Error Handling Gaps**

**Problem**: Script needs robust error handling for production use.

**Missing Error Handling**:
- OpenAI API rate limits
- Network timeouts
- Partial failures (some categories succeed, others fail)
- Invalid API responses
- File I/O errors

**Recommendation**:
```python
# generate_templates.py should have:
import logging
from typing import Dict, List
from openai import OpenAI, RateLimitError, APIError

logger = logging.getLogger(__name__)

def generate_template_for_category(category: str, config: dict, max_retries: int = 3) -> Optional[dict]:
    """Generate template with retry logic"""
    for attempt in range(max_retries):
        try:
            # Generate template
            return _generate_single_template(category, config)
        except RateLimitError as e:
            wait_time = 2 ** attempt  # Exponential backoff
            logger.warning(f"Rate limit hit for {category}, waiting {wait_time}s")
            time.sleep(wait_time)
        except APIError as e:
            logger.error(f"API error for {category}: {e}")
            if attempt == max_retries - 1:
                raise
            time.sleep(1)
        except Exception as e:
            logger.error(f"Unexpected error for {category}: {e}")
            raise
    
    return None

def generate_all_templates(categories: Dict, continue_on_error: bool = True) -> Dict[str, bool]:
    """Generate templates for all categories, return success status"""
    results = {}
    for category, config in categories.items():
        try:
            template = generate_template_for_category(category, config)
            if template:
                save_template(category, template)
                results[category] = True
            else:
                results[category] = False
        except Exception as e:
            logger.error(f"Failed to generate template for {category}: {e}")
            results[category] = False
            if not continue_on_error:
                raise
    
    return results
```

**Action Required**: Add comprehensive error handling and retry logic.

---

#### 3. **Testing Strategy Missing**

**Problem**: No way to test template generation without calling OpenAI API.

**Recommendation**:
```python
# Add mock mode for testing
def generate_template_for_category(category: str, config: dict, mock: bool = False) -> Optional[dict]:
    """Generate template, with optional mock mode for testing"""
    if mock:
        return _generate_mock_template(category, config)
    else:
        return _generate_real_template(category, config)

def _generate_mock_template(category: str, config: dict) -> dict:
    """Return mock template for testing"""
    return {
        "category": category,
        "version": "1.0.0",
        "anti_patterns": ["Mock pattern 1", "Mock pattern 2"],
        "prompt_template": "Mock template for {{category}}",
        "questions": [
            {
                "id": "business_name",
                "question": "What's your business name?",
                "type": "text",
                "required": True,
                "why_matters": "Mock explanation"
            }
        ]
    }
```

**Action Required**: Add mock mode for testing without API calls.

---

#### 4. **Logging & Observability**

**Problem**: Script needs comprehensive logging for debugging.

**Recommendation**:
```python
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('template_generation.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def generate_all_templates(categories: Dict):
    """Generate with comprehensive logging"""
    logger.info(f"Starting template generation for {len(categories)} categories")
    start_time = datetime.now()
    
    results = {}
    for category, config in categories.items():
        logger.info(f"Generating template for category: {category}")
        try:
            # ... generation logic ...
            logger.info(f"Successfully generated template for {category}")
            results[category] = True
        except Exception as e:
            logger.error(f"Failed to generate template for {category}: {e}", exc_info=True)
            results[category] = False
    
    duration = (datetime.now() - start_time).total_seconds()
    logger.info(f"Template generation complete. Duration: {duration}s. Success: {sum(results.values())}/{len(results)}")
    
    return results
```

**Action Required**: Add comprehensive logging throughout.

---

#### 5. **Configuration Management**

**Problem**: API key and configuration should be managed properly.

**Recommendation**:
```python
# Use environment variables
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found in environment")

# Configuration file for categories
# backend/config/template_categories.json
{
    "restaurant": {
        "user_domain": "...",
        "user_framing": "..."
    },
    ...
}

# Load from config file
def load_category_configs() -> Dict:
    """Load category configurations from file"""
    config_path = os.path.join(os.path.dirname(__file__), 'config', 'template_categories.json')
    with open(config_path, 'r') as f:
        return json.load(f)
```

**Action Required**: Use environment variables and config files.

---

## 📋 Recommended Implementation Order

### Step 1: Architecture Decisions (30 min)
1. ✅ Define integration strategy (template-first vs. fallback)
2. ✅ Define data model mapping (template → runtime format)
3. ✅ Design versioning system
4. ✅ Plan rollback mechanism

### Step 2: Foundation (1 hour)
1. ✅ Create `backend/scripts/` directory
2. ✅ Add dependencies to `requirements.txt` (or make optional)
3. ✅ Create configuration file for categories
4. ✅ Set up logging infrastructure

### Step 3: Core Scripts (2 hours)
1. ✅ Create `template_parser.py` with robust parsing
2. ✅ Create `smb_data_loader.py` with graceful fallback
3. ✅ Create `generate_templates.py` with error handling
4. ✅ Create `template_loader.py` with versioning support

### Step 4: Integration Layer (1 hour)
1. ✅ Create template loader for runtime (load templates for sidebar + chat)
2. ✅ Create form answer serializer (convert form answers to JSON for chat)
3. ✅ Update chat API to accept form answers with messages

### Step 5: Testing & Validation (1 hour)
1. ✅ Add mock mode for testing
2. ✅ Create validation tests
3. ✅ Test integration with existing system
4. ✅ Generate real templates (one-time)

### Step 6: Documentation (30 min)
1. ✅ Document template format
2. ✅ Document integration approach
3. ✅ Document rollback procedure

---

## ✅ Approval Checklist

Before starting implementation, ensure:

- [x] Integration strategy defined (templates provide sidebar form + chat context)
- [x] Data model documented (template structure for form + chat)
- [x] User flow understood (form answers embedded as JSON in chat)
- [ ] Versioning system designed
- [ ] Error handling strategy defined
- [ ] Testing approach defined (mock mode)
- [ ] Dependencies added to requirements.txt (or made optional)
- [ ] Logging infrastructure set up
- [ ] Configuration management decided
- [ ] Rollback procedure documented

---

## 🎯 Final Recommendation

**APPROVE Phase 2** with the following modifications:

1. **Add integration layer** between templates and `chat_flows.py`
2. **Add versioning** to templates
3. **Enhance error handling** with retries and graceful failures
4. **Add mock mode** for testing
5. **Make SMB loader optional** (graceful fallback)
6. **Add comprehensive logging**
7. **Define rollback strategy**

**Estimated Time**: 4-5 hours (vs. original 2 hours) due to additional robustness requirements.

---

**Reviewer**: System Architect & Senior Engineer  
**Date**: 2025-11-06  
**Updated**: 2025-11-06 (Architecture clarified after discussion)  
**Status**: ✅ Approved - Ready for Implementation

---

## 📝 Architecture Clarifications (Post-Discussion)

### Key Decisions Made:

1. **Templates serve dual purpose**: Sidebar form questions + Chat context
2. **Form validation**: Allow partial answers, don't block chat
3. **Form updates**: Only sent on new message (save tokens)
4. **Chat opening**: Comes from template (light acknowledgment)
5. **Form answers format**: JSON embedded in chat message
6. **Placeholders**: Show in form fields with "use this" button/icon
7. **Security**: JSON format for form answers (security considerations in Phase 3)

### Implementation Notes:

- Templates are NEW system, not replacing `chat_flows.py`
- Templates loaded when user selects question/theme
- Form answers serialized as JSON when user sends chat message
- AI sees both chat message AND form answers (JSON) in context

