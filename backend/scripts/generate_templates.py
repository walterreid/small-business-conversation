#!/usr/bin/env python3
"""
Template Generator Script

One-time script that uses meta-prompt-system.md to generate high-quality
question templates for each business category. Saves 99.5% on costs vs
generating on-demand.

Usage:
    python scripts/generate_templates.py [--mock] [--category CATEGORY]
"""

import os
import sys
import json
import logging
import time
from datetime import datetime
from typing import Dict, Optional
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
from openai import OpenAI, RateLimitError, APIError

from scripts.template_parser import parse_meta_prompt_output, validate_template
from scripts.smb_data_loader import load_smb_insights, enhance_template_with_data

# Load environment variables
load_dotenv()

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


def load_meta_prompt_template() -> str:
    """Load meta-prompt-system.md template"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    meta_prompt_path = os.path.join(script_dir, '..', 'prompts', 'meta-prompt-system.md')
    
    if not os.path.exists(meta_prompt_path):
        raise FileNotFoundError(f"Meta-prompt file not found: {meta_prompt_path}")
    
    with open(meta_prompt_path, 'r', encoding='utf-8') as f:
        return f.read()


def load_category_configs(config_file: str = 'template_categories.json') -> Dict:
    """
    Load category configurations from JSON file.
    
    Args:
        config_file: Name of config file (default: 'template_categories.json')
                    Can also use 'marketing_goal_categories.json'
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, '..', 'config', config_file)
    
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Category config file not found: {config_path}")
    
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def fill_meta_prompt_template(template: str, user_domain: str, user_framing: str = "") -> str:
    """Replace {{userDomain}} and {{userFraming}} in template"""
    filled = template.replace('{{userDomain}}', user_domain)
    if user_framing:
        filled = filled.replace('{{userFraming}}', f"\n\n{user_framing}")
    else:
        filled = filled.replace('{{userFraming}}', '')
    return filled


def generate_mock_template(category: str, config: Dict) -> Dict:
    """Generate mock template for testing without API calls"""
    # Use starter questions if available, otherwise generate defaults
    starter_questions = config.get('starter_questions', [])
    
    if starter_questions:
        questions = starter_questions
    else:
        # Default questions if no starters provided
        questions = [
            {
                "id": "business_name",
                "question": f"What's your {category.replace('_', ' ')} business name?",
                "type": "text",
                "placeholder": f"e.g., Example {category.replace('_', ' ').title()}",
                "required": True,
                "why_matters": "Personalizes recommendations"
            },
            {
                "id": "target_audience",
                "question": "Who are your ideal customers?",
                "type": "textarea",
                "placeholder": "Describe your target audience",
                "required": True,
                "why_matters": "Helps tailor marketing strategies"
            }
        ]
    
    # Build variable list from questions
    variables = "\n".join([f"- {{{q.get('id', 'unknown')}}}: {q.get('why_matters', 'User input')}" for q in questions])
    
    return {
        "category": category,
        "version": "1.0.0",
        "meta_prompt_version": "v1.0",
        "generated_at": datetime.now().isoformat(),
        "generated_by": "generate_templates.py (mock mode)",
        "opening_dialog": f"Hi! I'm here to help you {config.get('name', category.replace('_', ' '))}. Let's get started.",
        "anti_patterns": [
            f"Mock anti-pattern 1 for {category}",
            f"Mock anti-pattern 2 for {category}"
        ],
        "prompt_template": f"Role: Marketing strategist specializing in {config.get('name', category.replace('_', ' '))}\n\nIntent: Help user with {config.get('user_domain', 'marketing')}\n\nVariables:\n{variables}",
        "questions": questions
    }


