"""
Template Loader for Runtime

Loads pre-generated templates for use in the application.
Supports caching and versioning.
"""

import json
import os
from typing import Optional, Dict, List
from pathlib import Path


# In-memory cache for loaded templates
_TEMPLATE_CACHE: Dict[str, Dict] = {}


def load_template(category: str, version: str = "latest") -> Optional[Dict]:
    """
    Load pre-generated template for a category.
    
    Args:
        category: Business category name (e.g., "restaurant")
        version: Template version to load (default: "latest")
        
    Returns:
        Template dictionary or None if not found
    """
    # Check cache first
    cache_key = f"{category}:{version}"
    if cache_key in _TEMPLATE_CACHE:
        return _TEMPLATE_CACHE[cache_key]
    
    # Determine template path
    script_dir = os.path.dirname(os.path.abspath(__file__))
    templates_dir = os.path.join(script_dir, 'prompts', 'generated_templates')
    
    # For now, just load latest version (versioning can be added later)
    template_path = os.path.join(templates_dir, f"{category}.json")
    
    if not os.path.exists(template_path):
        return None
    
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            template = json.load(f)
        
        # Cache it
        _TEMPLATE_CACHE[cache_key] = template
        
        return template
    except Exception as e:
        print(f"Error loading template for {category}: {e}")
        return None


def get_available_categories() -> List[str]:
    """
    Get list of all available categories with templates.
    
    Returns:
        List of category names
    """
    # Get the directory where this file is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    templates_dir = os.path.join(script_dir, 'prompts', 'generated_templates')
    
    if not os.path.exists(templates_dir):
        print(f"Warning: Templates directory not found: {templates_dir}")
        return []
    
    categories = []
    try:
        for filename in os.listdir(templates_dir):
            if filename.endswith('.json'):
                category = filename.replace('.json', '')
                categories.append(category)
    except Exception as e:
        print(f"Error reading templates directory: {e}")
        return []
    
    return sorted(categories)


def clear_cache():
    """Clear the template cache (useful for testing or reloading)"""
    global _TEMPLATE_CACHE
    _TEMPLATE_CACHE = {}


def get_template_opening_dialog(category: str) -> str:
    """
    Get opening dialog for a category.
    
    Args:
        category: Business category name
        
    Returns:
        Opening dialog string or default message
    """
    template = load_template(category)
    if template and 'opening_dialog' in template:
        return template['opening_dialog']
    
    # Default fallback
    return f"Hi! I'm here to help you with your {category.replace('_', ' ')} business. Let's get started."


def get_template_questions(category: str) -> List[Dict]:
    """
    Get questions for a category (for sidebar form).
    
    Args:
        category: Business category name
        
    Returns:
        List of question dictionaries
    """
    template = load_template(category)
    if template and 'questions' in template:
        return template['questions']
    
    return []


def get_template_prompt_template(category: str) -> Optional[str]:
    """
    Get prompt template for a category (for chat context).
    
    Args:
        category: Business category name
        
    Returns:
        Prompt template string or None
    """
    template = load_template(category)
    if template and 'prompt_template' in template:
        return template['prompt_template']
    
    return None


def fill_template_with_answers(prompt_template: str, form_answers: Dict) -> str:
    """
    Fill template variables with form answers.
    
    Args:
        prompt_template: Template string with {{variables}}
        form_answers: Dictionary of question_id -> answer
        
    Returns:
        Filled template string
    """
    filled = prompt_template
    
    # Replace all {{variable}} with answers
    for question_id, answer in form_answers.items():
        placeholder = f"{{{{{question_id}}}}}"
        filled = filled.replace(placeholder, str(answer))
    
    return filled

