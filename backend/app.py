import os
import logging
import uuid
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

# ===== CHAT ENDPOINTS =====

@app.route('/api/chat/start', methods=['POST'])
def chat_start():
    """Start a new chat session for a business category"""
    try:
        if not request.is_json:
            return jsonify({
                "success": False,
                "error": "Request must be JSON"
            }), 400
        
        data = request.get_json()
        category = data.get('category', '').strip().lower()
        
        if not category:
            return jsonify({
                "success": False,
                "error": "Category is required"
            }), 400
        
        # Validate category
        valid_categories = ['restaurant', 'retail_store', 'professional_services', 'ecommerce', 'local_services']
        if category not in valid_categories:
            return jsonify({
                "success": False,
                "error": f"Invalid category. Must be one of: {', '.join(valid_categories)}"
            }), 400
        
        # Create new session
        session_id = str(uuid.uuid4())
        chat_sessions[session_id] = {
            "session_id": session_id,
            "category": category,
            "answers": {},
            "conversation": [],
            "created_at": datetime.now().isoformat(),
            "current_question_id": None  # Track which question we're currently asking
        }
        
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
        chat_sessions[session_id]["current_question_id"] = first_question_obj["id"]
        
        # Add welcome message to conversation
        chat_sessions[session_id]["conversation"].append({
            "role": "assistant",
            "content": welcome_text,
            "timestamp": datetime.now().isoformat(),
            "question_id": first_question_obj["id"]
        })
        
        first_question = welcome_text
        
        logger.info(f"Chat session started: {session_id} for category: {category}")
        
        return jsonify({
            "success": True,
            "session_id": session_id,
            "first_question": first_question,
            "conversation": chat_sessions[session_id]["conversation"]
        })
        
    except Exception as e:
        logger.error(f"Error starting chat session: {str(e)}")
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
        session_id = data.get('session_id', '').strip()
        user_message = data.get('user_message', '').strip()
        
        if not session_id:
            return jsonify({
                "success": False,
                "error": "Session ID is required"
            }), 400
        
        if not user_message:
            return jsonify({
                "success": False,
                "error": "User message is required"
            }), 400
        
        # Validate message length (prevent extremely long messages)
        if len(user_message) > 5000:
            return jsonify({
                "success": False,
                "error": "Message is too long. Please keep responses under 5000 characters."
            }), 400
        
        # Check if session exists
        if session_id not in chat_sessions:
            return jsonify({
                "success": False,
                "error": "Session not found. Your session may have expired. Please start a new chat."
            }), 404
        
        session = chat_sessions[session_id]
        
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
        
        logger.info(f"Chat message processed for session: {session_id}. Questions answered: {len(session['answers'])}. Complete: {is_complete}")
        
        return jsonify({
            "success": True,
            "ai_response": ai_response,
            "is_complete": is_complete,
            "conversation": session["conversation"],
            "questions_answered": len(session["answers"])
        })
        
    except Exception as e:
        logger.error(f"Error processing chat message: {str(e)}")
        return jsonify({
            "success": False,
            "error": "An unexpected error occurred"
        }), 500

@app.route('/api/chat/generate-plan', methods=['POST'])
def chat_generate_plan():
    """Generate final marketing plan based on collected answers"""
    try:
        if not request.is_json:
            return jsonify({
                "success": False,
                "error": "Request must be JSON"
            }), 400
        
        data = request.get_json()
        session_id = data.get('session_id', '').strip()
        
        if not session_id:
            return jsonify({
                "success": False,
                "error": "Session ID is required"
            }), 400
        
        # Check if session exists
        if session_id not in chat_sessions:
            return jsonify({
                "success": False,
                "error": "Session not found. Your session may have expired. Please start a new chat."
            }), 404
        
        session = chat_sessions[session_id]
        
        if not openai_client:
            return jsonify({
                "success": False,
                "error": "OpenAI client not initialized"
            }), 500
        
        # Check if all required questions are answered
        if not is_flow_complete(session["category"], session["answers"]):
            return jsonify({
                "success": False,
                "error": "Please answer all questions before generating the plan"
            }), 400
        
        # Use chat_flows.py to generate structured marketing plan prompt
        marketing_plan_prompt = generate_marketing_plan_prompt(
            session["category"],
            session["answers"]
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
            
            logger.info(f"Marketing plan generated for session: {session_id}. Tokens used: {tokens_used}")
            
            return jsonify({
                "success": True,
                "marketing_plan": marketing_plan,
                "metadata": {
                    "model": "gpt-4o",
                    "tokens_used": tokens_used,
                    "category": session["category"]
                }
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

@app.route('/api/chat/session/<session_id>', methods=['GET'])
def get_chat_session(session_id):
    """Get conversation history for a session"""
    try:
        if not session_id:
            return jsonify({
                "success": False,
                "error": "Session ID is required"
            }), 400
        
        # Check if session exists
        if session_id not in chat_sessions:
            return jsonify({
                "success": False,
                "error": "Session not found. Your session may have expired. Please start a new chat."
            }), 404
        
        session = chat_sessions[session_id]
        
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

if __name__ == '__main__':
    # Initialize OpenAI client on startup
    if not initialize_openai():
        logger.error("Failed to initialize OpenAI client. Check your API key.")
        exit(1)
    
    # Get port from environment or default to 5001 (5000 often used by AirPlay on macOS)
    port = int(os.getenv('PORT', 5001))
    
    logger.info(f"Starting Flask app on port {port}")
    app.run(host='0.0.0.0', port=port, debug=os.getenv('FLASK_ENV') == 'development')
