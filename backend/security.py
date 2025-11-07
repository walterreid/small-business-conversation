"""
Security Module

Provides input validation, sanitization, and rate limiting for the application.
"""

import re
import html
import json
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from collections import defaultdict


# Rate limiting storage (in-memory, can be upgraded to Redis later)
_rate_limit_store: Dict[str, List[datetime]] = defaultdict(list)


def sanitize_string(text: str, max_length: int = 5000) -> str:
    """
    Sanitize user input string.
    
    Args:
        text: Input string to sanitize
        max_length: Maximum allowed length
        
    Returns:
        Sanitized string
    """
    if not isinstance(text, str):
        text = str(text)
    
    # Trim whitespace
    text = text.strip()
    
    # Limit length
    if len(text) > max_length:
        text = text[:max_length]
    
    # Escape HTML to prevent XSS
    text = html.escape(text)
    
    # Remove null bytes
    text = text.replace('\x00', '')
    
    # Remove control characters (except newlines and tabs)
    text = re.sub(r'[\x00-\x08\x0B-\x0C\x0E-\x1F\x7F]', '', text)
    
    return text


def sanitize_form_answers(form_answers: Dict) -> Dict[str, str]:
    """
    Sanitize form answers dictionary.
    
    Args:
        form_answers: Dictionary of question_id -> answer
        
    Returns:
        Sanitized dictionary
    """
    sanitized = {}
    
    for question_id, answer in form_answers.items():
        # Validate question ID (alphanumeric and underscores only)
        if not re.match(r'^[a-zA-Z0-9_]+$', question_id):
            continue  # Skip invalid question IDs
        
        # Sanitize answer
        if isinstance(answer, (int, float)):
            answer = str(answer)
        elif not isinstance(answer, str):
            answer = str(answer)
        
        # Sanitize string (with reasonable length limit per field)
        sanitized[question_id] = sanitize_string(answer, max_length=2000)
    
    return sanitized


def validate_question_ids(question_ids: List[str], template_questions: List[Dict]) -> Tuple[bool, List[str]]:
    """
    Validate that question IDs match template structure.
    
    Args:
        question_ids: List of question IDs from form answers
        template_questions: List of question dictionaries from template
        
    Returns:
        Tuple of (is_valid, error_messages)
    """
    errors = []
    valid_ids = {q.get('id') for q in template_questions if 'id' in q}
    
    for qid in question_ids:
        if qid not in valid_ids:
            errors.append(f"Invalid question ID: {qid}")
    
    return len(errors) == 0, errors


def validate_json_structure(data: Dict, required_fields: List[str], optional_fields: List[str] = None) -> Tuple[bool, Optional[str]]:
    """
    Validate JSON structure has required fields.
    
    Args:
        data: JSON data to validate
        required_fields: List of required field names
        optional_fields: List of optional field names (for validation)
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not isinstance(data, dict):
        return False, "Data must be a dictionary"
    
    for field in required_fields:
        if field not in data:
            return False, f"Missing required field: {field}"
    
    # Check for unexpected fields (optional security measure)
    if optional_fields:
        all_allowed = set(required_fields) | set(optional_fields)
        unexpected = set(data.keys()) - all_allowed
        if unexpected:
            # Log but don't fail (for forward compatibility)
            pass
    
    return True, None


def validate_category(category: str, valid_categories: List[str]) -> Tuple[bool, Optional[str]]:
    """
    Validate category is in allowed list.
    
    Args:
        category: Category string to validate
        valid_categories: List of valid categories
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not category:
        return False, "Category is required"
    
    if category not in valid_categories:
        return False, f"Invalid category. Must be one of: {', '.join(valid_categories)}"
    
    return True, None


def validate_session_id(session_id: str) -> bool:
    """
    Validate session ID format (UUID).
    
    Args:
        session_id: Session ID string
        
    Returns:
        True if valid UUID format
    """
    if not session_id:
        return False
    
    # UUID format: 8-4-4-4-12 hex digits
    uuid_pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
    return bool(re.match(uuid_pattern, session_id.lower()))


