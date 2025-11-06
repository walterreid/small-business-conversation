# Small Business Marketing Plan Generator

Generate personalized marketing plans for your small business through a simple, conversational chat interface. Select your business category, answer a few questions, and get an actionable marketing plan tailored to your needs and budget.

---

## What It Does

**The Problem**: Most small businesses struggle with marketing because they don't know where to start, what strategies work for their industry, or how to allocate their limited budget.

**The Solution**: This tool guides you through a conversational flow to understand your business, then generates a comprehensive marketing plan that includes:
- Executive Summary
- Target Audience Analysis
- Recommended Marketing Channels (budget-aware)
- 90-Day Action Plan
- Success Metrics

**Example Flow**:
1. You select: "Restaurant"
2. Chat asks: Questions about your business, target audience, budget, challenges, goals
3. You answer: One question at a time in a friendly conversation
4. You get: A detailed, actionable marketing plan ready to implement

---

## Tech Stack

- **Backend**: Python/Flask
- **Frontend**: React with Chatscope UI Kit
- **AI**: OpenAI GPT-4o
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
git clone https://github.com/yourusername/small-business-marketing-tool.git
cd small-business-marketing-tool

# 2. Backend setup
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Create .env file
echo "OPENAI_API_KEY=sk-your-key-here" > .env
echo "FLASK_ENV=development" >> .env
echo "PORT=5000" >> .env

# 3. Frontend setup (in new terminal)
cd frontend
npm install
```

### Running Locally

```bash
# Terminal 1 - Backend (http://localhost:5000)
cd backend
source venv/bin/activate
python3 app.py

# Terminal 2 - Frontend (http://localhost:3001)
cd frontend
npm start
```

Visit `http://localhost:3001` to use the app.

---

## Deployment

See **[docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)** for complete deployment guide.

Quick reference:

### Render (Recommended)

1. Push your code to GitHub
2. Connect your repo to Render
3. Render will detect `render.yaml` and create both services
4. Add environment variables in Render dashboard:
   - Backend: `OPENAI_API_KEY`, `FLASK_ENV=production`, `PORT=10000`
   - Frontend: `REACT_APP_API_URL` (your backend URL)

The app will auto-deploy on every push to main.

---

## Project Structure

```
/small-business-marketing-tool
├── backend/
│   ├── app.py                    # Flask API with chat endpoints
│   ├── chat_flows.py             # Question flows for each category
│   ├── requirements.txt          # Python dependencies
│   ├── .env                      # Environment variables (not committed)
│   └── prompts/
│       └── meta-prompt-system.md # (Legacy - kept for reference)
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── App.js               # Main React component (3-step flow)
│   │   ├── App.css              # Global styles
│   │   ├── components/          # React components
│   │   │   ├── CategorySelector.js
│   │   │   ├── ChatInterface.js
│   │   │   └── MarketingPlanView.js
│   │   ├── api/                 # API clients
│   │   │   └── chatApi.js
│   │   ├── styles/              # Component styles
│   │   │   ├── CategorySelector.css
│   │   │   ├── ChatApp.css
│   │   │   └── MarketingPlanView.css
│   │   └── index.js
│   └── package.json
├── docs/                         # Documentation
│   ├── README.md                # Documentation index
│   ├── DEPLOYMENT.md            # Deployment guide
│   ├── TROUBLESHOOTING.md       # Troubleshooting guide
│   ├── ARCHITECTURE_PLAN.md     # Architecture planning
│   └── PHASE_*_COMPLETE.md      # Phase summaries
├── test/                         # Testing materials (not committed)
│   ├── README.md                # Testing overview
│   ├── test_scenarios.json      # Test scenarios
│   └── manual_test_checklist.md # Testing checklist
├── render.yaml                   # Render deployment config
├── .gitignore
├── README.md                     # This file
└── CLAUDE.md                     # AI assistant guidance
```

---

## How It Works

### Architecture

