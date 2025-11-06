# Meta-Prompt Generator

Generate custom AI prompts tailored to your specific needs. Describe what you want help with, and get a structured prompt template with fill-in-the-blank questions that prevent generic output.

---

## What It Does

**The Problem**: Most people use AI with vague prompts like "write me wedding vows" and get generic, templated responses that could apply to anyone.

**The Solution**: This tool generates custom prompt templates that:
- Ask specific questions about your situation
- Include anti-patterns (what to avoid)
- Use constraints that force specificity
- Embed philosophical grounding about why the output matters

**Example Flow**:
1. You say: "I need help writing wedding vows"
2. System generates: A custom prompt template with 10+ specific questions
3. You fill in: Your names, shared memories, what you love about them, what to avoid
4. You get: A fully-formed prompt ready to use with ChatGPT/Claude that will produce authentic, specific vows

---

## Tech Stack

- **Backend**: Python/Flask
- **Frontend**: React
- **AI**: OpenAI GPT-4
- **Deployment**: Render
- **Version Control**: GitHub

---

## Local Development

### Prerequisites

- Python 3.9+
- Node.js 16+
- OpenAI API key

### Setup

```bash
# 1. Clone the repo
git clone https://github.com/yourusername/meta-prompt-generator.git
cd meta-prompt-generator

# 2. Backend setup
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY

# 3. Frontend setup (in new terminal)
cd frontend
npm install

# 4. Create prompts directory
cd backend
mkdir -p prompts
# Copy meta-prompt-system.md into backend/prompts/
```

### Running Locally

```bash
# Terminal 1 - Backend (http://localhost:5000)
cd backend
source venv/bin/activate
python app.py

# Terminal 2 - Frontend (http://localhost:3000)
cd frontend
npm start
```

Visit `http://localhost:3000` to use the app.

---

## Deployment

### Render (Recommended)

1. Push your code to GitHub
2. Connect your repo to Render
3. Render will detect `render.yaml` and create both services
4. Add environment variables in Render dashboard:
   - Backend: `OPENAI_API_KEY`
   - Frontend: `REACT_APP_API_URL` (your backend URL)

The app will auto-deploy on every push to main.

---

## Project Structure

```
/meta-prompt-generator
├── backend/
│   ├── app.py                    # Flask API
│   ├── requirements.txt          # Python dependencies
│   ├── .env                      # Environment variables (not committed)
│   └── prompts/
│       └── meta-prompt-system.md # The meta-prompt template (intent-based)
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── App.js               # Main React component
│   │   ├── App.css              # Styles
│   │   ├── api.js               # API client
│   │   └── index.js
│   └── package.json
├── test/                         # Test suite (not committed to git)
│   ├── test-scenarios.json      # 10 test scenarios covering all intent types
│   ├── test-runner.js           # Test execution engine
│   └── run-tests.sh             # Test runner script
├── render.yaml                   # Render deployment config
├── .gitignore                    # Includes test suite exclusion
├── README.md                     # This file
└── CLAUDE.md                     # AI assistant guidance
```

---

## How It Works

### Architecture

```
User Input
    ↓
Flask Backend (/api/generate-template)
    ↓
OpenAI API (with meta-prompt)
    ↓
Structured Response
    ↓
React Frontend (parses & renders form)
    ↓
User Fills Form
    ↓
Client-Side Template Filling
    ↓
Final Prompt
```

### The Two-Stage Process

**Stage 1: Template Generation** (uses OpenAI API)
- User describes their need
- Backend sends meta-prompt to GPT-4
- AI returns structured template with variables and questions

**Stage 2: Template Filling** (client-side)
- User answers questions in dynamic form
- Simple string replacement fills {{variables}}
- No API call needed - instant and free

### The Meta-Prompt

The core innovation is the meta-prompt in `backend/prompts/meta-prompt-system.md`. It instructs GPT-4 to:

1. **Anti-Brainstorm**: Identify common/overdone patterns to avoid
2. **Extract Variables**: Determine what info is needed for specificity
3. **Build Template**: Create structured prompt with {{variables}}
4. **Generate Questions**: Create user-facing questions for each variable

This meta-prompt is the "secret sauce" - it encodes knowledge about what makes good prompts.

---

## Key Features

### 1. Anti-Brainstorming
Shows users common patterns to avoid (e.g., "generic 'journey' language in wedding vows"). Pushes responses toward statistically unlikely but coherent territory.

