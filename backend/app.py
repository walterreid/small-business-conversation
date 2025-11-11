import os
import logging
import uuid
import json
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from openai import OpenAI
import re
from chat_flows import (
    get_next_question,
    is_flow_complete,
    generate_marketing_plan_prompt,
    extract_answer_from_message
)
from security import (
    sanitize_string,
    sanitize_form_answers,
    validate_question_ids,
    validate_json_structure,
    validate_category,
    validate_session_id,
    check_rate_limit,
    get_client_identifier,
    sanitize_for_ai,
    validate_form_answers_structure
)
from security.input_validator import validate_message as validate_message_security
from security.rate_limiter import RateLimiter
from security.session_manager import SessionManager
from security.system_prompt_wrapper import create_protected_system_prompt
from template_loader import (
    load_template,
    get_available_categories,
    get_template_opening_dialog,
    get_template_questions,
    fill_template_with_answers
)
from diagnostic_engine import (
    load_all_template_questions,
    match_questions,
    explain_why_match
)

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Configure CORS for production and development
CORS(app, resources={
    r"/api/*": {
        "origins": [
            "http://localhost:3001",  # Local development frontend
            "https://small-business-marketing-tool-frontend.onrender.com",  # Production frontend
        ],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "supports_credentials": True
    }
})

# Initialize OpenAI client
openai_client = None

# In-memory session storage (will be replaced with database in future)
chat_sessions = {}

# Initialize security modules
rate_limiter = RateLimiter()
session_manager = SessionManager()

def initialize_openai():
    """Initialize OpenAI client with API key validation"""
    global openai_client
    api_key = os.getenv('OPENAI_API_KEY')
    
    if not api_key:
        logger.error("OPENAI_API_KEY not found in environment variables")
        return False
    
    if not api_key.startswith('sk-'):
        logger.error("OPENAI_API_KEY appears to be invalid (should start with 'sk-')")
        return False
    
    try:
        openai_client = OpenAI(api_key=api_key)
        logger.info("OpenAI client initialized successfully")
        return True
    except Exception as e:
        logger.error(f"Failed to initialize OpenAI client: {str(e)}")
        return False

def load_meta_prompt():
    """Load the meta-prompt template from file"""
    try:
        meta_prompt_path = os.path.join(os.path.dirname(__file__), 'prompts', 'meta-prompt-system.md')
        
        if not os.path.exists(meta_prompt_path):
            logger.error(f"Meta-prompt file not found at: {meta_prompt_path}")
            return None
        
        with open(meta_prompt_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract the actual prompt from the markdown file
        # Look for the prompt section that starts with "You are a prompt architect"
        prompt_start = content.find("You are a prompt architect")
        if prompt_start == -1:
            logger.error("Could not find the prompt section in meta-prompt-system.md")
            return None
        
        # Extract everything from the prompt start to the end of the file
        prompt_content = content[prompt_start:]
        
        logger.info("Meta-prompt template loaded successfully")
        return prompt_content
        
    except Exception as e:
        logger.error(f"Failed to load meta-prompt: {str(e)}")
        return None

def replace_template_variables(template, user_domain, user_framing=""):
    """Replace {{userDomain}} and {{userFraming}} placeholders in the template"""
    try:
        # Replace userDomain
        template = template.replace("{{userDomain}}", user_domain)
        
        # Replace userFraming (handle empty case)
        if user_framing:
            template = template.replace("{{userFraming}}", user_framing)
        else:
            # Remove the userFraming line if it's empty
            template = re.sub(r"{{userFraming}}\n?", "", template)
        
        return template
    except Exception as e:
        logger.error(f"Failed to replace template variables: {str(e)}")
        return None

@app.before_request
def apply_security():
    """Apply security checks to all requests"""
    # Skip security for health check
    if request.path == '/health':
        return None
    
    # Skip for OPTIONS requests (CORS preflight)
    if request.method == 'OPTIONS':
        return None
    
    # Rate limiting
    ip_address = get_client_identifier(request)
    allowed, reason = rate_limiter.is_allowed(ip_address, max_requests=20, window_seconds=60)
    
    if not allowed:
        logger.warning(f"Rate limit exceeded for IP: {ip_address}")
        return jsonify({
            "success": False,
            "error": reason
        }), 429
    
    return None

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "small-business-marketing-tool"
    })