```
User Selects Category
    ↓
Chat Interface (one question at a time)
    ↓
Flask Backend (/api/chat/start, /api/chat/message)
    ↓
Question Flow System (chat_flows.py)
    ↓
OpenAI Chat API (conversational, maintains context)
    ↓
All Questions Answered
    ↓
Marketing Plan Generation (/api/chat/generate-plan)
    ↓
Structured Marketing Plan
```

### The Chat Flow

**Step 1: Category Selection**
- User selects business category (Restaurant, Retail Store, Professional Services, E-commerce, Local Services)
- Each category has tailored questions

**Step 2: Conversational Questions**
- Chat interface asks questions one at a time
- Questions are structured and category-specific
- User answers naturally in conversation
- System tracks answers and determines next question

**Step 3: Marketing Plan Generation**
- When all required questions answered, user can generate plan
- System uses all collected answers to build comprehensive prompt
- OpenAI generates structured marketing plan
- Plan includes actionable recommendations, timelines, and metrics

### Question Flow System

Each business category has 9 structured questions covering:
- Business basics (name, type, location)
- Target audience
- Monthly marketing budget
- Current marketing efforts
- Biggest challenges
- Unique value proposition
- Marketing goals

Questions are stored in `backend/chat_flows.py` and can be easily modified.

---

## Key Features

### 1. Conversational Interface
One question at a time feels less overwhelming than long forms. Uses Chatscope UI Kit for professional chat experience.

### 2. Category-Specific Intelligence
Each business type gets tailored questions and recommendations. A restaurant needs different strategies than a local plumber.

### 3. Budget-Aware Recommendations
Marketing plans adapt to budget constraints. Under $500/month gets different recommendations than $5000+/month.

### 4. Actionable Plans
Plans include specific tactics, timelines, and next steps. Not generic advice but concrete actions you can take.

### 5. Structured Output
Every plan includes:
- Executive Summary
- Target Audience Analysis
- Recommended Marketing Channels
- 90-Day Action Plan
- Success Metrics

---

## API Endpoints

### `POST /api/chat/start`

Start a new chat session for a business category.

**Request:**
```json
{
  "category": "restaurant"
}
```

**Response:**
```json
{
  "success": true,
  "session_id": "uuid",
  "first_question": "Hi! I'm here to help...",
  "conversation": [...]
}
```

### `POST /api/chat/message`

Send a message in an ongoing chat session.

**Request:**
```json
{
  "session_id": "uuid",
  "user_message": "Joe's Pizza"
}
```

**Response:**
```json
{
  "success": true,
  "ai_response": "Great! What type of cuisine...",
  "is_complete": false,
  "conversation": [...],
  "questions_answered": 2
}
```

### `POST /api/chat/generate-plan`

Generate final marketing plan from completed session.

**Request:**
```json
{
  "session_id": "uuid"
}
```

**Response:**
```json
{
  "success": true,
  "marketing_plan": "EXECUTIVE SUMMARY\n...",
  "metadata": {
    "model": "gpt-4o",
    "tokens_used": 2847,
    "category": "restaurant"
  }
}
```

### `GET /api/chat/session/<session_id>`

Get conversation history for a session.

**Response:**
```json
{
  "success": true,
  "session": {
    "session_id": "uuid",
    "category": "restaurant",
    "conversation": [...],
    "answers": {...},
    "created_at": "ISO timestamp"
  }
}
```

