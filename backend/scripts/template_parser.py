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
    
    # Look for [ANTI-PATTERNS] section (multiple format attempts)
    # Important: Stop at PROMPT_TEMPLATE or Part 2/Part 3 sections
    patterns = [
        r'\[ANTI-PATTERNS?\]\s*\n(.*?)(?=\n\[PROMPT_TEMPLATE\]|$)',
        r'\[ANTI-PATTERNS?\]\s*\n(.*?)(?=\n(?:\[PROMPT_TEMPLATE\]|Part 2|#### Part 2|### Part 2))',
        r'\*\*ANTI-PATTERNS?:\*\*\s*\n(.*?)(?=\n\*\*PROMPT_TEMPLATE|$)',
        r'\*\*ANTI-PATTERNS?:\*\*\s*\n(.*?)(?=\n(?:####|###|Part 2))',
        r'ANTI-PATTERNS?:\s*\n(.*?)(?=\n(?:PROMPT_TEMPLATE|Part 2|####|###))',
        # Code block format
        r'\[ANTI-PATTERNS?\]\s*\n```(?:.*?)?\n(.*?)```',
    ]
    
    match = None
    for pattern in patterns:
        match = re.search(pattern, raw_output, re.IGNORECASE | re.DOTALL)
        if match:
            break
    
    if match:
        content = match.group(1).strip()
        # Remove code block markers if present
        content = re.sub(r'^```.*?\n', '', content, flags=re.MULTILINE)
        content = re.sub(r'\n```.*?$', '', content, flags=re.MULTILINE)
        
        # Extract lines starting with "- " or "* " or numbered
        # Stop if we hit a section marker or variable/question content
        lines = content.split('\n')
        for line in lines:
            line = line.strip()
            # Stop if we hit a section header or start of next section
            if re.match(r'^(Part \d+|####|###|\[PROMPT|\[USER|Variables?:|Variable:)', line, re.IGNORECASE):
                break
            # Stop if we see markdown formatting that indicates next section
            if re.match(r'^\*\*.*:\*\*', line) and 'Pattern' not in line:
                break
            # Handle various bullet formats
            if line.startswith('- ') or line.startswith('* '):
                # Remove bullet point
                pattern_text = line[2:].strip()
                # Only add if it's clearly a Common Pattern description
                if pattern_text and 'Common Pattern' in pattern_text:
                    # Extract just the pattern description (after "Common Pattern X:")
                    if ':' in pattern_text:
                        pattern_text = pattern_text.split(':', 1)[1].strip()
                    if pattern_text and not re.match(r'^\{\{', pattern_text):
                        anti_patterns.append(pattern_text)
            elif re.match(r'^\d+\.\s+', line):
                # Handle numbered lists
                pattern_text = re.sub(r'^\d+\.\s+', '', line).strip()
                # Only add if it's clearly a Common Pattern
                if pattern_text and 'Common Pattern' in pattern_text:
                    if ':' in pattern_text:
                        pattern_text = pattern_text.split(':', 1)[1].strip()
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
    # Look for [PROMPT_TEMPLATE] section (multiple format attempts)
    # Important: Stop at USER_QUESTIONS or Part 3 sections
    patterns = [
        # Standard bracket format - stop at USER_QUESTIONS
        r'\[PROMPT_TEMPLATE\]\s*\n(.*?)(?=\n\[USER_QUESTIONS\]|$)',
        r'\[PROMPT_TEMPLATE\]\s*\n(.*?)(?=\n(?:\[USER_QUESTIONS\]|Part 3|#### Part 3|### Part 3))',
        # Markdown bold format
        r'\*\*PROMPT_TEMPLATE:\*\*\s*\n(.*?)(?=\n\*\*USER_QUESTIONS|$)',
        # Plain text format
        r'PROMPT_TEMPLATE:\s*\n(.*?)(?=\n(?:\[USER_QUESTIONS\]|USER_QUESTIONS|Part 3))',
        # Code block format (```) - stop before USER_QUESTIONS
        r'\*\*PROMPT_TEMPLATE:\*\*\s*\n```(?:.*?)?\n(.*?)```(?=\n(?:\[USER_QUESTIONS\]|Part 3))',
        r'PROMPT_TEMPLATE:\s*\n```(?:.*?)?\n(.*?)```(?=\n(?:\[USER_QUESTIONS\]|Part 3))',
        # Markdown header format
        r'(?:###|####)\s*\*\*PROMPT_TEMPLATE:\*\*\s*\n(.*?)(?=\n(?:###|####|\[USER_QUESTIONS\]|Part 3))',
        r'(?:###|####)\s*PROMPT_TEMPLATE:\s*\n(.*?)(?=\n(?:###|####|\[USER_QUESTIONS\]|Part 3))',
        # "Part 2: Design the Template" format
        r'Part 2.*?PROMPT_TEMPLATE:\s*\n```(?:.*?)?\n(.*?)```(?=\n(?:Part 3|\[USER_QUESTIONS\]))',
        r'Part 2.*?PROMPT_TEMPLATE:\s*\n(.*?)(?=\n(?:Part 3|\[USER_QUESTIONS\]|```))',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, raw_output, re.IGNORECASE | re.DOTALL)
        if match:
            content = match.group(1).strip()
            # Remove code block markers if present
            content = re.sub(r'^```.*?\n', '', content, flags=re.MULTILINE)
            content = re.sub(r'\n```.*?$', '', content, flags=re.MULTILINE)
            
            # Stop at USER_QUESTIONS section - be very strict
            content = re.split(r'\n(?:###|####)?\s*\[?USER_QUESTIONS', content, flags=re.IGNORECASE)[0]
            content = re.split(r'\n(?:###|####)?\s*For each variable', content, flags=re.IGNORECASE)[0]
            content = re.split(r'\n(?:###|####)?\s*Part 3', content, flags=re.IGNORECASE)[0]
            content = re.split(r'\n---\s*\n(?:###|####)?\s*\[?USER_QUESTIONS', content, flags=re.IGNORECASE)[0]
            
            # Remove any trailing markdown sections
            content = re.sub(r'\n(?:###|####)?\s*\[?USER_QUESTIONS.*$', '', content, flags=re.IGNORECASE | re.DOTALL)
            content = re.sub(r'\n(?:###|####)?\s*For each variable.*$', '', content, flags=re.IGNORECASE | re.DOTALL)
            content = re.sub(r'\n(?:###|####)?\s*Stage 2.*$', '', content, flags=re.IGNORECASE | re.DOTALL)
            
            if content and len(content) > 50:  # Only return if we got substantial content
                return content.strip()
    
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
    
    # Find [USER_QUESTIONS] section (multiple format attempts)
    # Important: Stop at ANTI-PATTERNS, Part 4, or Stage 2 sections
    patterns = [
        # Standard bracket format
        r'\[USER_QUESTIONS\]\s*\n(.*?)(?=\n(?:\[ANTI-PATTERNS\]|Part 4|Stage 2|---|$))',
        # Markdown bold format
        r'\*\*USER_QUESTIONS:\*\*\s*\n(.*?)(?=\n(?:\[ANTI-PATTERNS\]|Part 4|Stage 2|---|$))',
        # Plain text format
        r'USER_QUESTIONS:\s*\n(.*?)(?=\n(?:\[ANTI-PATTERNS\]|Part 4|Stage 2|---|$))',
        # Code block format (```)
        r'\*\*USER_QUESTIONS:\*\*\s*\n```(?:.*?)?\n(.*?)```(?=\n(?:\[ANTI-PATTERNS\]|Part 4|Stage 2))',
        r'USER_QUESTIONS:\s*\n```(?:.*?)?\n(.*?)```(?=\n(?:\[ANTI-PATTERNS\]|Part 4|Stage 2))',
        # Markdown header format
        r'(?:###|####)\s*\*\*USER_QUESTIONS:\*\*\s*\n(.*?)(?=\n(?:###|####|\[ANTI-PATTERNS\]|Part 4|Stage 2|---))',
        r'(?:###|####)\s*USER_QUESTIONS:\s*\n(.*?)(?=\n(?:###|####|\[ANTI-PATTERNS\]|Part 4|Stage 2|---))',
        # "For each variable" format (common in OpenAI responses) - with code block
        r'For each.*?variable.*?:\s*\n```(?:.*?)?\n(.*?)```(?=\n(?:####|\[ANTI-PATTERNS\]|Part 4|Stage 2|This structured))',
        r'For each.*?variable.*?:\s*\n(.*?)(?=\n(?:####|\[ANTI-PATTERNS\]|Part 4|Stage 2|---|This structured|$))',
        # "Part 3: Generate Questions" format - with code block
        r'PART 3.*?GENERATE QUESTIONS.*?\n(?:.*?For each.*?variable.*?:\s*\n)?```(?:.*?)?\n(.*?)```(?=\n(?:Part 4|\[ANTI-PATTERNS\]|Stage 2|This structured))',
        r'PART 3.*?GENERATE QUESTIONS.*?\n(?:.*?For each.*?variable.*?:\s*\n)?(.*?)(?=\n(?:Part 4|\[ANTI-PATTERNS\]|Stage 2|This structured|---|$))',
        # "### PART 3" format
        r'###\s*PART 3.*?GENERATE QUESTIONS.*?\n(?:.*?For each.*?variable.*?:\s*\n)?```(?:.*?)?\n(.*?)```(?=\n(?:###|Part 4|\[ANTI-PATTERNS\]|Stage 2|This structured))',
        r'###\s*PART 3.*?GENERATE QUESTIONS.*?\n(?:.*?For each.*?variable.*?:\s*\n)?(.*?)(?=\n(?:###|Part 4|\[ANTI-PATTERNS\]|Stage 2|This structured|---|$))',
        # More flexible: find code block after "For each" that contains Variable: patterns
        r'For each.*?variable.*?:\s*\n```\s*\n(.*?)```',
        # Even more flexible: find any code block containing "Variable: {{"
        r'```\s*\n(.*?Variable:\s*\{\{.*?)\n```',
        # Most flexible: find code block that starts with Variable: (handles any format)
        r'```\s*\n(Variable:\s*\{\{.*?)```',
        # Direct match: PART 3 followed by code block with Variable:
        r'PART 3.*?GENERATE QUESTIONS.*?\n```\s*\n(Variable:.*?)```',
    ]
    
    match = None
    for i, pattern in enumerate(patterns):
        match = re.search(pattern, raw_output, re.IGNORECASE | re.DOTALL)
        if match:
            break
    
    # If no match found, try a very simple catch-all: any code block containing "Variable:"
    if not match:
        # Find all code blocks - handle both ``` and ```language formats
        code_blocks = re.findall(r'```(?:[^\n]*)?\n(.*?)```', raw_output, re.DOTALL)
        for block in code_blocks:
            if 'Variable:' in block and ('{{' in block or 'Question:' in block):
                # Create a mock match object
                class MockMatch:
                    def group(self, n):
                        return block if n == 1 else None
                match = MockMatch()
                break
    
    if not match:
        return questions
    
    content = match.group(1).strip()
    # Remove code block markers if present
    content = re.sub(r'^```.*?\n', '', content, flags=re.MULTILINE)
    content = re.sub(r'\n```.*?$', '', content, flags=re.MULTILINE)
    
    # Stop at Part 4, ANTI-PATTERNS, or Stage 2 - be very strict
    content = re.split(r'\n(?:Part 4|\[ANTI-PATTERNS\]|Stage 2|### Stage 2|#### Part 4)', content, flags=re.IGNORECASE)[0]
    content = re.split(r'\n---\s*\n(?:Part 4|\[ANTI-PATTERNS\]|Stage 2)', content, flags=re.IGNORECASE)[0]
    
    # Remove any trailing sections that leaked in
    content = re.sub(r'\n(?:Part 4|\[ANTI-PATTERNS\]|Stage 2|### Stage 2|#### Part 4).*$', '', content, flags=re.IGNORECASE | re.DOTALL)
    
    # Split by "Variable:" markers - simpler approach
    question_blocks = re.split(r'Variable:\s*', content, flags=re.IGNORECASE)
    
    for i, block in enumerate(question_blocks):
        if not block.strip():
            continue
        
        # Skip the first block if it doesn't contain a Variable: (it's just preamble)
        if i == 0:
            # Check if this block actually contains variable/question content
            if '{{' not in block and 'Question:' not in block:
                continue
        
        question = {}
        
        # Extract variable name (from {{variableName}}) - should be at start of block
        var_match = re.search(r'\{\{(\w+)\}\}', block)
        if var_match:
            question['id'] = var_match.group(1)
        else:
            # Try to extract from first line - might be just the variable name
            first_line = block.split('\n')[0].strip()
            var_name = first_line.replace('{{', '').replace('}}', '').strip()
            if var_name and re.match(r'^\w+$', var_name):
                question['id'] = var_name
            else:
                # Skip if we can't extract a valid variable name
                continue
        
        # Extract question text - handle multiple formats
        q_match = re.search(r'Question:\s*["\']?([^"\'\n]+)["\']?', block, re.IGNORECASE)
        if not q_match:
            # Try markdown format: **Question**: "..."
            q_match = re.search(r'\*\*Question\*\*:\s*["\']?([^"\'\n]+)["\']?', block, re.IGNORECASE)
        if not q_match:
            # Try with dash: - **Question**: "..."
            q_match = re.search(r'-\s*\*\*Question\*\*:\s*["\']?([^"\'\n]+)["\']?', block, re.IGNORECASE)
        if q_match:
            question['question'] = q_match.group(1).strip()
        else:
            # Skip if no question found
            continue
        
        # Extract type
        type_match = re.search(r'Type:\s*(\w+)', block, re.IGNORECASE)
        if not type_match:
            # Try markdown format
            type_match = re.search(r'\*\*Type\*\*:\s*(\w+)', block, re.IGNORECASE)
        if type_match:
            question['type'] = type_match.group(1).lower()
        else:
            question['type'] = 'text'  # Default
        
        # Extract placeholder/options
        placeholder_match = re.search(r'Placeholder(?:/Options)?:\s*["\']?([^"\'\n]+)["\']?', block, re.IGNORECASE)
        if not placeholder_match:
            # Try markdown format
            placeholder_match = re.search(r'\*\*Placeholder\*\*:\s*["\']?([^"\'\n]+)["\']?', block, re.IGNORECASE)
        if placeholder_match:
            placeholder_text = placeholder_match.group(1).strip()
            if question['type'] == 'select':
                # Parse options (could be pipe-separated, comma-separated, or newline-separated)
                if '|' in placeholder_text:
                    options = [opt.strip() for opt in placeholder_text.split('|')]
                elif ',' in placeholder_text:
                    options = [opt.strip() for opt in placeholder_text.split(',')]
                else:
                    options = [opt.strip() for opt in placeholder_text.split('\n') if opt.strip()]
                
                # Clean up options - remove "Options:" prefix if present
                cleaned_options = []
                for opt in options:
                    # Remove "Options:" prefix if it exists
                    opt = opt.replace('Options:', '').strip()
                    # Remove "etc." or "etc" at the end
                    opt = re.sub(r'\s*,\s*etc\.?$', '', opt, flags=re.IGNORECASE).strip()
                    if opt and opt.lower() not in ['options', 'option']:
                        cleaned_options.append(opt)
                
                question['options'] = cleaned_options if cleaned_options else options
            else:
                question['placeholder'] = placeholder_text
        
        # Extract "Why it matters" - stop at next section
        why_match = re.search(r'Why it matters:\s*["\']?([^"\']+?)(?:\n(?:Variable:|Part |\[|Stage |---)|["\']?\s*$)', block, re.IGNORECASE | re.DOTALL)
        if not why_match:
            # Try markdown format
            why_match = re.search(r'\*\*Why it matters\*\*:\s*["\']?([^"\']+?)(?:\n(?:Variable:|Part |\[|Stage |---)|["\']?\s*$)', block, re.IGNORECASE | re.DOTALL)
        if why_match:
            why_text = why_match.group(1).strip()
            # Clean up any trailing content
            why_text = re.split(r'\n(?:Variable:|Part |\[|Stage |---)', why_text)[0].strip()
            question['why_matters'] = why_text
        
        # Default required to True if not specified
        question['required'] = True
        
        # Only add if we have at least id and question
        if 'id' in question and 'question' in question and question['question']:
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