@app.route('/api/generate-template', methods=['POST'])
def generate_template():
    """Generate a custom prompt template using OpenAI"""
    try:
        # Validate request data
        if not request.is_json:
            return jsonify({
                "success": False,
                "error": "Request must be JSON"
            }), 400
        
        data = request.get_json()
        
        # Validate required fields
        if 'userDomain' not in data:
            return jsonify({
                "success": False,
                "error": "userDomain is required"
            }), 400
        
        user_domain = data['userDomain'].strip()
        user_framing = data.get('userFraming', '').strip()
        
        # Sanitize inputs
        user_domain = sanitize_string(user_domain, max_length=1000)
        user_framing = sanitize_string(user_framing, max_length=1000)
        
        if not user_domain:
            return jsonify({
                "success": False,
                "error": "userDomain cannot be empty"
            }), 400
        
        # Check if OpenAI client is initialized
        if not openai_client:
            logger.error("OpenAI client not initialized")
            return jsonify({
                "success": False,
                "error": "Service configuration error. Please check API key."
            }), 500
        
        # Load meta-prompt template
        meta_prompt_template = load_meta_prompt()
        if not meta_prompt_template:
            logger.error("Failed to load meta-prompt template")
            return jsonify({
                "success": False,
                "error": "Service configuration error. Template not found."
            }), 500
        
        # Replace template variables
        filled_prompt = replace_template_variables(meta_prompt_template, user_domain, user_framing)
        if not filled_prompt:
            logger.error("Failed to replace template variables")
            return jsonify({
                "success": False,
                "error": "Service configuration error. Template processing failed."
            }), 500
        
        logger.info(f"Generating template for domain: {user_domain}")
        
        # Call OpenAI API
        try:
            response = openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "user",
                        "content": filled_prompt
                    }
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            # Extract the response content
            ai_output = response.choices[0].message.content
            
            # Get usage information
            usage = response.usage
            tokens_used = usage.total_tokens if usage else 0
            
            logger.info(f"OpenAI API call successful. Tokens used: {tokens_used}")
            
            return jsonify({
                "success": True,
                "output": ai_output,
                "metadata": {
                    "model": "gpt-4o",
                    "tokens_used": tokens_used,
                    "domain": user_domain,
                    "framing": user_framing if user_framing else None
                }
            })
            
        except Exception as e:
            logger.error(f"OpenAI API call failed: {str(e)}")
            return jsonify({
                "success": False,
                "error": "Failed to generate template. Please try again."
            }), 500
        
    except Exception as e:
        logger.error(f"Unexpected error in generate_template: {str(e)}")
        return jsonify({
            "success": False,
            "error": "An unexpected error occurred. Please try again."
        }), 500

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        "success": False,
        "error": "Endpoint not found"
    }), 404

@app.errorhandler(405)
def method_not_allowed(error):
    """Handle 405 errors"""
    return jsonify({
        "success": False,
        "error": "Method not allowed"
    }), 405

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Internal server error: {str(error)}")
    return jsonify({
        "success": False,
        "error": "Internal server error"
    }), 500

@app.route('/api/feedback', methods=['POST'])
def receive_feedback():
    """Store user feedback (optional endpoint)"""
    try:
        data = request.get_json()
        feedback_type = data.get('type')
        domain = data.get('domain', '')
        metadata = data.get('metadata', {})
        
        # Log feedback (you could store in database later)
        logger.info(f"Feedback received: {feedback_type} for domain: {domain[:50]}...")
        logger.info(f"Metadata: {metadata}")
        
        # For now, just acknowledge receipt
        return jsonify({
            "success": True,
            "message": "Feedback received"
        })
    except Exception as e:
        logger.error(f"Feedback endpoint error: {str(e)}")
        # Don't fail - feedback is optional
        return jsonify({"success": True}), 200

@app.route('/api/try-prompt', methods=['POST', 'OPTIONS'])
def try_prompt():
    """Generate example output using the filled prompt"""
    if request.method == 'OPTIONS':
        # Handle preflight request
        return jsonify({"status": "ok"}), 200
    
    try:
        data = request.get_json()
        prompt = data.get('prompt', '').strip()
        
        # Sanitize prompt
        prompt = sanitize_string(prompt, max_length=5000)
        
        if not prompt:
            return jsonify({
                "success": False,
                "error": "Prompt is required"
            }), 400
        
        if not openai_client:
            return jsonify({
                "success": False,
                "error": "OpenAI client not initialized"
            }), 500
        
        logger.info("Generating example output from filled prompt")
        
        # Call OpenAI with the user's filled prompt
        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=1000
        )
        
        output = response.choices[0].message.content
        tokens_used = response.usage.total_tokens if response.usage else 0
        
        logger.info(f"Example output generated. Tokens used: {tokens_used}")
        
        return jsonify({
            "success": True,
            "output": output,
            "metadata": {
                "model": "gpt-4o",
                "tokens_used": tokens_used
            }
        })
        
    except Exception as e:
        logger.error(f"Try prompt failed: {str(e)}")
        return jsonify({
            "success": False,
            "error": "Failed to generate example output"
        }), 500

# ===== FRAMEWORK INSIGHTS FUNCTIONS =====

def load_question_template(category, question_number):
    """Load a specific question template."""
    template_path = os.path.join(
        os.path.dirname(__file__),
        'prompts',
        'generated_templates',
        category,
        f'question_{question_number}.json'
    )
    
    if os.path.exists(template_path):
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading template {template_path}: {e}")
            return None
    
    return None


def extract_unique_value_from_question(question):
    """
    Extract unique value proposition from question template.
    Pulls from prompt_template, smb_insights, or other unique aspects.
    """
    unique_parts = []
    
    # Extract from prompt_template if available
    prompt_template = question.get('prompt_template', '')
    if prompt_template:
        # Look for "Approach:" section
        if 'Approach:' in prompt_template:
            try:
                parts = prompt_template.split('Approach:')
                if len(parts) > 1:
                    approach_text = parts[1].split('\n\n')[0].strip()
                    if approach_text:
                        # Take first sentence or first 100 chars
                        sentences = [s.strip() for s in approach_text.split('.') if s.strip() and len(s.strip()) > 20]
                        if sentences:
                            unique_parts.append(sentences[0])
            except:
                pass
        
        # Look for "Focus:" in constraints
        if 'Focus:' in prompt_template:
            try:
                parts = prompt_template.split('Focus:')
                if len(parts) > 1:
                    focus_text = parts[1].split('\n')[0].strip()
                    if focus_text and len(focus_text) > 10:
                        unique_parts.append(focus_text)
            except:
                pass
    
    # Extract from smb_insights if available
    smb_insights = question.get('smb_insights', {})
    if smb_insights:
        effective_channels = smb_insights.get('effective_channels', [])
        if effective_channels:
            # Take first 2-3 channels as unique value
            channel_str = ', '.join(effective_channels[:3])
            if channel_str:
                unique_parts.append(f"Focuses on proven channels: {channel_str}")
    
    # If we have unique parts, combine them
    if unique_parts:
        return ' • '.join(unique_parts[:2])  # Max 2 parts
    
    # Fallback: use category description
    category = question.get('category', '').replace('_', ' ').title()
    return f"Tailored strategies for {category}"


