"""
Input Validator

Detects prompt injection attempts and sanitizes user input.
"""

import re
import html
from typing import Tuple, Optional


# Dangerous patterns that indicate prompt injection attempts
PROMPT_INJECTION_PATTERNS = [
    # Direct instruction overrides
    (r'(?i)ignore\s+(all\s+)?previous\s+instructions?', 'Attempt to override instructions'),
    (r'(?i)forget\s+(all\s+)?previous\s+instructions?', 'Attempt to clear context'),
    (r'(?i)disregard\s+(all\s+)?previous\s+instructions?', 'Attempt to ignore instructions'),
    (r'(?i)override\s+(all\s+)?previous\s+instructions?', 'Attempt to override system'),
    
    # Role manipulation
    (r'(?i)you\s+are\s+now\s+(a\s+)?(hacker|malicious|evil|bad)', 'Role manipulation attempt'),
    (r'(?i)act\s+as\s+(a\s+)?(hacker|malicious|evil|bad)', 'Role manipulation attempt'),
    (r'(?i)pretend\s+to\s+be\s+(a\s+)?(hacker|malicious|evil|bad)', 'Role manipulation attempt'),
    
    # System prompt extraction
    (r'(?i)(show|reveal|display|tell\s+me|give\s+me)\s+(me\s+)?(your\s+)?(system\s+)?(prompt|instructions?|directives?)', 'System prompt extraction attempt'),
    (r'(?i)what\s+are\s+your\s+(system\s+)?(prompt|instructions?|directives?)', 'System prompt extraction attempt'),
    (r'(?i)repeat\s+(your\s+)?(system\s+)?(prompt|instructions?|directives?)', 'System prompt extraction attempt'),
    (r'(?i)show\s+me\s+your', 'System prompt extraction attempt'),
    
    # Template variable exploitation
    (r'\{\{.*?system.*?\}\}', 'Template variable exploitation'),
    (r'\{\{.*?prompt.*?\}\}', 'Template variable exploitation'),
    (r'\{\{.*?instructions?.*?\}\}', 'Template variable exploitation'),
    
    # Code injection attempts
    (r'(?i)(execute|run|eval|exec)\s+', 'Code execution attempt'),
    (r'<script[^>]*>', 'Script injection attempt'),
    (r'javascript:', 'JavaScript injection attempt'),
    
    # Base64 encoded suspicious content
    (r'[A-Za-z0-9+/]{100,}={0,2}', 'Potential base64 encoded payload'),
]


def detect_prompt_injection(text: str) -> Tuple[bool, Optional[str]]:
    """
    Detect if text contains prompt injection patterns.
    
    Args:
        text: Input text to check
        
    Returns:
        Tuple of (is_dangerous, reason)
        - is_dangerous: True if dangerous pattern detected
        - reason: Description of the threat, or None if safe
    """
    if not isinstance(text, str):
        text = str(text)
    
    text_lower = text.lower()
    
    # Check for dangerous patterns
    for pattern, reason in PROMPT_INJECTION_PATTERNS:
        if re.search(pattern, text):
            return True, reason
    
    # Check for excessive special characters (potential obfuscation)
    special_char_count = len(re.findall(r'[^\w\s]', text))
    if len(text) > 0 and special_char_count / len(text) > 0.3:  # More than 30% special chars
        if special_char_count > 100:  # And more than 100 total
            return True, 'Excessive special characters (potential obfuscation)'
    
    # Check for null bytes
    if '\x00' in text:
        return True, 'Null byte injection attempt'
    
    return False, None


def sanitize_input(text: str, max_length: int = 5000, aggressive: bool = True) -> str:
    """
    Sanitize user input to prevent XSS and injection attacks.
    
    Args:
        text: Input text to sanitize
        max_length: Maximum allowed length
        aggressive: If True, HTML escape everything. If False, preserve more formatting.
        
    Returns:
        Sanitized text
    """
    if not isinstance(text, str):
        text = str(text)
    
    # Trim whitespace
    text = text.strip()
    
    # Limit length
    if len(text) > max_length:
        text = text[:max_length]
    
    # Remove null bytes
    text = text.replace('\x00', '')
    
    # Remove control characters (except newlines and tabs if not aggressive)
    if aggressive:
        # Remove all control characters
        text = re.sub(r'[\x00-\x08\x0B-\x0C\x0E-\x1F\x7F]', '', text)
        # HTML escape to prevent XSS
        text = html.escape(text)
    else:
        # Keep newlines and tabs, remove other control characters
        text = re.sub(r'[\x00-\x08\x0B-\x0C\x0E-\x1F\x7F]', '', text)
    
    return text


def validate_message(text: str, max_length: int = 5000) -> Tuple[bool, Optional[str]]:
    """
    Validate message for security and length.
    
    Args:
        text: Message text to validate
        max_length: Maximum allowed length
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not isinstance(text, str):
        return False, "Message must be a string"
    
    # Check length
    if len(text) > max_length:
        return False, f"Message is too long. Maximum {max_length} characters allowed."
    
    # Check for prompt injection
    is_dangerous, reason = detect_prompt_injection(text)
    if is_dangerous:
        return False, f"Message contains potentially harmful content: {reason}"
    
    # Check for empty after sanitization
    sanitized = sanitize_input(text, max_length=max_length, aggressive=False)
    if not sanitized.strip():
        return False, "Message cannot be empty"
    
    return True, None

