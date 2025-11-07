"""
Security Module

Provides comprehensive security for the application including:
- Input validation and sanitization
- Prompt injection detection
- Rate limiting with blocking
- Session management with IP validation
- System prompt protection
"""

from .input_validator import (
    detect_prompt_injection,
    sanitize_input,
    validate_message
)
from .rate_limiter import RateLimiter
from .session_manager import SessionManager
from .system_prompt_wrapper import create_protected_system_prompt

# Import legacy functions from old security.py for backward compatibility
# These will be migrated to use the new modules
import re
import html
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from collections import defaultdict

def sanitize_string(text: str, max_length: int = 5000) -> str:
    """Legacy function - use sanitize_input from input_validator instead"""
    return sanitize_input(text, max_length=max_length, aggressive=True)

def sanitize_form_answers(form_answers: Dict) -> Dict[str, str]:
    """Sanitize form answers dictionary"""
    sanitized = {}
    for question_id, answer in form_answers.items():
        if not re.match(r'^[a-zA-Z0-9_]+$', question_id):
            continue
        if isinstance(answer, (int, float)):
            answer = str(answer)
        elif not isinstance(answer, str):
            answer = str(answer)
        sanitized[question_id] = sanitize_input(answer, max_length=2000, aggressive=True)
    return sanitized

def validate_question_ids(question_ids: List[str], template_questions: List[Dict]) -> Tuple[bool, List[str]]:
    """Validate that question IDs match template structure"""
    errors = []
    valid_ids = {q.get('id') for q in template_questions if 'id' in q}
    for qid in question_ids:
        if qid not in valid_ids:
            errors.append(f"Invalid question ID: {qid}")
    return len(errors) == 0, errors

def validate_json_structure(data: Dict, required_fields: List[str], optional_fields: List[str] = None) -> Tuple[bool, Optional[str]]:
    """Validate JSON structure has required fields"""
    if not isinstance(data, dict):
        return False, "Data must be a dictionary"
    for field in required_fields:
        if field not in data:
            return False, f"Missing required field: {field}"
    return True, None

def validate_category(category: str, valid_categories: List[str]) -> Tuple[bool, Optional[str]]:
    """Validate category is in allowed list"""
    if not category:
        return False, "Category is required"
    if category not in valid_categories:
        return False, f"Invalid category. Must be one of: {', '.join(valid_categories)}"
    return True, None

def validate_session_id(session_id: str) -> bool:
    """Validate session ID format (UUID)"""
    if not session_id:
        return False
    uuid_pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
    return bool(re.match(uuid_pattern, session_id.lower()))

_rate_limit_store: Dict[str, List[datetime]] = defaultdict(list)

def check_rate_limit(identifier: str, max_requests: int = 10, window_seconds: int = 60) -> Tuple[bool, Optional[str]]:
    """Legacy rate limiting - use RateLimiter class instead"""
    now = datetime.now()
    window_start = now - timedelta(seconds=window_seconds)
    requests = _rate_limit_store[identifier]
    requests[:] = [req_time for req_time in requests if req_time > window_start]
    if len(requests) >= max_requests:
        return False, f"Rate limit exceeded. Maximum {max_requests} requests per {window_seconds} seconds."
    requests.append(now)
    return True, None

def get_client_identifier(request) -> str:
    """Get client identifier for rate limiting"""
    if request.headers.get('X-Forwarded-For'):
        ip = request.headers.get('X-Forwarded-For').split(',')[0].strip()
    else:
        ip = request.remote_addr or 'unknown'
    return ip

def sanitize_for_ai(text: str) -> str:
    """Sanitize text before sending to AI (less aggressive than HTML sanitization)"""
    if not isinstance(text, str):
        text = str(text)
    text = text.strip()
    text = text.replace('\x00', '')
    text = re.sub(r'[\x00-\x08\x0B-\x0C\x0E-\x1F\x7F]', '', text)
    if len(text) > 10000:
        text = text[:10000]
    return text

def validate_form_answers_structure(form_answers: Dict, template_questions: List[Dict]) -> Tuple[bool, List[str]]:
    """Validate form answers structure matches template"""
    errors = []
    if not isinstance(form_answers, dict):
        errors.append("Form answers must be a dictionary")
        return False, errors
    valid_ids = {q.get('id') for q in template_questions if 'id' in q}
    for question_id, answer in form_answers.items():
        if not re.match(r'^[a-zA-Z0-9_]+$', question_id):
            errors.append(f"Invalid question ID format: {question_id}")
            continue
        if question_id not in valid_ids:
            errors.append(f"Question ID not found in template: {question_id}")
            continue
        question = next((q for q in template_questions if q.get('id') == question_id), None)
        if question and question.get('required', False):
            if not answer or (isinstance(answer, str) and not answer.strip()):
                errors.append(f"Required question '{question_id}' is empty")
    return len(errors) == 0, errors

__all__ = [
    'detect_prompt_injection',
    'sanitize_input',
    'validate_message',
    'RateLimiter',
    'SessionManager',
    'create_protected_system_prompt',
    # Legacy exports
    'sanitize_string',
    'sanitize_form_answers',
    'validate_question_ids',
    'validate_json_structure',
    'validate_category',
    'validate_session_id',
    'check_rate_limit',
    'get_client_identifier',
    'sanitize_for_ai',
    'validate_form_answers_structure'
]