def determine_budget_tier(budget_string):
    """Determine budget tier from user input."""
    if not budget_string:
        return None
    
    budget_lower = str(budget_string).lower()
    
    # Check for specific budget ranges
    if 'under' in budget_lower or '<' in budget_lower:
        if '500' in budget_lower:
            return "Under $500"
    
    if '500' in budget_lower and ('1000' in budget_lower or '1k' in budget_lower or '1,000' in budget_lower):
        return "$500-1000"
    
    if '1000' in budget_lower or '1k' in budget_lower or '1,000' in budget_lower:
        if '2500' in budget_lower or '2.5k' in budget_lower or '2,500' in budget_lower:
            return "$1000-2500"
        elif '5000' not in budget_lower and '5k' not in budget_lower:
            return "$1000-2500"
    
    if '2500' in budget_lower or '2.5k' in budget_lower or '2,500' in budget_lower:
        if '5000' in budget_lower or '5k' in budget_lower or '5,000' in budget_lower:
            return "$2500-5000"
    
    if '5000' in budget_lower or '5k' in budget_lower or '5,000' in budget_lower:
        if '+' in budget_lower or 'over' in budget_lower or 'more' in budget_lower:
            return "$5000+"
        return "$2500-5000"
    
    # Default
    return None


def extract_framework_insights(category, question_number, current_answers, new_answers):
    """
    Extract what the framework is doing based on current answers.
    Returns insights to show in the sidebar.
    """
    try:
        # Load the question template
        template = load_question_template(category, question_number)
        if not template:
            return None
        
        # Merge answers
        all_answers = {**current_answers, **new_answers}
        
        insights = {
            'framework_name': f"{category.replace('_', ' ').title()} Framework",
            'anti_patterns': template.get('anti_patterns', []),
            'active_strategies': [],
            'budget_allocation': None,
            'focusing_on': [],
            'avoiding': []
        }
        
        # Extract budget info if available
        budget_answer = None
        for key, value in all_answers.items():
            if 'budget' in key.lower() and value:
                budget_answer = value
                break
        
        if budget_answer:
            # Parse budget and get allocation
            smb_insights = template.get('smb_insights', {})
            budget_allocations = smb_insights.get('budget_allocations', {})
            
            # Determine budget tier
            budget_tier = determine_budget_tier(budget_answer)
            
            if budget_tier and budget_tier in budget_allocations:
                allocation = budget_allocations[budget_tier]
                
                insights['budget_allocation'] = {
                    'tier': budget_tier,
                    'focus': allocation.get('focus', ''),
                    'channels': allocation.get('channels', [])
                }
                
                # Add to focusing_on
                insights['focusing_on'].extend(allocation.get('channels', []))
        
        # Extract industry-specific insights
        industry_answer = all_answers.get('industry') or all_answers.get('businessType')
        if industry_answer:
            insights['active_strategies'].append(
                f"Industry-specific tactics for {industry_answer}"
            )
            insights['focusing_on'].append(f"Industry-specific strategies for {industry_answer}")
        
        # Extract location insights
        location_answer = all_answers.get('location') or all_answers.get('urbanAreas') or all_answers.get('service_area')
        if location_answer:
            insights['active_strategies'].append(
                f"Location-optimized for {location_answer}"
            )
            insights['focusing_on'].append(f"Location-based tactics for {location_answer}")
        
        # Add avoiding strategies based on anti-patterns and budget
        if budget_answer:
            budget_tier = determine_budget_tier(budget_answer)
            if budget_tier:
                if budget_tier == "Under $500":
                    insights['avoiding'].extend([
                        "Expensive paid advertising campaigns",
                        "High-cost influencer partnerships",
                        "Premium marketing tools"
                    ])
                elif budget_tier in ["$500-1000", "$1000-2500"]:
                    insights['avoiding'].extend([
                        "Enterprise-level marketing platforms",
                        "High-cost influencer partnerships"
                    ])
        
        insights['avoiding'].append("Generic one-size-fits-all tactics")
        
        return insights
        
    except Exception as e:
        logger.error(f"Error extracting framework insights: {e}", exc_info=True)
        return None


# ===== CHAT ENDPOINTS =====