### `GET /health`

Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "service": "small-business-marketing-tool"
}
```

---

## Environment Variables

### Backend (`backend/.env`)

```bash
OPENAI_API_KEY=sk-...          # Your OpenAI API key (required)
FLASK_ENV=development          # development or production
PORT=5001                      # Server port (5001 to avoid macOS AirPlay conflict)
```

### Frontend (`.env` or Render dashboard)

```bash
REACT_APP_API_URL=http://localhost:5001    # Backend URL (optional - proxy handles this in dev)
```

---

## Development Workflow

1. **Make changes** to backend or frontend
2. **Test locally** (both servers running)
3. **Commit and push** to GitHub
4. **Render auto-deploys** to production

### Updating Question Flows

To modify questions for a category:

1. Edit `backend/chat_flows.py` QUESTION_FLOWS
2. Test locally by going through the flow
3. Commit and push
4. Render will redeploy with updated questions

---

## Testing

### Manual Testing Checklist

- [ ] Select a business category
- [ ] Answer all questions in chat
- [ ] Verify questions are relevant to category
- [ ] Check that completion is detected
- [ ] Generate marketing plan
- [ ] Verify plan includes all required sections
- [ ] Test copy to clipboard
- [ ] Test download functionality
- [ ] Test start over flow

### Test Categories

All 5 categories should be tested:
- Restaurant
- Retail Store
- Professional Services
- E-commerce
- Local Services

---

## Current Implementation Status

**✅ Completed Features:**
- Complete chat-based marketing plan generation system
- 5 business categories with tailored questions
- Professional UI with Chatscope UI Kit
- Smooth animations and transitions
- Session management
- Marketing plan generation with structured output
- Copy/download functionality
- Mobile-responsive design
- Comprehensive error handling

**🔧 Technical Implementation:**
- **Backend**: Flask API with OpenAI GPT-4o integration, chat endpoints, session management
- **Frontend**: React with 3-step flow (category → chat → plan)
- **Styling**: Professional CSS with animations, gradient themes
- **Chat UI**: Chatscope UI Kit for professional chat experience
- **Ports**: Backend on port 5001, Frontend on port 3001

---

## Troubleshooting

See **[docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)** for detailed troubleshooting guide.

Quick reference:

### "API Key Invalid"
- Check `.env` file exists in `/backend`
- Verify key starts with `sk-`
- Ensure no extra quotes or spaces
- Restart Flask server after changes

### "Session Not Found"
- Session may have expired (in-memory storage)
- Start a new session
- Check backend logs for session creation

### "CORS Error"
- Add frontend URL to CORS origins in `app.py`
- Restart Flask server
- Clear browser cache

### "All Questions Not Answered"
- Ensure you've answered all required questions
- Check that answers are being stored correctly
- Review backend logs for answer tracking

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

## Completed Features

✅ **Budget-Aware Marketing Plans** - Plans adapt to user's budget tier (low to high)  
✅ **Category-Specific Intelligence** - Tailored questions and recommendations for each business type  
✅ **Industry Insights Integration** - Marketing best practices and channel recommendations  
✅ **Comprehensive Testing** - Test materials, scenarios, and checklists  
✅ **Error Handling** - Robust validation and user-friendly error messages  
✅ **Professional UI** - Smooth animations, responsive design, Chatscope UI Kit

## Future Enhancements
- [ ] Database for session persistence
- [ ] User accounts and plan history
- [ ] Analytics dashboard
- [ ] Export plans as PDF
- [ ] Multi-language support

---

## Cost Estimates

- **Development**: Free (Render free tier)
- **OpenAI API**: ~$0.05-0.10 per marketing plan generation
- **Scaling**: Upgrade Render plans as needed

At 100 plans/day: ~$5-10/day in API costs

---

## License

[Add your license here]

---

## Credits

Built by [Your Name]

Inspired by:
- Bridesmaid for Hire's conversational flow
- Small business marketing challenges
- Need for actionable, budget-aware marketing plans

---

## Questions?

- **Issues**: [GitHub Issues](https://github.com/yourusername/small-business-marketing-tool/issues)
- **Email**: your-email@example.com
- **Docs**: See `CLAUDE.md` for AI assistant guidance

---

**Status**: Production ready / Chat-based flow complete  
**Last Updated**: 2025-11-06  
**Version**: 2.0

---

## Project History

This project was migrated from a meta-prompt generator to a chat-based marketing tool. Migration documentation is available in the `/docs` folder:

- See `docs/README.md` for migration overview
- See `docs/ARCHITECTURE_PLAN.md` for complete architecture details
- See `docs/PHASE_*_COMPLETE.md` files for phase-by-phase implementation

The migration was completed in 10 phases, transforming the system from a prompt template generator into a direct marketing plan creation tool.
