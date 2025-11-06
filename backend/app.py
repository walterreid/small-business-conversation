import os
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from openai import OpenAI
import re

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
            "http://localhost:3000",  # Alternative local frontend port
            "https://meta-prompt-generator-frontend.onrender.com",  # Production frontend
            "https://meta-prompt-generator.onrender.com",  # Alternative production URL
        ],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "supports_credentials": True
    }
})

# Initialize OpenAI client
openai_client = None

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
        "service": "meta-prompt-generator"
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

if __name__ == '__main__':
    # Initialize OpenAI client on startup
    if not initialize_openai():
        logger.error("Failed to initialize OpenAI client. Check your API key.")
        exit(1)
    
    # Load and validate meta-prompt template
    if not load_meta_prompt():
        logger.error("Failed to load meta-prompt template. Check file path.")
        exit(1)
    
    # Get port from environment or default to 5000
    port = int(os.getenv('PORT', 5000))
    
    logger.info(f"Starting Flask app on port {port}")
    app.run(host='0.0.0.0', port=port, debug=os.getenv('FLASK_ENV') == 'development')