@app.route('/api/chat/start', methods=['POST'])
def chat_start():
    """
    Start a new chat session for a business category or marketing goal.
    
    Supports both:
    - Template-based categories (marketing goals: increase_sales, build_brand_awareness, etc.)
    - chat_flows.py categories (business types: restaurant, retail_store, etc.)
    """
    try:
        ip_address = get_client_identifier(request)
        data = request.get_json()
        
        # Validate request
        if not data or 'category' not in data:
            return jsonify({
                "success": False,
                "error": "Category is required"
            }), 400
        
        category = data.get('category', '').strip().lower()
        question_number = data.get('question_number')  # Optional: for question-specific templates
        
        # Sanitize category
        category = sanitize_string(category, max_length=100)
        
        # Validate question_number if provided
        if question_number is not None:
            try:
                question_number = int(question_number)
                if question_number < 1 or question_number > 5:
                    return jsonify({
                        "success": False,
                        "error": "Question number must be between 1 and 5"
                    }), 400
            except (ValueError, TypeError):
                return jsonify({
                    "success": False,
                    "error": "Invalid question number"
                }), 400
        
        # Define business type categories (use chat_flows.py, not templates)
        valid_chat_flows_categories = [
            'restaurant', 'retail_store', 'professional_services', 
            'ecommerce', 'local_services'
        ]
        
        # Check if category uses template system (marketing goals)
        # Business types should use chat_flows.py even if a template exists
        available_template_categories = get_available_categories()
        is_business_type = category in valid_chat_flows_categories
        uses_template = category in available_template_categories and not is_business_type
        
        # Validate category exists (either in templates or chat_flows)
        if not uses_template and not is_business_type:
            # Provide helpful error with both options
            template_list = ', '.join([c for c in available_template_categories if c not in valid_chat_flows_categories]) if available_template_categories else 'none'
            business_list = ', '.join(valid_chat_flows_categories)
            return jsonify({
                "success": False,
                "error": f"Invalid category '{category}'. Available marketing goal categories: {template_list}. Available business type categories: {business_list}"
            }), 400
        
        # Create secure session
        try:
            session_id, security_token = session_manager.create_session(ip_address, category)
        except ValueError as e:
            return jsonify({
                "success": False,
                "error": str(e)
            }), 400
        
        # Get session data
        session = session_manager.get_session(session_id)
        if not session:
            return jsonify({
                "success": False,
                "error": "Failed to create session"
            }), 500
        
        # Store whether using template
        session['uses_template'] = uses_template
        
        if uses_template:
            # Load pre-generated template (question-specific if question_number provided)
            template = load_template(category, question_number=question_number)
            if not template:
                logger.error(f"Template not found for category: {category}, question: {question_number}")
                return jsonify({
                    "success": False,
                    "error": "Template not available for this category/question"
                }), 500
            
            # Store template in session
            session['template'] = template
            session['current_question_index'] = 0
            session['question_number'] = question_number  # Store for framework insights
            
            # Get opening dialog
            opening_dialog = template.get('opening_dialog', get_template_opening_dialog(category))
            
            # Get all questions for sidebar form
            questions = template.get('questions', [])
            first_question = questions[0] if questions else None
            
            if not first_question:
                logger.error(f"No questions in template for: {category}")
                return jsonify({
                    "success": False,
                    "error": "Template configuration error"
                }), 500
            
            # Add opening dialog to conversation
            session['conversation'].append({
                'role': 'assistant',
                'content': opening_dialog,
                'timestamp': datetime.now().isoformat()
            })
            
            # Update session
            session_manager.update_session(session_id, session)
            
            logger.info(f"Chat started (template) - Session: {session_id}, Category: {category}")
            
            return jsonify({
                "success": True,
                "session_id": session_id,
                "security_token": security_token,
                "category": category,
                "opening_dialog": opening_dialog,
                "questions": questions,  # All questions for sidebar
                "first_question": first_question,  # First question for chat
                "anti_patterns": template.get('anti_patterns', []),
                "total_questions": len(questions),
                "uses_template": True,
                "conversation": session['conversation']
            })
        else:
            # Use existing chat_flows.py system
            # Get first question from chat_flows.py
            first_question_obj = get_next_question(category, {})
            
            if not first_question_obj:
                return jsonify({
                    "success": False,
                    "error": "No questions found for this category"
                }), 500
            
            # Build welcome message with first question
            welcome_text = f"Hi! I'm here to help you create a marketing plan for your {category.replace('_', ' ')} business. Let's start with a few questions.\n\n{first_question_obj['question']}"
            if first_question_obj.get('help_text'):
                welcome_text += f"\n\n💡 {first_question_obj['help_text']}"
            
            # Store current question ID
            session['current_question_id'] = first_question_obj["id"]
            
            # Add welcome message to conversation
            session['conversation'].append({
                "role": "assistant",
                "content": welcome_text,
                "timestamp": datetime.now().isoformat(),
                "question_id": first_question_obj["id"]
            })
            
            # Update session
            session_manager.update_session(session_id, session)
            
            logger.info(f"Chat started (chat_flows) - Session: {session_id}, Category: {category}")
            
            return jsonify({
                "success": True,
                "session_id": session_id,
                "security_token": security_token,
                "category": category,
                "opening_dialog": welcome_text,
                "first_question": first_question_obj,
                "uses_template": False,
                "conversation": session['conversation']
            })
        
    except Exception as e:
        logger.error(f"Error starting chat session: {str(e)}", exc_info=True)
        return jsonify({
            "success": False,
            "error": "Failed to start chat session"
        }), 500