def check_rate_limit(identifier: str, max_requests: int = 10, window_seconds: int = 60) -> Tuple[bool, Optional[str]]:
    """
    Check if request exceeds rate limit.
    
    Args:
        identifier: Unique identifier (IP address, session ID, etc.)
        max_requests: Maximum requests allowed
        window_seconds: Time window in seconds
        
    Returns:
        Tuple of (is_allowed, error_message)
    """
    now = datetime.now()
    window_start = now - timedelta(seconds=window_seconds)
    
    # Get request history for this identifier
    requests = _rate_limit_store[identifier]
    
    # Remove old requests outside window
    requests[:] = [req_time for req_time in requests if req_time > window_start]
    
    # Check if limit exceeded
    if len(requests) >= max_requests:
        return False, f"Rate limit exceeded. Maximum {max_requests} requests per {window_seconds} seconds."
    
    # Add current request
    requests.append(now)
    
    return True, None


def get_client_identifier(request) -> str:
    """
    Get client identifier for rate limiting.
    
    Args:
        request: Flask request object
        
    Returns:
        Client identifier string
    """
    # Try to get IP address
    if request.headers.get('X-Forwarded-For'):
        # Handle proxy headers
        ip = request.headers.get('X-Forwarded-For').split(',')[0].strip()
    else:
        ip = request.remote_addr or 'unknown'
    
    return ip


def sanitize_for_ai(text: str) -> str:
    """
    Sanitize text before sending to AI (less aggressive than HTML sanitization).
    
    Args:
        text: Text to sanitize
        
    Returns:
        Sanitized text safe for AI processing
    """
    if not isinstance(text, str):
        text = str(text)
    
    # Trim whitespace
    text = text.strip()
    
    # Remove null bytes
    text = text.replace('\x00', '')
    
    # Remove dangerous control characters but keep newlines/tabs
    text = re.sub(r'[\x00-\x08\x0B-\x0C\x0E-\x1F\x7F]', '', text)
    
    # Limit extremely long strings (but allow longer than HTML sanitization)
    if len(text) > 10000:
        text = text[:10000]
    
    return text


def validate_form_answers_structure(form_answers: Dict, template_questions: List[Dict]) -> Tuple[bool, List[str]]:
    """
    Validate form answers structure matches template.
    
    Args:
        form_answers: Dictionary of question_id -> answer
        template_questions: List of question dictionaries from template
        
    Returns:
        Tuple of (is_valid, error_messages)
    """
    errors = []
    
    if not isinstance(form_answers, dict):
        errors.append("Form answers must be a dictionary")
        return False, errors
    
    # Get valid question IDs from template
    valid_ids = {q.get('id') for q in template_questions if 'id' in q}
    
    # Check each answer
    for question_id, answer in form_answers.items():
        # Validate question ID format
        if not re.match(r'^[a-zA-Z0-9_]+$', question_id):
            errors.append(f"Invalid question ID format: {question_id}")
            continue
        
        # Check if question ID exists in template
        if question_id not in valid_ids:
            errors.append(f"Question ID not found in template: {question_id}")
            continue
        
        # Validate answer is not empty if required
        question = next((q for q in template_questions if q.get('id') == question_id), None)
        if question and question.get('required', False):
            if not answer or (isinstance(answer, str) and not answer.strip()):
                errors.append(f"Required question '{question_id}' is empty")
    
    return len(errors) == 0, errors


def create_safe_json_response(data: Dict) -> Dict:
    """
    Create safe JSON response (sanitize any user-provided data in response).
    
    Args:
        data: Response data dictionary
        
    Returns:
        Sanitized response dictionary
    """
    # Deep copy to avoid modifying original
    safe_data = json.loads(json.dumps(data))
    
    # Recursively sanitize string values
    def sanitize_value(value):
        if isinstance(value, str):
            return sanitize_string(value, max_length=10000)  # Longer limit for responses
        elif isinstance(value, dict):
            return {k: sanitize_value(v) for k, v in value.items()}
        elif isinstance(value, list):
            return [sanitize_value(item) for item in value]
        else:
            return value
    
    return sanitize_value(safe_data)