### 2. Philosophical Grounding
Each prompt includes context about *why* the output matters:
- "Good vows are a gift from one person to another"
- "Performance reviews are growth tools, not report cards"

This shapes the AI's approach without being prescriptive.

### 3. Dynamic Form Generation
Every domain gets a custom form. Wedding vows need different questions than performance reviews.

### 4. "First Draft" Language
Reduces perfectionism by framing outputs as starting points, not final products.

---

## API Endpoints

### `POST /api/generate-template`

Generate a custom prompt template.

**Request:**
```json
{
  "userDomain": "I need help writing wedding vows",
  "userFraming": "Treat nuance as a feature, not noise"
}
```

**Response:**
```json
{
  "success": true,
  "output": "[ANTI-PATTERNS]\n...\n[PROMPT_TEMPLATE]\n...\n[USER_QUESTIONS]\n...",
  "metadata": {
    "model": "gpt-4o",
    "tokens_used": 2847,
    "domain": "wedding vows"
  }
}
```

### `GET /health`

Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "service": "meta-prompt-generator"
}
```

---

## Environment Variables

### Backend (`backend/.env`)

```bash
OPENAI_API_KEY=sk-...          # Your OpenAI API key
FLASK_ENV=development          # development or production
PORT=5000                      # Server port
```

### Frontend (`.env` or Render dashboard)

```bash
REACT_APP_API_URL=http://localhost:5000    # Backend URL
```

---

## Development Workflow

1. **Make changes** to backend or frontend
2. **Test locally** (both servers running)
3. **Commit and push** to GitHub
4. **Render auto-deploys** to production

### Updating the Meta-Prompt

The meta-prompt is the core of the system. To improve it:

1. Edit `backend/prompts/meta-prompt-system.md`
2. Test locally by generating a few prompts
3. Commit and push
4. Render will redeploy with the updated prompt

---

## Testing

### Manual Testing Checklist

- [ ] Input a domain (e.g., "wedding vows")
- [ ] Wait for template generation (10-20 seconds)
- [ ] Verify anti-patterns are shown
- [ ] Check that form renders with appropriate questions
- [ ] Fill in all required fields
- [ ] Generate final prompt
- [ ] Verify no {{variables}} remain in output
- [ ] Copy to clipboard works
- [ ] Test the prompt in ChatGPT/Claude

### Test Domains

Good test cases:
- Wedding vows (baseline - compare to marriedbyjosh.com)
- Performance review
- Apology letter
- Groomsman speech
- Product description
- Business proposal

### Current Implementation Status

**✅ Completed Features:**
- Full end-to-end meta-prompt generation system
- Professional UI with gradient backgrounds and smooth animations
- Dynamic form rendering based on AI-generated questions
- Anti-patterns display with warning styling
- Client-side template filling with variable replacement
- Copy-to-clipboard functionality with success feedback
- Debug console for troubleshooting parsing issues
- Mobile-responsive design
- Comprehensive error handling and validation

**🔧 Technical Implementation:**
- **Backend**: Flask API with OpenAI GPT-4o integration
- **Frontend**: React with 4-step flow (landing → loading → form → result)
- **Styling**: Professional CSS with CSS variables and animations
- **Parsing**: Robust regex-based parsing of AI output sections
- **Validation**: Form validation with required field checking
- **Ports**: Backend runs on 3000, Frontend on 3001 (configured to avoid conflicts)

**📁 File Structure:**
```
/meta-prompt-generator
├── backend/
│   ├── app.py                    # Flask API with OpenAI integration
│   ├── requirements.txt          # Python dependencies (updated for compatibility)
│   ├── .env                      # Environment variables (not committed)
│   └── prompts/
│       └── meta-prompt-system.md # Core meta-prompt template
├── frontend/
│   ├── src/
│   │   ├── App.js               # Main React component with full flow
│   │   ├── App.css              # Professional styling system
│   │   ├── api.js               # API client with error handling
│   │   └── index.js
│   └── package.json             # React config with port settings
├── .gitignore                   # Comprehensive ignore patterns
├── README.md                    # This documentation
└── CLAUDE.md                    # AI assistant guidance
```

---

## Troubleshooting

### "API Key Invalid"
- Check `.env` file exists
- Verify key starts with `sk-`
- Ensure no extra quotes or spaces
- Restart Flask server after changes

### "Parsing Failed"
- Log the raw API response
- Check if AI followed the output format
- Make regex more flexible if needed
- Try GPT-4 instead of GPT-3.5-turbo

### "CORS Error"
- Add frontend URL to CORS origins in `app.py`
- Restart Flask server
- Clear browser cache

### "Variables Not Replaced"
- Check that variable names in template match form field IDs
- Log `formValues` object to verify data
- Ensure case sensitivity matches

---

## Contributing

### Code Style

- **Python**: Follow PEP 8
- **JavaScript**: ES6+, functional components
- **Comments**: Explain *why*, not *what*

### Pull Request Process

1. Fork the repo
2. Create a feature branch
3. Test locally
4. Submit PR with description of changes
5. Wait for review

---

## Future Enhancements

### Phase 2
- [ ] User feedback mechanism (rate generated prompts)
- [ ] Prompt history/favorites
- [ ] Analytics on which domains work best
- [ ] A/B testing of meta-prompts

### Phase 3
- [ ] CrewAI multi-agent generation
- [ ] Community prompt library
- [ ] Prompt sharing/remixing
- [ ] User accounts

### Phase 4
- [ ] Self-improving system (learns from usage)
- [ ] Domain-specific fine-tuning
- [ ] Multi-language support

---

## Cost Estimates

- **Development**: Free (Render free tier)
- **OpenAI API**: ~$0.03-0.05 per prompt generation
- **Scaling**: Upgrade Render plans as needed

At 100 prompts/day: ~$3-5/day in API costs

---

## License

[Add your license here]

---

## Credits

Built by [Your Name]

Inspired by:
- The wedding vows generator at marriedbyjosh.com
- The concept of "anti-brainstorming" 
- Research on probability-based prompt diversification

---

## Questions?

- **Issues**: [GitHub Issues](https://github.com/yourusername/meta-prompt-generator/issues)
- **Email**: your-email@example.com
- **Docs**: See `CLAUDE.md` for AI assistant guidance

---

## Acknowledgments

Special thanks to:
- OpenAI for GPT-4 API
- Render for deployment platform
- The prompt engineering community

---

**Status**: Active development / UX enhancements complete  
**Last Updated**: 2025-01-06  
**Version**: 1.2

---

## Recent Updates

### v1.2 - UX Enhancements (January 2025)
- **Example Gallery**: Added 5 curated example queries on landing page for user education
- **Better Error Messages**: Improved error handling with actionable suggestions
- **Post-Generation Feedback**: Added thumbs up/down collection system
- **Try This Prompt**: Added button to generate example outputs from filled prompts
- **Improved Text Readability**: Fixed contrast issues in example output display
- **Feedback & Try-Prompt Endpoints**: Added backend endpoints for user feedback and example generation

### v1.1 - Intent-Based Meta-Prompt System (January 2025)

### Intent-Based Meta-Prompt System
- **Intent Classification**: AI now classifies user needs into 5 intent types (Creation, Understanding, Problem-Solving, Decision-Making, Guidance)
- **Intent-Specific Templates**: Template structure adapts based on user's intent with appropriate approaches
- **Decision Tree**: Added intent classification indicators to help AI correctly identify user needs
- **Flexible Architecture**: Works for both creative tasks (writing vows) and cognitive tasks (learning math)

### Enhanced Features
- **Use Sample Button**: Quick-fill sample text for testing form fields (uses AI-generated placeholders)
- **Auto-Population**: Special handling for `{{userIntent}}` variable to ensure templates always work
- **Comprehensive Test Suite**: Automated testing covering all intent types (not committed to git)
- **Better Variable Coverage**: Improved validation to ensure all form variables appear in templates
- **Example Gallery**: 5 curated example queries on landing page to teach users good prompt writing
- **Better Error Messages**: Actionable error messages with specific suggestions for each error type
- **Post-Generation Feedback**: Thumbs up/down collection to improve the system
- **Try This Prompt**: Button to generate example outputs directly in the app

### Technical Improvements
- **Port Configuration**: Backend on port 3000, Frontend on port 3001 to avoid conflicts
- **Enhanced Error Handling**: Better user-friendly error messages and retry logic
- **Debug Console**: Toggle debug view to inspect AI output and parsed schema
- **Feedback Endpoint**: `/api/feedback` to collect user feedback on prompt quality
- **Try-Prompt Endpoint**: `/api/try-prompt` to generate example outputs from filled prompts