def generate_template_for_category(
    category: str,
    config: Dict,
    openai_client: OpenAI,
    meta_prompt_template: str,
    mock: bool = False,
    max_retries: int = 3
) -> Optional[Dict]:
    """
    Generate template for a single category with retry logic.
    
    Args:
        category: Category name
        config: Category configuration (user_domain, user_framing)
        openai_client: OpenAI client instance
        meta_prompt_template: Meta-prompt template string
        mock: If True, return mock template without API call
        max_retries: Maximum number of retry attempts
        
    Returns:
        Template dictionary or None if failed
    """
    if mock:
        logger.info(f"Generating MOCK template for {category}")
        return generate_mock_template(category, config)
    
    # Fill template with category-specific content
    filled_prompt = fill_meta_prompt_template(
        meta_prompt_template,
        config['user_domain'],
        config.get('user_framing', '')
    )
    
    # Generate with retry logic
    for attempt in range(max_retries):
        try:
            logger.info(f"Generating template for {category} (attempt {attempt + 1}/{max_retries})")
            
            response = openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "user",
                        "content": filled_prompt
                    }
                ],
                temperature=0.7,
                max_tokens=4000
            )
            
            raw_output = response.choices[0].message.content
            
            # Parse the output
            template = parse_meta_prompt_output(raw_output, category)
            template['generated_at'] = datetime.now().isoformat()
            template['generated_by'] = 'generate_templates.py'
            
            # Validate
            is_valid, errors = validate_template(template)
            if not is_valid:
                logger.error(f"Template validation failed for {category}: {errors}")
                return None
            
            # Add SMB insights
            smb_insights = load_smb_insights()
            template = enhance_template_with_data(template, smb_insights)
            
            logger.info(f"Successfully generated template for {category}")
            return template
            
        except RateLimitError as e:
            wait_time = 2 ** attempt  # Exponential backoff
            logger.warning(f"Rate limit hit for {category}, waiting {wait_time}s")
            if attempt < max_retries - 1:
                time.sleep(wait_time)
            else:
                logger.error(f"Rate limit exceeded for {category} after {max_retries} attempts")
                raise
                
        except APIError as e:
            logger.error(f"API error for {category}: {e}")
            if attempt == max_retries - 1:
                raise
            time.sleep(1)
            
        except Exception as e:
            logger.error(f"Unexpected error for {category}: {e}", exc_info=True)
            raise
    
    return None


def save_template(category: str, template: Dict, output_dir: str):
    """Save template to JSON file"""
    output_path = os.path.join(output_dir, f"{category}.json")
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(template, f, indent=2, ensure_ascii=False)
    
    logger.info(f"Saved template to {output_path}")


def generate_all_templates(
    categories: Dict,
    openai_client: Optional[OpenAI],
    meta_prompt_template: str,
    output_dir: str,
    mock: bool = False,
    continue_on_error: bool = True
) -> Dict[str, bool]:
    """
    Generate templates for all categories.
    
    Returns:
        Dictionary mapping category to success status
    """
    results = {}
    start_time = datetime.now()
    
    logger.info(f"Starting template generation for {len(categories)} categories (mock={mock})")
    
    for category, config in categories.items():
        try:
            template = generate_template_for_category(
                category,
                config,
                openai_client,
                meta_prompt_template,
                mock=mock
            )
            
            if template:
                save_template(category, template, output_dir)
                results[category] = True
            else:
                logger.error(f"Failed to generate template for {category}")
                results[category] = False
                
        except Exception as e:
            logger.error(f"Failed to generate template for {category}: {e}", exc_info=True)
            results[category] = False
            if not continue_on_error:
                raise
    
    duration = (datetime.now() - start_time).total_seconds()
    success_count = sum(results.values())
    logger.info(f"Template generation complete. Duration: {duration}s. Success: {success_count}/{len(results)}")
    
    return results


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate templates from meta-prompt-system.md')
    parser.add_argument('--mock', action='store_true', help='Generate mock templates without API calls')
    parser.add_argument('--category', type=str, help='Generate template for single category only')
    parser.add_argument('--continue-on-error', action='store_true', default=True, help='Continue on error')
    parser.add_argument('--config', type=str, default='template_categories.json', 
                       help='Config file to use (default: template_categories.json, or marketing_goal_categories.json)')
    
    args = parser.parse_args()
    
    # Load configuration
    try:
        categories = load_category_configs(args.config)
        meta_prompt_template = load_meta_prompt_template()
    except FileNotFoundError as e:
        logger.error(f"Configuration error: {e}")
        sys.exit(1)
    
    # Filter to single category if specified
    if args.category:
        if args.category not in categories:
            logger.error(f"Category '{args.category}' not found in config")
            sys.exit(1)
        categories = {args.category: categories[args.category]}
    
    # Setup output directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, '..', 'prompts', 'generated_templates')
    os.makedirs(output_dir, exist_ok=True)
    
    # Initialize OpenAI client (if not mock)
    openai_client = None
    if not args.mock:
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            logger.error("OPENAI_API_KEY not found in environment variables")
            sys.exit(1)
        openai_client = OpenAI(api_key=api_key)
    
    # Generate templates
    results = generate_all_templates(
        categories,
        openai_client,
        meta_prompt_template,
        output_dir,
        mock=args.mock,
        continue_on_error=args.continue_on_error
    )
    
    # Print summary
    print("\n" + "="*50)
    print("Template Generation Summary")
    print("="*50)
    for category, success in results.items():
        status = "✅" if success else "❌"
        print(f"{status} {category}")
    print("="*50)
    
    # Exit with error if any failed
    if not all(results.values()):
        sys.exit(1)


if __name__ == '__main__':
    main()

