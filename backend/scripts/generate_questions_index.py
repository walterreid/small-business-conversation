#!/usr/bin/env python3
"""
Generate a JSON index file mapping marketing goal categories to their questions.

This creates a simple JSON structure that the frontend can use to display
questions when a user clicks on a marketing goal category.
"""

import os
import json
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def load_question_file(category: str, question_number: int, base_dir: str) -> dict:
    """Load a question JSON file"""
    file_path = os.path.join(base_dir, category, f"question_{question_number}.json")
    
    if not os.path.exists(file_path):
        return None
    
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def generate_questions_index(output_file: str = None):
    """Generate the questions index JSON file"""
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    templates_dir = os.path.join(script_dir, '..', 'prompts', 'generated_templates')
    
    if output_file is None:
        output_file = os.path.join(script_dir, '..', 'config', 'marketing_questions_index.json')
    
    # Category mapping (folder names to display names)
    category_display = {
        "increase_sales": {
            "display_name": "Increase Sales",
            "icon": "📈",
            "description": "Convert more prospects into paying customers"
        },
        "build_brand_awareness": {
            "display_name": "Build Brand Awareness",
            "icon": "💡",
            "description": "Get your brand noticed by the right people"
        },
        "drive_foot_traffic": {
            "display_name": "Drive Foot Traffic",
            "icon": "🚶",
            "description": "Bring more customers to your physical location"
        },
        "generate_more_leads": {
            "display_name": "Generate More Leads",
            "icon": "🎯",
            "description": "Find and attract potential customers"
        },
        "launch_new_service_product": {
            "display_name": "Launch New Product/Service",
            "icon": "🚀",
            "description": "Successfully introduce your new offering"
        },
        "retain_customers": {
            "display_name": "Retain Customers",
            "icon": "🔄",
            "description": "Keep customers coming back"
        }
    }
    
    index = {}
    
    # Process each category
    for category_folder, display_info in category_display.items():
        category_data = {
            "category": category_folder,
            "display_name": display_info["display_name"],
            "icon": display_info["icon"],
            "description": display_info["description"],
            "questions": []
        }
        
        # Load all 5 questions for this category
        for question_num in range(1, 6):
            question_data = load_question_file(category_folder, question_num, templates_dir)
            
            if question_data:
                question_info = {
                    "question_number": question_data.get("question_number", question_num),
                    "question_text": question_data.get("question_text", ""),
                    "file_path": f"{category_folder}/question_{question_num}.json",
                    "category": category_folder
                }
                category_data["questions"].append(question_info)
        
        # Only add if we have questions
        if category_data["questions"]:
            index[category_folder] = category_data
    
    # Write to file
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(index, f, indent=2, ensure_ascii=False)
    
    print(f"Generated questions index: {output_file}")
    print(f"Categories: {len(index)}")
    print(f"Total questions: {sum(len(cat['questions']) for cat in index.values())}")
    
    return index

if __name__ == '__main__':
    generate_questions_index()