@app.route('/api/chat/message', methods=['POST'])
def chat_message():
    """Handle ongoing conversation messages"""
    try:
        if not request.is_json:
            return jsonify({
                "success": False,
                "error": "Request must be JSON"
            }), 400
        
        data = request.get_json()
        
        # Validate JSON structure
        is_valid, struct_error = validate_json_structure(
            data, 
            required_fields=['session_id', 'user_message'],
            optional_fields=['form_answers']
        )
        if not is_valid:
            return jsonify({
                "success": False,
                "error": struct_error
            }), 400
        
        session_id = data.get('session_id', '').strip()
        user_message = data.get('user_message', '').strip()
        form_answers = data.get('form_answers', {})
        
        # Validate session ID format
        if not validate_session_id(session_id):
            return jsonify({
                "success": False,
                "error": "Invalid session ID format"
            }), 400
        
        # Sanitize user message
        user_message = sanitize_string(user_message, max_length=5000)
        
        # Allow empty message if form answers are provided (for template flows)
        if not user_message and not form_answers:
            return jsonify({
                "success": False,
                "error": "User message or form answers required"
            }), 400
        
        # Sanitize and validate form answers if provided
        if form_answers:
            if not isinstance(form_answers, dict):
                return jsonify({
                    "success": False,
                    "error": "Form answers must be a dictionary"
                }), 400
            
            # Sanitize form answers
            form_answers = sanitize_form_answers(form_answers)
            
            # Validate form answers structure
            if len(form_answers) > 50:  # Reasonable limit
                return jsonify({
                    "success": False,
                    "error": "Too many form answers"
                }), 400
        
        # Validate session using SessionManager
        ip_address = get_client_identifier(request)
        is_valid, error_msg, session = session_manager.validate_session(session_id, ip_address)
        
        if not is_valid:
            return jsonify({
                "success": False,
                "error": error_msg or "Session not found. Your session may have expired. Please start a new chat."
            }), 404
        
        # Increment request count
        session_manager.increment_request_count(session_id)
        
        # Check if this is a template-based flow
        uses_template = session.get("uses_template", False)
        
        if uses_template:
            # Template-based flow: Process with OpenAI using template context
            # Merge form answers into session answers
            if form_answers:
                session["answers"].update(form_answers)
            
            # Add user message to conversation (only if not empty)
            if user_message:
                session["conversation"].append({
                    "role": "user",
                    "content": user_message,
                    "timestamp": datetime.now().isoformat()
                })
            
            # Get template and build context
            template = session.get("template")
            if not template:
                return jsonify({
                    "success": False,
                    "error": "Template not found in session"
                }), 500
            
            # Fill template with answers
            from template_loader import fill_template_with_answers
            prompt_template = template.get("prompt_template", "")
            filled_template = fill_template_with_answers(prompt_template, session["answers"])
            
            # Build OpenAI message with context
            # For template flows, we pass the filled template as the prompt and answers as user_answers
            system_prompt = create_protected_system_prompt(filled_template, session["answers"])
            
            # Get conversation history for context
            conversation_messages = [
                {"role": "system", "content": system_prompt}
            ]
            
            # Add recent conversation history (last 10 messages for context)
            recent_conversation = session["conversation"][-10:]
            for msg in recent_conversation:
                conversation_messages.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })
            
            # Call OpenAI
            if not openai_client:
                logger.error("OpenAI client not initialized")
                return jsonify({
                    "success": False,
                    "error": "OpenAI client not initialized"
                }), 500
            
            # Always include form answers in user message context (even if user typed a message)
            # This ensures the AI knows about all the form data
            user_message_content = user_message if user_message else ""
            
            # Add form answers context to user message
            if form_answers:
                form_context = f"\n\nUser has provided the following information:\n{json.dumps(form_answers, indent=2)}"
                user_message_content = (user_message_content + form_context).strip()
            
            # Ensure we have at least one user message
            if not any(msg.get("role") == "user" for msg in conversation_messages):
                if not user_message_content:
                    user_message_content = "User is ready to start the conversation."
                conversation_messages.append({
                    "role": "user",
                    "content": user_message_content
                })
            elif user_message_content and (not recent_conversation or recent_conversation[-1].get("content") != user_message_content):
                # Update the last user message or add new one with form context
                # Remove the last user message if it exists and add updated one
                conversation_messages = [msg for msg in conversation_messages if msg.get("role") != "user" or msg != conversation_messages[-1]]
                conversation_messages.append({
                    "role": "user",
                    "content": user_message_content
                })
            
            try:
                logger.info(f"Calling OpenAI with {len(conversation_messages)} messages")
                response = openai_client.chat.completions.create(
                    model="gpt-4o",
                    messages=conversation_messages,
                    temperature=0.7,
                    max_tokens=1000
                )
                
                ai_response = response.choices[0].message.content
                
                # Add AI response to conversation
                session["conversation"].append({
                    "role": "assistant",
                    "content": ai_response,
                    "timestamp": datetime.now().isoformat()
                })
                
                # Check if we have enough answers to generate plan
                template_questions = template.get("questions", [])
                required_questions = [q for q in template_questions if q.get("required", False)]
                answered_required = sum(1 for q in required_questions if session["answers"].get(q["id"]))
                
                is_complete = answered_required >= len(required_questions)
                
            except Exception as e:
                logger.error(f"OpenAI API error: {str(e)}")
                return jsonify({
                    "success": False,
                    "error": "Failed to get AI response"
                }), 500
        else:
            # chat_flows-based flow: Sequential questions
            # Get current question ID
            current_question_id = session.get("current_question_id")
            
            if not current_question_id:
                return jsonify({
                    "success": False,
                    "error": "No active question. Please start a new session."
                }), 400
            
            # Extract and store the answer
            # Get the question object to help with extraction
            from chat_flows import get_all_questions
            all_questions = get_all_questions(session["category"])
            current_question = next((q for q in all_questions if q["id"] == current_question_id), None)
            
            if current_question:
                # Extract answer from message
                answer = extract_answer_from_message(user_message, current_question)
                session["answers"][current_question_id] = answer
            
            # Add user message to conversation
            session["conversation"].append({
                "role": "user",
                "content": user_message,
                "timestamp": datetime.now().isoformat(),
                "question_id": current_question_id
            })
            
            # Check if flow is complete
            is_complete = is_flow_complete(session["category"], session["answers"])
            
            if is_complete:
                # All questions answered - prepare completion message
                ai_response = "Perfect! I have all the information I need. Ready to generate your marketing plan?"
                session["current_question_id"] = None
            else:
                # Get next question
                next_question = get_next_question(session["category"], session["answers"])
                
                if not next_question:
                    # Shouldn't happen if is_flow_complete is working correctly
                    is_complete = True
                    ai_response = "Perfect! I have all the information I need. Ready to generate your marketing plan?"
                    session["current_question_id"] = None
                else:
                    # Build next question message
                    ai_response = next_question["question"]
                    if next_question.get("help_text"):
                        ai_response += f"\n\n💡 {next_question['help_text']}"
                    
                    # Store current question ID
                    session["current_question_id"] = next_question["id"]
            
            # Add AI response to conversation
            session["conversation"].append({
                "role": "assistant",
                "content": ai_response,
                "timestamp": datetime.now().isoformat(),
                "question_id": session.get("current_question_id")
            })
        
        # Extract framework insights for template-based sessions
        framework_insights = None
        if uses_template:
            category = session.get("category")
            question_number = session.get("question_number") or session.get("template", {}).get("question_number")
            if category and question_number:
                framework_insights = extract_framework_insights(
                    category,
                    question_number,
                    session.get("answers", {}),
                    form_answers if form_answers else {}
                )
        
        # Update session via SessionManager
        session_manager.update_session(session_id, session)
        
        logger.info(f"Chat message processed for session: {session_id}. Questions answered: {len(session['answers'])}. Complete: {is_complete}")
        
        response_data = {
            "success": True,
            "ai_response": ai_response,
            "is_complete": is_complete,
            "conversation": session["conversation"],
            "questions_answered": len(session["answers"])
        }
        
        # Add framework insights if available
        if framework_insights:
            response_data["framework_insights"] = framework_insights
        
        return jsonify(response_data)
        
    except Exception as e:
        logger.error(f"Error processing chat message: {str(e)}", exc_info=True)
        return jsonify({
            "success": False,
            "error": f"An unexpected error occurred: {str(e)}"
        }), 500

