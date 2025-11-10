#!/usr/bin/env python3
"""
Question-Based Template Generator

Generates templates for each question in QUESTIONS.md using the meta-prompt system.
Each question gets its own template, organized by category folders.

Usage:
    python scripts/generate_question_templates.py [--mock] [--category CATEGORY] [--question-id QUESTION_ID]
"""

import os
import sys
import json
import logging
import time
import re
from datetime import datetime
from typing import Dict, List, Optional, Tuple
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
        logging.FileHandler('question_template_generation.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


# Category mapping from QUESTIONS.md headers to folder names
CATEGORY_MAPPING = {
    "📈 Increase Sales": "increase_sales",
    "💡 Build Brand Awareness": "build_brand_awareness",
    "🚶 Drive Foot Traffic": "drive_foot_traffic",
    "🎯 Generate More Leads": "generate_more_leads",
    "🚀 Launch New Product/Service": "launch_new_service_product",
    "🔄 Retain Customers": "retain_customers"
}


def load_meta_prompt_template() -> str:
    """Load meta-prompt-system.md template - extract just the prompt section"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    meta_prompt_path = os.path.join(script_dir, '..', 'prompts', 'meta-prompt-system.md')
    
    if not os.path.exists(meta_prompt_path):
        raise FileNotFoundError(f"Meta-prompt file not found: {meta_prompt_path}")
    
    with open(meta_prompt_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract the prompt from the code block (starts with "You are a prompt architect")
    # Look for the code block that contains the actual prompt
    prompt_start = content.find("You are a prompt architect")
    if prompt_start == -1:
        # Fallback: try to find the code block
        code_block_match = re.search(r'```\s*\nYou are a prompt architect.*?```', content, re.DOTALL)
        if code_block_match:
            prompt_text = code_block_match.group(0)
            # Remove the code block markers
            prompt_text = re.sub(r'^```\s*\n', '', prompt_text)
            prompt_text = re.sub(r'\n```\s*$', '', prompt_text)
            return prompt_text
        # If still not found, return the whole file (legacy behavior)
        return content
    
    # Extract from "You are a prompt architect" to the end of the code block
    # Find the closing ``` after the prompt
    remaining = content[prompt_start:]
    code_block_end = remaining.find('```', remaining.find('```') + 3)  # Find second ```
    if code_block_end != -1:
        prompt_text = remaining[:code_block_end + 3]
        # Remove code block markers
        prompt_text = re.sub(r'^```\s*\n?', '', prompt_text)
        prompt_text = re.sub(r'\n?```\s*$', '', prompt_text)
        return prompt_text.strip()
    
    # Fallback: return from prompt_start to end of file
    return content[prompt_start:].strip()


def parse_questions_md(questions_file: str) -> Dict[str, List[Tuple[int, str]]]:
    """
    Parse QUESTIONS.md and extract questions by category.
    
    Returns:
        Dictionary mapping category folder name to list of (question_number, question_text) tuples
    """
    questions_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), questions_file)
    
    if not os.path.exists(questions_path):
        raise FileNotFoundError(f"QUESTIONS.md not found: {questions_path}")
    
    with open(questions_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    questions_by_category = {}
    current_category = None
    question_number = 0
    
    lines = content.split('\n')
    
    for line in lines:
        # Check if this is a category header
        for category_header, folder_name in CATEGORY_MAPPING.items():
            if category_header in line:
                current_category = folder_name
                question_number = 0
                if folder_name not in questions_by_category:
                    questions_by_category[folder_name] = []
                break
        
        # Check if this is a question (numbered list item)
        if current_category:
            # Match patterns like "1. How do I..." or "1. What pricing..."
            match = re.match(r'^\d+\.\s+(.+)$', line.strip())
            if match:
                question_number += 1
                question_text = match.group(1).strip()
                # Remove trailing question mark if present (we'll add context)
                if question_text.endswith('?'):
                    question_text = question_text[:-1]
                questions_by_category[current_category].append((question_number, question_text))
    
    logger.info(f"Parsed {sum(len(q) for q in questions_by_category.values())} questions across {len(questions_by_category)} categories")
    return questions_by_category


def fill_meta_prompt_template(template: str, user_domain: str, user_framing: str = "") -> str:
    """Replace {{userDomain}} and {{userFraming}} in template"""
    filled = template.replace('{{userDomain}}', user_domain)
    if user_framing:
        filled = filled.replace('{{userFraming}}', f"\n\n{user_framing}")
    else:
        filled = filled.replace('{{userFraming}}', '')
    return filled


def generate_mock_template(category: str, question_number: int, question_text: str) -> Dict:
    """Generate mock template for testing without API calls"""
    return {
        "category": category,
        "question_number": question_number,
        "question_text": question_text,
        "version": "1.0.0",
        "meta_prompt_version": "v1.0",
        "generated_at": datetime.now().isoformat(),
        "generated_by": "generate_question_templates.py (mock mode)",
        "opening_dialog": f"Hi! I'm here to help you with: {question_text}",
        "anti_patterns": [
            f"Mock anti-pattern 1 for {category} question {question_number}",
            f"Mock anti-pattern 2 for {category} question {question_number}"
        ],
        "prompt_template": f"Role: Marketing strategist for {category}\n\nIntent: Help user with {question_text}\n\nVariables:\n- {{business_name}}: Business name\n- {{target_audience}}: Target audience",
        "questions": [
            {
                "id": "business_name",
                "question": f"What's your business name?",
                "type": "text",
                "placeholder": "e.g., Example Business",
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
    }


def generate_template_for_question(
    category: str,
    question_number: int,
    question_text: str,
    openai_client: OpenAI,
    meta_prompt_template: str,
    mock: bool = False,
    max_retries: int = 3
) -> Optional[Dict]:
    """
    Generate template for a single question with retry logic.
    
    Args:
        category: Category folder name
        question_number: Question number within category
        question_text: The question text
        openai_client: OpenAI client instance
        meta_prompt_template: Meta-prompt template string
        mock: If True, return mock template without API call
        max_retries: Maximum number of retry attempts
        
    Returns:
        Template dictionary or None if failed
    """
    if mock:
        logger.info(f"Generating MOCK template for {category} question {question_number}")
        return generate_mock_template(category, question_number, question_text)
    
    # Format the question as user domain
    # Add context to make it clear this is a marketing question
    user_domain = f"I need help with: {question_text}"
    user_framing = "This is a small business marketing question. Focus on practical, actionable strategies that work for small businesses with limited budgets. Avoid generic advice and provide specific tactics."
    
    # Fill template with question-specific content
    filled_prompt = fill_meta_prompt_template(
        meta_prompt_template,
        user_domain,
        user_framing
    )
    
    # Generate with retry logic
    for attempt in range(max_retries):
        try:
            logger.info(f"Generating template for {category} question {question_number} (attempt {attempt + 1}/{max_retries})")
            
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
            
            # Log raw output for debugging if parsing fails
            debug_log_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'prompts', 'generated_templates', 'debug')
            os.makedirs(debug_log_path, exist_ok=True)
            
            # Parse the output
            template = parse_meta_prompt_output(raw_output, f"{category}_question_{question_number}")
            template['category'] = category
            template['question_number'] = question_number
            template['question_text'] = question_text
            template['generated_at'] = datetime.now().isoformat()
            template['generated_by'] = 'generate_question_templates.py'
            
            # Check if parsing actually extracted content
            if not template.get('prompt_template') or not template.get('questions'):
                logger.warning(f"Parsing extracted empty content for {category} question {question_number}")
                logger.warning(f"Anti-patterns found: {len(template.get('anti_patterns', []))}")
                logger.warning(f"Prompt template length: {len(template.get('prompt_template', ''))}")
                logger.warning(f"Questions found: {len(template.get('questions', []))}")
                
                # Save raw output for debugging
                debug_file = os.path.join(debug_log_path, f"{category}_question_{question_number}_raw.txt")
                with open(debug_file, 'w', encoding='utf-8') as f:
                    f.write("=== RAW OPENAI OUTPUT ===\n\n")
                    f.write(raw_output)
                    f.write("\n\n=== PARSED TEMPLATE ===\n\n")
                    f.write(json.dumps(template, indent=2))
                logger.info(f"Saved raw output to {debug_file} for debugging")
            
            # Validate
            is_valid, errors = validate_template(template)
            if not is_valid:
                logger.error(f"Template validation failed for {category} question {question_number}: {errors}")
                # Save raw output even on validation failure
                debug_file = os.path.join(debug_log_path, f"{category}_question_{question_number}_validation_error.txt")
                with open(debug_file, 'w', encoding='utf-8') as f:
                    f.write("=== VALIDATION ERRORS ===\n\n")
                    f.write("\n".join(errors))
                    f.write("\n\n=== RAW OPENAI OUTPUT ===\n\n")
                    f.write(raw_output)
                    f.write("\n\n=== PARSED TEMPLATE ===\n\n")
                    f.write(json.dumps(template, indent=2))
                return None
            
            # Additional check: Don't save if essential content is missing
            if not template.get('prompt_template') or not template.get('questions'):
                logger.error(f"Template for {category} question {question_number} is missing essential content - not saving")
                return None
            
            # Add SMB insights
            smb_insights = load_smb_insights()
            template = enhance_template_with_data(template, smb_insights)
            
            logger.info(f"Successfully generated template for {category} question {question_number}")
            return template
            
        except RateLimitError as e:
            wait_time = 2 ** attempt  # Exponential backoff
            logger.warning(f"Rate limit hit for {category} question {question_number}, waiting {wait_time}s")
            if attempt < max_retries - 1:
                time.sleep(wait_time)
            else:
                logger.error(f"Rate limit exceeded for {category} question {question_number} after {max_retries} attempts")
                raise
                
        except APIError as e:
            logger.error(f"API error for {category} question {question_number}: {e}")
            if attempt == max_retries - 1:
                raise
            time.sleep(1)
            
        except Exception as e:
            logger.error(f"Unexpected error for {category} question {question_number}: {e}", exc_info=True)
            raise
    
    return None


def save_template(category: str, question_number: int, template: Dict, output_base_dir: str):
    """Save template to JSON file in category folder"""
    category_dir = os.path.join(output_base_dir, category)
    os.makedirs(category_dir, exist_ok=True)
    
    output_path = os.path.join(category_dir, f"question_{question_number}.json")
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(template, f, indent=2, ensure_ascii=False)
    
    logger.info(f"Saved template to {output_path}")


def template_exists(category: str, question_number: int, output_base_dir: str) -> bool:
    """Check if template file already exists"""
    category_dir = os.path.join(output_base_dir, category)
    output_path = os.path.join(category_dir, f"question_{question_number}.json")
    return os.path.exists(output_path)


def generate_all_question_templates(
    questions_by_category: Dict[str, List[Tuple[int, str]]],
    openai_client: Optional[OpenAI],
    meta_prompt_template: str,
    output_base_dir: str,
    mock: bool = False,
    category_filter: Optional[str] = None,
    question_filter: Optional[int] = None,
    continue_on_error: bool = True
) -> Dict[str, Dict[int, bool]]:
    """
    Generate templates for all questions.
    
    Returns:
        Dictionary mapping category to dict of question_number -> success status
    """
    results = {}
    start_time = datetime.now()
    
    total_questions = sum(len(questions) for questions in questions_by_category.values())
    logger.info(f"Starting template generation for {total_questions} questions (mock={mock})")
    
    for category, questions in questions_by_category.items():
        # Filter by category if specified
        if category_filter and category != category_filter:
            continue
        
        results[category] = {}
        
        for question_number, question_text in questions:
            # Filter by question number if specified
            if question_filter and question_number != question_filter:
                continue
            
            # Skip if template already exists (unless regenerating specific question)
            if not question_filter and template_exists(category, question_number, output_base_dir):
                logger.info(f"Skipping {category} question {question_number} - file already exists")
                results[category][question_number] = True
                continue
            
            try:
                template = generate_template_for_question(
                    category,
                    question_number,
                    question_text,
                    openai_client,
                    meta_prompt_template,
                    mock=mock
                )
                
                if template:
                    save_template(category, question_number, template, output_base_dir)
                    results[category][question_number] = True
                else:
                    logger.error(f"Failed to generate template for {category} question {question_number}")
                    results[category][question_number] = False
                    
            except Exception as e:
                logger.error(f"Failed to generate template for {category} question {question_number}: {e}", exc_info=True)
                results[category][question_number] = False
                if not continue_on_error:
                    raise
    
    duration = (datetime.now() - start_time).total_seconds()
    total_success = sum(sum(1 for v in cat_results.values() if v) for cat_results in results.values())
    total_attempted = sum(len(cat_results) for cat_results in results.values())
    logger.info(f"Template generation complete. Duration: {duration}s. Success: {total_success}/{total_attempted}")
    
    return results


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate templates for each question in QUESTIONS.md')
    parser.add_argument('--mock', action='store_true', help='Generate mock templates without API calls')
    parser.add_argument('--category', type=str, help='Generate templates for single category only')
    parser.add_argument('--question-id', type=int, help='Generate template for single question number only')
    parser.add_argument('--continue-on-error', action='store_true', default=True, help='Continue on error')
    parser.add_argument('--questions-file', type=str, default='QUESTIONS.md', help='Path to QUESTIONS.md file')
    
    args = parser.parse_args()
    
    # Load questions
    try:
        questions_by_category = parse_questions_md(args.questions_file)
        meta_prompt_template = load_meta_prompt_template()
    except FileNotFoundError as e:
        logger.error(f"Configuration error: {e}")
        sys.exit(1)
    
    # Filter to single category if specified
    if args.category:
        if args.category not in questions_by_category:
            logger.error(f"Category '{args.category}' not found. Available: {list(questions_by_category.keys())}")
            sys.exit(1)
        questions_by_category = {args.category: questions_by_category[args.category]}
    
    # Setup output directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_base_dir = os.path.join(script_dir, '..', 'prompts', 'generated_templates')
    os.makedirs(output_base_dir, exist_ok=True)
    
    # Initialize OpenAI client (if not mock)
    openai_client = None
    if not args.mock:
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            logger.error("OPENAI_API_KEY not found in environment variables")
            sys.exit(1)
        openai_client = OpenAI(api_key=api_key)
    
    # Generate templates
    results = generate_all_question_templates(
        questions_by_category,
        openai_client,
        meta_prompt_template,
        output_base_dir,
        mock=args.mock,
        category_filter=args.category,
        question_filter=args.question_id,
        continue_on_error=args.continue_on_error
    )
    
    # Print summary
    print("\n" + "="*50)
    print("Question Template Generation Summary")
    print("="*50)
    for category, cat_results in results.items():
        print(f"\n{category}:")
        for question_num, success in sorted(cat_results.items()):
            status = "✅" if success else "❌"
            print(f"  {status} Question {question_num}")
    print("="*50)
    
    # Exit with error if any failed
    all_success = all(all(cat_results.values()) for cat_results in results.values())
    if not all_success:
        sys.exit(1)


if __name__ == '__main__':
    main()

