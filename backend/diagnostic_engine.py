"""
Diagnostic engine to match users to the most relevant marketing questions.
Uses a simple decision tree based on pain points, revenue, and experience.
"""

import json
import os
from pathlib import Path
from typing import List, Dict, Optional, Tuple

# Valid template categories for diagnostic
VALID_CATEGORIES = [
    "increase_sales",
    "build_brand_awareness",
    "drive_foot_traffic",
    "generate_more_leads",
    "launch_new_service_product",
    "retain_customers"
]

# Category mapping from CLARIFYING-QUESTIONS.md - note: generate_more_leads not generate_leads
DIAGNOSTIC_MAPPINGS = {
    "not_enough_customers": {
        "priority_categories": ["increase_sales", "generate_more_leads", "drive_foot_traffic"],
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
        "priority_categories": ["launch_new_service_product"],
        "keywords": ["launch", "new", "product", "service"]
    },
    "competing_with_big_brands": {
        "priority_categories": ["build_brand_awareness", "increase_sales"],
        "keywords": ["compete", "big", "brands", "competition"]
    },
    "sleeping_on_money": {
        "priority_categories": ["increase_sales", "build_brand_awareness"],
        "keywords": ["sales", "brand", "awareness"]
    }
}


def load_all_template_questions() -> List[Dict]:
    """
    Load all question templates from generated_templates/ subdirectories.
    Only loads questions from valid categories.
    
    Returns:
        List of question template dictionaries
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    templates_dir = os.path.join(script_dir, 'prompts', 'generated_templates')
    
    all_questions = []
    
    if not os.path.exists(templates_dir):
        return all_questions
    
    # Iterate through valid category directories
    for category in VALID_CATEGORIES:
        category_dir = os.path.join(templates_dir, category)
        
        if not os.path.isdir(category_dir):
            continue
        
        # Load all question_*.json files in this category
        for question_file in os.listdir(category_dir):
            if question_file.startswith('question_') and question_file.endswith('.json'):
                question_path = os.path.join(category_dir, question_file)
                
                try:
                    with open(question_path, 'r', encoding='utf-8') as f:
                        question_data = json.load(f)
                        # Ensure category is set correctly
                        question_data['category'] = category
                        all_questions.append(question_data)
                except Exception as e:
                    print(f"Error loading question template {question_path}: {e}")
                    continue
    
    return all_questions


def match_questions(
    pain_point: str,
    revenue_range: str,
    tried_before: List[str],
    all_questions: Optional[List[Dict]] = None
) -> List[Dict]:
    """
    Match user to top 3 most relevant questions.
    
    Args:
        pain_point: User's main pain point (e.g., "not_enough_customers")
        revenue_range: Monthly revenue range (e.g., "under_10k")
        tried_before: List of what they've already tried (e.g., ["social_media", "ads"])
        all_questions: Optional pre-loaded questions list (for performance)
    
    Returns:
        List of 3 dicts with question data + match_score + reasoning
    """
    if all_questions is None:
        all_questions = load_all_template_questions()
    
    # Get priority categories based on pain point
    mapping = DIAGNOSTIC_MAPPINGS.get(pain_point, {})
    priority_categories = mapping.get("priority_categories", [])
    
    scored_questions = []
    
    for question in all_questions:
        score = 0
        reasoning_parts = []
        
        question_category = question.get("category", "")
        question_text = question.get("question_text", "").lower()
        
        # Score based on category match (50 points)
        if question_category in priority_categories:
            score += 50
            reasoning_parts.append(f"Addresses your '{pain_point.replace('_', ' ')}' challenge")
        
        # Score based on revenue appropriateness (20 points)
        if revenue_range == "under_10k":
            # Prioritize low-budget strategies
            if "budget" in question_text or "free" in question_text or "low-cost" in question_text:
                score += 20
                reasoning_parts.append("Includes budget-conscious strategies")
        elif revenue_range == "1k_to_2k":
            # Very small budget - prioritize free/low-cost
            if "budget" in question_text or "free" in question_text or "low-cost" in question_text:
                score += 25
                reasoning_parts.append("Perfect for very small budgets ($1k-2k/month)")
        elif revenue_range == "2k_to_5k":
            # Small budget - can do some paid
            score += 15
            reasoning_parts.append("Balanced for small budgets ($2k-5k/month)")
        elif revenue_range == "10k_to_50k":
            # Can handle more complex strategies
            score += 10
            reasoning_parts.append("Suitable for growing businesses")
        
        # Penalize if they've already tried related strategies (-20 points)
        question_lower = question_text
        tried_lower = [t.lower() for t in tried_before]
        
        if "social_media" in tried_lower and ("social" in question_lower or "instagram" in question_lower or "facebook" in question_lower):
            score -= 20
            reasoning_parts.append("Offers alternatives to social media")
        if "ads" in tried_lower or "advertising" in tried_lower:
            if "ad" in question_lower or "paid" in question_lower or "advertising" in question_lower:
                score -= 20
                reasoning_parts.append("Focuses on non-ad strategies")
        if "email" in tried_lower and "email" in question_lower:
            score -= 10
            reasoning_parts.append("Offers alternatives to email marketing")
        if "seo" in tried_lower and "seo" in question_lower:
            score -= 10
            reasoning_parts.append("Offers alternatives to SEO")
        
        # Add question with score
        scored_questions.append({
            "question": question,
            "score": score,
            "reasoning": " • ".join(reasoning_parts) if reasoning_parts else "Good general fit for your situation"
        })
    
    # Sort by score and return top 3
    scored_questions.sort(key=lambda x: x["score"], reverse=True)
    return scored_questions[:3]


def explain_why_match(pain_point: str, revenue_range: str, tried_before: List[str]) -> List[str]:
    """
    Generate explanation for why these questions were matched.
    
    Args:
        pain_point: User's main pain point
        revenue_range: Monthly revenue range
        tried_before: List of what they've already tried
    
    Returns:
        List of explanation strings
    """
    explanations = []
    
    # Pain point explanations
    if pain_point == "not_enough_customers":
        explanations.append("You need strategies to bring in more customers")
    elif pain_point == "no_visibility":
        explanations.append("Your business needs better visibility in your market")
    elif pain_point == "cant_keep_customers":
        explanations.append("You need to improve customer retention and loyalty")
    elif pain_point == "launching_something":
        explanations.append("You're launching something new and need a go-to-market strategy")
    
    # Revenue range explanations
    if revenue_range == "under_10k":
        explanations.append("These questions focus on cost-effective strategies for smaller budgets")
    elif revenue_range == "1k_to_2k":
        explanations.append("These questions prioritize free and low-cost strategies perfect for very small budgets")
    elif revenue_range == "2k_to_5k":
        explanations.append("These questions balance free and paid strategies suitable for small marketing budgets")
    elif revenue_range == "10k_to_50k":
        explanations.append("These questions balance organic and paid strategies for growing businesses")
    
    # Tried before explanations
    if tried_before:
        tried_str = ", ".join([t.replace("_", " ").title() for t in tried_before])
        explanations.append(f"These offer alternatives to what you've already tried ({tried_str})")
    
    return explanations