@app.route('/api/chat/generate-plan', methods=['POST'])
def chat_generate_plan():
    """Generate final marketing plan based on collected answers"""
    try:
        # Rate limiting (stricter for plan generation)
        client_id = get_client_identifier(request)
        is_allowed, rate_error = check_rate_limit(client_id, max_requests=5, window_seconds=60)
        if not is_allowed:
            return jsonify({
                "success": False,
                "error": rate_error
            }), 429
        
        if not request.is_json:
            return jsonify({
                "success": False,
                "error": "Request must be JSON"
            }), 400
        
        data = request.get_json()
        
        # Validate JSON structure
        is_valid, struct_error = validate_json_structure(data, required_fields=['session_id'])
        if not is_valid:
            return jsonify({
                "success": False,
                "error": struct_error
            }), 400
        
        session_id = data.get('session_id', '').strip()
        
        # Validate session ID format
        if not validate_session_id(session_id):
            return jsonify({
                "success": False,
                "error": "Invalid session ID format"
            }), 400
        
        # Validate session using SessionManager
        ip_address = get_client_identifier(request)
        is_valid, error_msg, session = session_manager.validate_session(session_id, ip_address)
        
        if not is_valid:
            return jsonify({
                "success": False,
                "error": error_msg or "Session not found. Your session may have expired. Please start a new chat."
            }), 404
        
        # Increment request count
        session_manager.increment_request_count(session_id)
        
        if not openai_client:
            return jsonify({
                "success": False,
                "error": "OpenAI client not initialized"
            }), 500
        
        # Check if this is a template-based flow
        uses_template = session.get("uses_template", False)
        
        if uses_template:
            # Template-based flow: Use template to generate plan
            template = session.get("template")
            if not template:
                return jsonify({
                    "success": False,
                    "error": "Template not found in session"
                }), 500
            
            # Check if all required questions are answered
            template_questions = template.get("questions", [])
            required_questions = [q for q in template_questions if q.get("required", False)]
            answered_required = sum(1 for q in required_questions if session["answers"].get(q["id"]))
            
            if answered_required < len(required_questions):
                return jsonify({
                    "success": False,
                    "error": f"Please answer all required questions ({answered_required}/{len(required_questions)} answered)"
                }), 400
            
            # Fill template with answers
            from template_loader import fill_template_with_answers
            prompt_template = template.get("prompt_template", "")
            filled_template = fill_template_with_answers(prompt_template, session["answers"])
            
            # Build protected system prompt
            system_prompt = create_protected_system_prompt(filled_template, session["answers"])
            
            # Create plan generation prompt
            marketing_plan_prompt = f"{system_prompt}\n\nGenerate a comprehensive marketing plan based on the above information. Include:\n1. Executive Summary\n2. Target Audience Analysis\n3. Recommended Marketing Channels\n4. 90-Day Action Plan\n5. Success Metrics\n6. Budget Allocation"
        else:
            # chat_flows-based flow: Use existing logic
            # Check if all required questions are answered
            if not is_flow_complete(session["category"], session["answers"]):
                return jsonify({
                    "success": False,
                    "error": "Please answer all questions before generating the plan"
                }), 400
            
            # Sanitize answers before generating plan
            sanitized_answers = {}
            for key, value in session["answers"].items():
                sanitized_answers[key] = sanitize_for_ai(str(value))
            
            # Use chat_flows.py to generate structured marketing plan prompt
            marketing_plan_prompt = generate_marketing_plan_prompt(
                session["category"],
                sanitized_answers
            )
        
        try:
            response = openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "user",
                        "content": marketing_plan_prompt
                    }
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            marketing_plan = response.choices[0].message.content
            tokens_used = response.usage.total_tokens if response.usage else 0
            
            # Build metadata with framework information
            metadata = {
                "model": "gpt-4o",
                "tokens_used": tokens_used,
                "category": session["category"]
            }
            
            # Add template-specific metadata
            if uses_template:
                question_number = session.get("question_number") or session.get("template", {}).get("question_number")
                if question_number:
                    metadata["question_number"] = question_number
                
                # Extract budget tier from answers
                answers = session.get("answers", {})
                budget_answer = None
                for key, value in answers.items():
                    if 'budget' in key.lower() and value:
                        budget_answer = value
                        break
                
                if budget_answer:
                    budget_tier = determine_budget_tier(budget_answer)
                    if budget_tier:
                        metadata["budget_tier"] = budget_tier
            
            logger.info(f"Marketing plan generated for session: {session_id}. Tokens used: {tokens_used}")
            
            return jsonify({
                "success": True,
                "marketing_plan": marketing_plan,
                "metadata": metadata
            })
            
        except Exception as e:
            logger.error(f"OpenAI API call failed: {str(e)}")
            return jsonify({
                "success": False,
                "error": "Failed to generate marketing plan. Please try again."
            }), 500
        
    except Exception as e:
        logger.error(f"Error generating marketing plan: {str(e)}")
        return jsonify({
            "success": False,
            "error": "An unexpected error occurred"
        }), 500

