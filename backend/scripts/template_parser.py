"""
Template Parser for Meta-Prompt Output

Parses the output from meta-prompt-system.md into structured JSON templates.
"""

import re
from typing import List, Dict, Optional, Tuple


def parse_anti_patterns(raw_output: str) -> List[str]:
    """
    Extract anti-patterns from [ANTI-PATTERNS] section.
    
    Args:
        raw_output: Raw output from OpenAI API
        
    Returns:
        List of anti-pattern strings
    """
    anti_patterns = []
    
    # Look for [ANTI-PATTERNS] section
    pattern = r'\[ANTI-PATTERNS?\]\s*\n(.*?)(?=\n\[|$)'
    match = re.search(pattern, raw_output, re.IGNORECASE | re.DOTALL)
    
    if not match:
        # Try alternative format: **ANTI-PATTERNS:**
        pattern = r'\*\*ANTI-PATTERNS?:\*\*\s*\n(.*?)(?=\n\*\*|$)'
        match = re.search(pattern, raw_output, re.IGNORECASE | re.DOTALL)
    
    if match:
        content = match.group(1).strip()
        # Extract lines starting with "- " or "* "
        lines = content.split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith('- ') or line.startswith('* '):
                # Remove bullet point
                pattern_text = line[2:].strip()
                if pattern_text:
                    anti_patterns.append(pattern_text)
    
    return anti_patterns


def parse_prompt_template(raw_output: str) -> str:
    """
    Extract template from [PROMPT_TEMPLATE] section.
    
    Args:
        raw_output: Raw output from OpenAI API
        
    Returns:
        Template string with {{variables}}
    """
    # Look for [PROMPT_TEMPLATE] section
    pattern = r'\[PROMPT_TEMPLATE\]\s*\n(.*?)(?=\n\[USER_QUESTIONS\]|$)'
    match = re.search(pattern, raw_output, re.IGNORECASE | re.DOTALL)
    
    if match:
        return match.group(1).strip()
    
    return ""


def parse_questions(raw_output: str) -> List[Dict]:
    """
    Extract and structure questions from [USER_QUESTIONS] section.
    
    Args:
        raw_output: Raw output from OpenAI API
        
    Returns:
        List of question dictionaries
    """
    questions = []
    
    # Find [USER_QUESTIONS] section
    pattern = r'\[USER_QUESTIONS\]\s*\n(.*?)$'
    match = re.search(pattern, raw_output, re.IGNORECASE | re.DOTALL)
    
    if not match:
        return questions
    
    content = match.group(1).strip()
    
    # Split by "Variable:" markers
    question_blocks = re.split(r'Variable:\s*', content, flags=re.IGNORECASE)
    
    for block in question_blocks:
        if not block.strip():
            continue
        
        question = {}
        
        # Extract variable name (from {{variableName}})
        var_match = re.search(r'\{\{(\w+)\}\}', block)
        if var_match:
            question['id'] = var_match.group(1)
        else:
            # Try to extract from first line
            first_line = block.split('\n')[0].strip()
            question['id'] = first_line.replace('{{', '').replace('}}', '').strip()
        
        # Extract question text
        q_match = re.search(r'Question:\s*["\']?([^"\']+)["\']?', block, re.IGNORECASE)
        if q_match:
            question['question'] = q_match.group(1).strip()
        
        # Extract type
        type_match = re.search(r'Type:\s*(\w+)', block, re.IGNORECASE)
        if type_match:
            question['type'] = type_match.group(1).lower()
        else:
            question['type'] = 'text'  # Default
        
        # Extract placeholder/options
        placeholder_match = re.search(r'Placeholder(?:/Options)?:\s*["\']?([^"\']+)["\']?', block, re.IGNORECASE)
        if placeholder_match:
            placeholder_text = placeholder_match.group(1).strip()
            if question['type'] == 'select':
                # Parse options (could be pipe-separated or newline-separated)
                if '|' in placeholder_text:
                    question['options'] = [opt.strip() for opt in placeholder_text.split('|')]
                else:
                    question['options'] = [opt.strip() for opt in placeholder_text.split('\n') if opt.strip()]
            else:
                question['placeholder'] = placeholder_text
        
        # Extract "Why it matters"
        why_match = re.search(r'Why it matters:\s*["\']?([^"\']+)["\']?', block, re.IGNORECASE)
        if why_match:
            question['why_matters'] = why_match.group(1).strip()
        
        # Default required to True if not specified
        question['required'] = True
        
        # Only add if we have at least id and question
        if 'id' in question and 'question' in question:
            questions.append(question)
    
    return questions


def validate_template(template: Dict) -> Tuple[bool, List[str]]:
    """
    Validate that template is complete and correct.
    
    Args:
        template: Template dictionary to validate
        
    Returns:
        Tuple of (is_valid, error_messages)
    """
    errors = []
    
    # Check required top-level fields
    required_fields = ['category', 'prompt_template', 'questions']
    for field in required_fields:
        if field not in template:
            errors.append(f"Missing required field: {field}")
    
    # Validate questions
    if 'questions' in template:
        question_ids = set()
        for i, q in enumerate(template['questions']):
            # Check required question fields
            required_q_fields = ['id', 'question', 'type']
            for field in required_q_fields:
                if field not in q:
                    errors.append(f"Question {i+1} missing required field: {field}")
            
            # Check ID uniqueness
            if 'id' in q:
                if q['id'] in question_ids:
                    errors.append(f"Duplicate question ID: {q['id']}")
                question_ids.add(q['id'])
            
            # Check type validity
            if 'type' in q:
                if q['type'] not in ['text', 'textarea', 'select']:
                    errors.append(f"Invalid question type: {q['type']} (must be text, textarea, or select)")
            
            # Check select has options
            if q.get('type') == 'select' and 'options' not in q:
                errors.append(f"Select question '{q.get('id', 'unknown')}' missing 'options' array")
    
    # Validate that all {{variables}} in prompt_template match question IDs
    if 'prompt_template' in template and 'questions' in template:
        template_vars = re.findall(r'\{\{(\w+)\}\}', template['prompt_template'])
        question_ids = {q.get('id') for q in template['questions'] if 'id' in q}
        
        for var in template_vars:
            if var not in question_ids and var not in ['userIntent', 'category']:  # Allow special vars
                # Warning, not error (template might have variables filled elsewhere)
                pass
    
    return len(errors) == 0, errors


def parse_meta_prompt_output(raw_output: str, category: str) -> Dict:
    """
    Parse complete meta-prompt output into structured template.
    
    Args:
        raw_output: Raw output from OpenAI API
        category: Business category name
        
    Returns:
        Structured template dictionary
    """
    template = {
        'category': category,
        'version': '1.0.0',
        'meta_prompt_version': 'v1.0',
        'anti_patterns': parse_anti_patterns(raw_output),
        'prompt_template': parse_prompt_template(raw_output),
        'questions': parse_questions(raw_output)
    }
    
    # Generate opening dialog (light acknowledgment)
    # This will be enhanced in later phases, for now use a simple default
    template['opening_dialog'] = f"Hi! I'm here to help you with your {category.replace('_', ' ')} business. Let's get started."
    
    return template