@app.route('/api/marketing-goals', methods=['GET'])
def get_marketing_goals():
    """Get all marketing goal categories with their questions"""
    try:
        index_path = os.path.join(os.path.dirname(__file__), 'config', 'marketing_questions_index.json')
        
        if not os.path.exists(index_path):
            return jsonify({
                "success": False,
                "error": "Marketing goals index not found"
            }), 404
        
        with open(index_path, 'r', encoding='utf-8') as f:
            index_data = json.load(f)
        
        return jsonify({
            "success": True,
            "goals": index_data
        })
        
    except Exception as e:
        logger.error(f"Error loading marketing goals: {str(e)}")
        return jsonify({
            "success": False,
            "error": "An unexpected error occurred"
        }), 500

@app.route('/api/marketing-goals/<category>/question/<int:question_number>', methods=['GET'])
def get_question_template(category, question_number):
    """Get full question template for a specific marketing goal question"""
    try:
        # Validate category
        valid_categories = ['increase_sales', 'build_brand_awareness', 'drive_foot_traffic', 
                           'generate_more_leads', 'launch_new_service_product', 'retain_customers']
        if category not in valid_categories:
            return jsonify({
                "success": False,
                "error": f"Invalid category. Must be one of: {', '.join(valid_categories)}"
            }), 400
        
        # Validate question number
        if question_number < 1 or question_number > 5:
            return jsonify({
                "success": False,
                "error": "Question number must be between 1 and 5"
            }), 400
        
        # Load the question template
        template_path = os.path.join(
            os.path.dirname(__file__),
            'prompts',
            'generated_templates',
            category,
            f'question_{question_number}.json'
        )
        
        if not os.path.exists(template_path):
            return jsonify({
                "success": False,
                "error": f"Question template not found for {category} question {question_number}"
            }), 404
        
        with open(template_path, 'r', encoding='utf-8') as f:
            template_data = json.load(f)
        
        return jsonify({
            "success": True,
            "template": template_data
        })
        
    except Exception as e:
        logger.error(f"Error loading question template: {str(e)}")
        return jsonify({
            "success": False,
            "error": "An unexpected error occurred"
        }), 500

@app.route('/api/diagnostic', methods=['POST'])
def run_diagnostic():
    """
    Run diagnostic to match user to best questions.
    
    Request body:
    {
        "pain_point": "not_enough_customers",
        "revenue_range": "under_10k",
        "tried_before": ["social_media", "ads"]
    }
    """
    try:
        if not request.is_json:
            return jsonify({
                "success": False,
                "error": "Request must be JSON"
            }), 400
        
        data = request.get_json()
        pain_point = data.get('pain_point')
        revenue_range = data.get('revenue_range')
        tried_before = data.get('tried_before', [])
        
        # Validate input
        if not pain_point or not revenue_range:
            return jsonify({
                "success": False,
                "error": "Missing required fields: pain_point and revenue_range"
            }), 400
        
        # Validate pain_point
        valid_pain_points = ["not_enough_customers", "no_visibility", "cant_keep_customers", "launching_something", "competing_with_big_brands", "sleeping_on_money"]
        if pain_point not in valid_pain_points:
            return jsonify({
                "success": False,
                "error": f"Invalid pain_point. Must be one of: {', '.join(valid_pain_points)}"
            }), 400
        
        # Validate revenue_range
        valid_revenue_ranges = ["under_10k", "10k_to_50k", "1k_to_2k", "2k_to_5k"]
        if revenue_range not in valid_revenue_ranges:
            return jsonify({
                "success": False,
                "error": f"Invalid revenue_range. Must be one of: {', '.join(valid_revenue_ranges)}"
            }), 400
        
        # Validate tried_before is a list
        if not isinstance(tried_before, list):
            return jsonify({
                "success": False,
                "error": "tried_before must be a list"
            }), 400
        
        # Load all questions once (can be cached in production)
        all_questions = load_all_template_questions()
        
        if not all_questions:
            logger.warning("No template questions found for diagnostic")
            return jsonify({
                "success": False,
                "error": "No questions available for matching"
            }), 500
        
        # Match questions
        matched = match_questions(pain_point, revenue_range, tried_before, all_questions)
        
        # Generate explanation
        reasoning = explain_why_match(pain_point, revenue_range, tried_before)
        
        # Format response with unique value extraction
        matched_questions = []
        for m in matched:
            question = m['question']
            
            # Extract unique value from question template
            unique_value = extract_unique_value_from_question(question)
            
            matched_questions.append({
                'category': question.get('category'),
                'question_number': question.get('question_number'),
                'question_text': question.get('question_text'),
                'match_score': m['score'],
                'why_this_fits': m['reasoning'],
                'unique_value': unique_value
            })
        
        logger.info(f"Diagnostic completed: {pain_point}, {revenue_range}, matched {len(matched_questions)} questions")
        
        return jsonify({
            'success': True,
            'matched_questions': matched_questions,
            'overall_reasoning': reasoning
        })
        
    except Exception as e:
        logger.error(f"Diagnostic error: {str(e)}", exc_info=True)
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/questions/all', methods=['GET'])
def get_all_questions():
    """Get all available template questions organized by category."""
    try:
        all_questions = load_all_template_questions()
        
        # Organize by category
        by_category = {}
        for q in all_questions:
            category = q.get('category')
            if not category:
                continue
            
            if category not in by_category:
                by_category[category] = []
            
            by_category[category].append({
                'question_number': q.get('question_number'),
                'question_text': q.get('question_text'),
                'anti_patterns': q.get('anti_patterns', [])
            })
        
        # Sort questions by question_number within each category
        for category in by_category:
            by_category[category].sort(key=lambda x: x.get('question_number', 0))
        
        return jsonify({
            'success': True,
            'categories': by_category,
            'total_questions': len(all_questions)
        })
        
    except Exception as e:
        logger.error(f"Error loading all questions: {str(e)}", exc_info=True)
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/sessions/clear', methods=['POST'])
def clear_sessions():
    """Clear all sessions for the requesting IP address"""
    try:
        ip_address = get_client_identifier(request)
        
        # Clear all sessions for this IP
        session_manager.clear_sessions_for_ip(ip_address)
        
        logger.info(f"Cleared all sessions for IP: {ip_address}")
        
        return jsonify({
            "success": True,
            "message": "All sessions cleared for your IP address"
        })
    except Exception as e:
        logger.error(f"Error clearing sessions: {str(e)}")
        return jsonify({
            "success": False,
            "error": "An unexpected error occurred"
        }), 500

@app.route('/api/chat/session/<session_id>', methods=['GET'])
def get_chat_session(session_id):
    """Get conversation history for a session"""
    try:
        # Validate session ID format
        if not validate_session_id(session_id):
            return jsonify({
                "success": False,
                "error": "Invalid session ID format"
            }), 400
        
        # Validate session using SessionManager
        ip_address = get_client_identifier(request)
        is_valid, error_msg, session = session_manager.validate_session(session_id, ip_address)
        
        if not is_valid:
            return jsonify({
                "success": False,
                "error": error_msg or "Session not found. Your session may have expired. Please start a new chat."
            }), 404
        
        return jsonify({
            "success": True,
            "session": {
                "session_id": session["session_id"],
                "category": session["category"],
                "conversation": session["conversation"],
                "answers": session["answers"],
                "created_at": session["created_at"]
            }
        })
        
    except Exception as e:
        logger.error(f"Error retrieving chat session: {str(e)}")
        return jsonify({
            "success": False,
            "error": "An unexpected error occurred"
        }), 500

# Initialize OpenAI client when module is imported (works for both direct run and gunicorn)
if not initialize_openai():
    logger.warning("OpenAI client not initialized. Set OPENAI_API_KEY environment variable.")
    logger.warning("The app will start but API endpoints requiring OpenAI will fail.")

if __name__ == '__main__':
    # Get port from environment or default to 5001 (5000 often used by AirPlay on macOS)
    port = int(os.getenv('PORT', 5001))
    
    logger.info(f"Starting Flask app on port {port}")
    app.run(host='0.0.0.0', port=port, debug=os.getenv('FLASK_ENV') == 'development')
