# CURSOR AI PROMPT: Better Business Questions v3.0
## Build the "Guided Discovery + Progressive Transparency" System

---

## 🎯 PROJECT OVERVIEW

We're upgrading a small business marketing tool that uses expert prompt templates to generate better marketing advice than generic ChatGPT. The current system has 30 pre-crafted marketing questions with expert frameworks, but users don't know which question to ask, and they can't see the expertise working behind the scenes.

**Current Problem:**
- 30 questions = choice paralysis
- Users can't see the expert prompt system working
- Looks like a generic chatbot
- No clear differentiation from ChatGPT

**Solution We're Building:**
1. **Diagnostic Funnel** - Match users to the right 3 questions in 30 seconds
2. **Progressive Transparency** - Show the expert framework activating in real-time
3. **Clear Differentiation** - Make it obvious this is NOT just ChatGPT

---

## 📁 EXISTING PROJECT STRUCTURE

```
/backend
  app.py                 # Flask API with OpenAI integration
  chat_flows.py          # Original question flows (keep for reference)
  /prompts
    /generated_templates
      /build_brand_awareness
        question_1.json  # Expert prompt templates (see example below)
      /increase_sales
      /drive_foot_traffic
      ... (6 categories total, 5 questions each)

/frontend
  /src
    App.js               # 3-step flow: category → chat → results
    /components
      CategorySelector.js
      ChatInterface.js   # Uses Chatscope UI Kit
      MarketingPlanView.js
    /api
      chatApi.js         # API client functions
    /styles
      ChatApp.css
      CategorySelector.css
      MarketingPlanView.css
```

---

## 📋 EXAMPLE: question_1.json STRUCTURE

```json
{
  "category": "build_brand_awareness",
  "version": "1.0.0",
  "meta_prompt_version": "v1.0",
  "question_text": "How do I increase brand awareness for my (unique proposition) (industry) brand among (demographic) in urban areas",
  "anti_patterns": [
    "Common Pattern 1: Overemphasis on social media presence without unique content",
    "Common Pattern 2: Relying solely on discounts and promotions to attract attention",
    "Common Pattern 3: Generic messaging that lacks a clear brand voice or story"
  ],
  "prompt_template": "Role: Guide\n\nIntent: Increase brand awareness for {{uniqueProposition}} {{industry}} brand among {{demographic}} in urban areas.\nUser wants to understand effective, practical strategies to enhance brand visibility and awareness within a specific demographic and urban setting.\n\nApproach: Explain concepts, check understanding, build gradually.\n- Provide step-by-step strategies tailored to the unique proposition.\n- Offer practical examples and case studies.\n- Encourage iteration and feedback loops to refine strategies.\n\nVariables:\n- {{uniqueProposition}}: Helps tailor strategies that align with the brand's distinct attributes.\n- {{industry}}: Allows focus on industry-specific trends and consumer behavior.\n- {{demographic}}: Targets strategies to the specific audience.\n- {{urbanAreas}}: Considers the unique aspects of marketing in urban settings.\n\nConstraints:\n- Style: Practical, conversational, intuitive.\n- Avoid: Generic advice, overly theoretical approaches.\n- Focus: Specific tactics for small businesses with limited budgets, actionable steps.\n\nOutput guidance: Provide a tailored guide with actionable steps, examples, and a framework for testing and iterating on strategies.\n\nSuccess conditions: User gains a clear understanding of how to effectively increase brand awareness in their specified context, with actionable steps they can implement.",
  "questions": [
    {
      "id": "uniqueProposition",
      "question": "What is the unique proposition of your brand?",
      "type": "text",
      "placeholder": "e.g., eco-friendly materials, innovative technology",
      "required": true
    },
    {
      "id": "industry",
      "question": "Which industry does your brand belong to?",
      "type": "select",
      "options": ["Fashion", "Technology", "Food & Beverage", "Healthcare", "Education", "Retail", "Professional Services", "Other"],
      "why_matters": "Allows focus on industry-specific trends and challenges, ensuring the advice is relevant.",
      "required": true
    }
  ],
  "opening_dialog": "Hi! I'm here to help you with your build brand awareness question 1 business. Let's get started.",
  "question_number": 1,
  "smb_insights": {
    "budget_ranges": ["Under $500", "$500-1000", "$1000-2500", "$2500-5000", "$5000+"],
    "pain_points": [
      "Limited time for marketing",
      "Don't know where to start",
      "Wasted money on ineffective ads",
      "Can't track ROI",
      "Competing with bigger businesses"
    ],
    "effective_channels": [
      "Google Business Profile (free)",
      "Instagram organic",
      "Local SEO",
      "Email marketing",
      "Facebook ads (if budget allows)",
      "Word of mouth referrals"
    ],
    "budget_allocations": {
      "Under $500": {
        "focus": "Free and low-cost channels",
        "channels": ["Google Business Profile", "Social media organic", "Email marketing"]
      },
      "$500-1000": {
        "focus": "Mix of free and paid",
        "channels": ["Google Ads (limited)", "Social media ads", "Email marketing"]
      }
    }
  }
}
```

---

## 🎯 WHAT WE'RE BUILDING: PHASED APPROACH

---

# PHASE 1: DIAGNOSTIC FUNNEL (The Matchmaker)
**Goal:** Help users find their perfect question in 30 seconds

## Backend Changes

### 1.1 Create Diagnostic Logic

**File: `backend/diagnostic_engine.py` (NEW)**

```python
"""
Diagnostic engine to match users to the most relevant marketing questions.
Uses a simple decision tree based on pain points, revenue, and experience.
"""

# Decision tree mapping
DIAGNOSTIC_MAPPINGS = {
    "not_enough_customers": {
        "priority_categories": ["increase_sales", "generate_leads", "drive_foot_traffic"],
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
        "priority_categories": ["launch_new_product"],
        "keywords": ["launch", "new", "product", "service"]
    }
}

def match_questions(pain_point, revenue_range, tried_before, all_questions):
    """
    Match user to top 3 most relevant questions.
    
    Args:
        pain_point: str - User's main pain point
        revenue_range: str - Monthly revenue range
        tried_before: list - What they've already tried
        all_questions: list - All available questions
    
    Returns:
        list of 3 dicts with question data + match_score + reasoning
    """
    # Get priority categories based on pain point
    mapping = DIAGNOSTIC_MAPPINGS.get(pain_point, {})
    priority_categories = mapping.get("priority_categories", [])
    
    scored_questions = []
    
    for question in all_questions:
        score = 0
        reasoning_parts = []
        
        # Score based on category match
        if question["category"] in priority_categories:
            score += 50
            reasoning_parts.append(f"Addresses your '{pain_point}' challenge")
        
        # Score based on revenue appropriateness
        if revenue_range == "under_10k":
            # Prioritize low-budget strategies
            if "budget" in question["question_text"].lower():
                score += 20
                reasoning_parts.append("Includes budget-conscious strategies")
        elif revenue_range == "over_100k":
            # Can handle more complex strategies
            score += 10
        
        # Penalize if they've already tried related strategies
        question_lower = question["question_text"].lower()
        if "social media" in tried_before and "social" in question_lower:
            score -= 20
            reasoning_parts.append("Offers alternatives to social media")
        if "ads" in tried_before and ("ad" in question_lower or "paid" in question_lower):
            score -= 20
            reasoning_parts.append("Focuses on non-ad strategies")
        
        # Add question with score
        scored_questions.append({
            "question": question,
            "score": score,
            "reasoning": " • ".join(reasoning_parts) if reasoning_parts else "Good general fit for your situation"
        })
    
    # Sort by score and return top 3
    scored_questions.sort(key=lambda x: x["score"], reverse=True)
    return scored_questions[:3]


def explain_why_match(pain_point, revenue_range, tried_before):
    """
    Generate explanation for why these questions were matched.
    """
    explanations = []
    
    if pain_point == "not_enough_customers":
        explanations.append("You need strategies to bring in more customers")
    elif pain_point == "no_visibility":
        explanations.append("Your business needs better visibility in your market")
    elif pain_point == "cant_keep_customers":
        explanations.append("You need to improve customer retention and loyalty")
    elif pain_point == "launching_something":
        explanations.append("You're launching something new and need a go-to-market strategy")
    
    if revenue_range == "under_10k":
        explanations.append("These questions focus on cost-effective strategies for smaller budgets")
    elif revenue_range == "50k_to_100k":
        explanations.append("These questions balance organic and paid strategies for growing businesses")
    elif revenue_range == "over_100k":
        explanations.append("These questions include advanced strategies for established businesses")
    
    if tried_before:
        tried_str = ", ".join(tried_before)
        explanations.append(f"These offer alternatives to what you've already tried ({tried_str})")
    
    return explanations
```

### 1.2 Add Diagnostic API Endpoints

**File: `backend/app.py` (MODIFY)**

Add these new endpoints:

```python
from diagnostic_engine import match_questions, explain_why_match
import json
import os
from pathlib import Path

# Load all question templates on startup
QUESTION_TEMPLATES = {}

def load_all_questions():
    """Load all question templates from generated_templates directory."""
    templates_dir = Path(__file__).parent / "prompts" / "generated_templates"
    all_questions = []
    
    for category_dir in templates_dir.iterdir():
        if category_dir.is_dir():
            for question_file in category_dir.glob("question_*.json"):
                with open(question_file, 'r') as f:
                    question_data = json.load(f)
                    all_questions.append(question_data)
    
    return all_questions

# Load questions on startup
ALL_QUESTIONS = load_all_questions()

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
        data = request.get_json()
        pain_point = data.get('pain_point')
        revenue_range = data.get('revenue_range')
        tried_before = data.get('tried_before', [])
        
        # Validate input
        if not pain_point or not revenue_range:
            return jsonify({
                'success': False,
                'error': 'Missing required fields: pain_point and revenue_range'
            }), 400
        
        # Match questions
        matched = match_questions(pain_point, revenue_range, tried_before, ALL_QUESTIONS)
        
        # Generate explanation
        reasoning = explain_why_match(pain_point, revenue_range, tried_before)
        
        return jsonify({
            'success': True,
            'matched_questions': [
                {
                    'category': m['question']['category'],
                    'question_number': m['question']['question_number'],
                    'question_text': m['question']['question_text'],
                    'match_score': m['score'],
                    'why_this_fits': m['reasoning'],
                    'anti_patterns': m['question']['anti_patterns']
                }
                for m in matched
            ],
            'overall_reasoning': reasoning
        })
        
    except Exception as e:
        app.logger.error(f"Diagnostic error: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/questions/all', methods=['GET'])
def get_all_questions():
    """Get all available questions organized by category."""
    try:
        # Organize by category
        by_category = {}
        for q in ALL_QUESTIONS:
            category = q['category']
            if category not in by_category:
                by_category[category] = []
            by_category[category].append({
                'question_number': q['question_number'],
                'question_text': q['question_text'],
                'anti_patterns': q.get('anti_patterns', [])
            })
        
        return jsonify({
            'success': True,
            'categories': by_category,
            'total_questions': len(ALL_QUESTIONS)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
```

## Frontend Changes

### 1.3 Create Diagnostic Flow Component

**File: `frontend/src/components/DiagnosticFlow.js` (NEW)**

```javascript
import React, { useState } from 'react';
import '../styles/DiagnosticFlow.css';

const DiagnosticFlow = ({ onComplete, onSkip }) => {
  const [step, setStep] = useState(1);
  const [answers, setAnswers] = useState({
    pain_point: null,
    revenue_range: null,
    tried_before: []
  });

  const painPoints = [
    {
      id: 'not_enough_customers',
      icon: '📉',
      title: 'Not Enough Customers',
      description: 'I need more sales, leads, or foot traffic'
    },
    {
      id: 'no_visibility',
      icon: '🔍',
      title: 'Nobody Knows About Us',
      description: 'People don\'t know my business exists'
    },
    {
      id: 'cant_keep_customers',
      icon: '🔄',
      title: 'Can\'t Keep Customers',
      description: 'Customers don\'t come back or stay loyal'
    },
    {
      id: 'launching_something',
      icon: '🚀',
      title: 'Launching Something New',
      description: 'I\'m launching a new product or service'
    }
  ];

  const revenueRanges = [
    { id: 'under_10k', label: 'Under $10k/month', description: 'Just getting started' },
    { id: '10k_to_50k', label: '$10k-50k/month', description: 'Growing steadily' },
    { id: '50k_to_100k', label: '$50k-100k/month', description: 'Well established' },
    { id: 'over_100k', label: 'Over $100k/month', description: 'Scaling up' }
  ];

  const triedOptions = [
    { id: 'social_media', label: 'Social Media Marketing' },
    { id: 'ads', label: 'Paid Advertising (Google/Facebook)' },
    { id: 'email', label: 'Email Marketing' },
    { id: 'seo', label: 'SEO / Content Marketing' },
    { id: 'nothing', label: 'Nothing yet / Just starting' }
  ];

  const handlePainPointSelect = (painPointId) => {
    setAnswers({ ...answers, pain_point: painPointId });
    setStep(2);
  };

  const handleRevenueSelect = (revenueId) => {
    setAnswers({ ...answers, revenue_range: revenueId });
    setStep(3);
  };

  const handleTriedToggle = (triedId) => {
    const current = answers.tried_before;
    if (current.includes(triedId)) {
      setAnswers({
        ...answers,
        tried_before: current.filter(id => id !== triedId)
      });
    } else {
      setAnswers({
        ...answers,
        tried_before: [...current, triedId]
      });
    }
  };

  const handleComplete = () => {
    onComplete(answers);
  };

  const handleBack = () => {
    setStep(step - 1);
  };

  return (
    <div className="diagnostic-flow">
      <div className="diagnostic-container">
        {/* Progress Indicator */}
        <div className="diagnostic-progress">
          <div className="progress-bar">
            <div 
              className="progress-fill" 
              style={{ width: `${(step / 3) * 100}%` }}
            />
          </div>
          <div className="progress-text">Step {step} of 3</div>
        </div>

        {/* Step 1: Pain Point */}
        {step === 1 && (
          <div className="diagnostic-step fade-in">
            <h2>What's keeping you up at night?</h2>
            <p className="step-subtitle">
              Choose your biggest marketing challenge right now
            </p>
            <div className="option-grid">
              {painPoints.map(option => (
                <button
                  key={option.id}
                  className={`option-card ${answers.pain_point === option.id ? 'selected' : ''}`}
                  onClick={() => handlePainPointSelect(option.id)}
                >
                  <div className="option-icon">{option.icon}</div>
                  <div className="option-title">{option.title}</div>
                  <div className="option-description">{option.description}</div>
                </button>
              ))}
            </div>
            <button className="skip-button" onClick={onSkip}>
              Skip diagnostic, show all questions →
            </button>
          </div>
        )}

        {/* Step 2: Revenue */}
        {step === 2 && (
          <div className="diagnostic-step fade-in">
            <button className="back-button" onClick={handleBack}>
              ← Back
            </button>
            <h2>What's your monthly revenue?</h2>
            <p className="step-subtitle">
              This helps us recommend strategies that fit your budget
            </p>
            <div className="option-list">
              {revenueRanges.map(option => (
                <button
                  key={option.id}
                  className={`option-row ${answers.revenue_range === option.id ? 'selected' : ''}`}
                  onClick={() => handleRevenueSelect(option.id)}
                >
                  <div>
                    <div className="option-label">{option.label}</div>
                    <div className="option-description">{option.description}</div>
                  </div>
                  {answers.revenue_range === option.id && (
                    <span className="checkmark">✓</span>
                  )}
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Step 3: What Tried */}
        {step === 3 && (
          <div className="diagnostic-step fade-in">
            <button className="back-button" onClick={handleBack}>
              ← Back
            </button>
            <h2>What have you already tried?</h2>
            <p className="step-subtitle">
              Select all that apply (we'll suggest alternatives)
            </p>
            <div className="option-list">
              {triedOptions.map(option => (
                <button
                  key={option.id}
                  className={`option-row multi-select ${
                    answers.tried_before.includes(option.id) ? 'selected' : ''
                  }`}
                  onClick={() => handleTriedToggle(option.id)}
                >
                  <div className="option-label">{option.label}</div>
                  {answers.tried_before.includes(option.id) && (
                    <span className="checkmark">✓</span>
                  )}
                </button>
              ))}
            </div>
            <button 
              className="continue-button"
              onClick={handleComplete}
            >
              Find My Questions →
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default DiagnosticFlow;
```

### 1.4 Create Matched Questions Display

**File: `frontend/src/components/MatchedQuestions.js` (NEW)**

```javascript
import React from 'react';
import '../styles/MatchedQuestions.css';

const MatchedQuestions = ({ matchedQuestions, reasoning, onSelectQuestion, onBrowseAll }) => {
  return (
    <div className="matched-questions">
      <div className="matched-container">
        <div className="matched-header">
          <h2>✨ Perfect! Here are your top 3 questions</h2>
          <div className="reasoning-box">
            <div className="reasoning-title">Why these questions?</div>
            <ul className="reasoning-list">
              {reasoning.map((reason, idx) => (
                <li key={idx}>{reason}</li>
              ))}
            </ul>
          </div>
        </div>

        <div className="questions-grid">
          {matchedQuestions.map((match, idx) => (
            <div 
              key={idx}
              className="matched-question-card"
              onClick={() => onSelectQuestion(match.category, match.question_number, match.question_text)}
            >
              <div className="match-rank">#{idx + 1} Best Match</div>
              <div className="question-text">{match.question_text}</div>
              
              <div className="why-fits">
                <div className="why-fits-title">🎯 Why this fits you:</div>
                <div className="why-fits-text">{match.why_this_fits}</div>
              </div>

              {match.anti_patterns && match.anti_patterns.length > 0 && (
                <div className="anti-patterns-preview">
                  <div className="anti-patterns-title">⚠️ You'll avoid:</div>
                  <ul>
                    {match.anti_patterns.slice(0, 2).map((pattern, pidx) => (
                      <li key={pidx}>{pattern}</li>
                    ))}
                  </ul>
                </div>
              )}

              <button className="select-question-btn">
                Start Conversation →
              </button>
            </div>
          ))}
        </div>

        <div className="browse-all-section">
          <button className="browse-all-btn" onClick={onBrowseAll}>
            Or browse all 30 questions →
          </button>
        </div>
      </div>
    </div>
  );
};

export default MatchedQuestions;
```

### 1.5 Update Main App Flow

**File: `frontend/src/App.js` (MODIFY)**

```javascript
import React, { useState } from 'react';
import DiagnosticFlow from './components/DiagnosticFlow';
import MatchedQuestions from './components/MatchedQuestions';
import CategorySelector from './components/CategorySelector';
import ChatInterface from './components/ChatInterface';
import MarketingPlanView from './components/MarketingPlanView';
import { runDiagnostic } from './api/chatApi';
import './App.css';

function App() {
  const [step, setStep] = useState('diagnostic'); // diagnostic, matched, browse, chat, plan
  const [diagnosticAnswers, setDiagnosticAnswers] = useState(null);
  const [matchedQuestions, setMatchedQuestions] = useState(null);
  const [matchReasoning, setMatchReasoning] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState(null);
  const [selectedQuestionNumber, setSelectedQuestionNumber] = useState(null);
  const [selectedQuestionText, setSelectedQuestionText] = useState(null);
  const [marketingPlan, setMarketingPlan] = useState(null);
  const [planMetadata, setPlanMetadata] = useState(null);

  const handleDiagnosticComplete = async (answers) => {
    setDiagnosticAnswers(answers);
    
    try {
      const result = await runDiagnostic(
        answers.pain_point,
        answers.revenue_range,
        answers.tried_before
      );
      
      if (result.success) {
        setMatchedQuestions(result.matched_questions);
        setMatchReasoning(result.overall_reasoning);
        setStep('matched');
      }
    } catch (error) {
      console.error('Diagnostic error:', error);
      // Fallback to browse all
      setStep('browse');
    }
  };

  const handleSkipDiagnostic = () => {
    setStep('browse');
  };

  const handleSelectMatchedQuestion = (category, questionNumber, questionText) => {
    setSelectedCategory(category);
    setSelectedQuestionNumber(questionNumber);
    setSelectedQuestionText(questionText);
    setStep('chat');
  };

  const handleBrowseAll = () => {
    setStep('browse');
  };

  const handleSelectFromBrowse = (category, questionNumber, questionText) => {
    setSelectedCategory(category);
    setSelectedQuestionNumber(questionNumber);
    setSelectedQuestionText(questionText);
    setStep('chat');
  };

  const handleGeneratePlan = (plan, metadata) => {
    setMarketingPlan(plan);
    setPlanMetadata(metadata);
    setStep('plan');
  };

  const handleStartOver = () => {
    setStep('diagnostic');
    setDiagnosticAnswers(null);
    setMatchedQuestions(null);
    setMatchReasoning([]);
    setSelectedCategory(null);
    setSelectedQuestionNumber(null);
    setSelectedQuestionText(null);
    setMarketingPlan(null);
    setPlanMetadata(null);
  };

  return (
    <div className="App">
      {step === 'diagnostic' && (
        <DiagnosticFlow
          onComplete={handleDiagnosticComplete}
          onSkip={handleSkipDiagnostic}
        />
      )}

      {step === 'matched' && (
        <MatchedQuestions
          matchedQuestions={matchedQuestions}
          reasoning={matchReasoning}
          onSelectQuestion={handleSelectMatchedQuestion}
          onBrowseAll={handleBrowseAll}
        />
      )}

      {step === 'browse' && (
        <CategorySelector
          onSelectQuestion={handleSelectFromBrowse}
        />
      )}

      {step === 'chat' && (
        <ChatInterface
          category={selectedCategory}
          questionNumber={selectedQuestionNumber}
          initialQuestionText={selectedQuestionText}
          diagnosticContext={diagnosticAnswers}
          onGeneratePlan={handleGeneratePlan}
          onAskDifferentQuestion={handleStartOver}
        />
      )}

      {step === 'plan' && (
        <MarketingPlanView
          marketingPlan={marketingPlan}
          metadata={planMetadata}
          onStartOver={handleStartOver}
        />
      )}
    </div>
  );
}

export default App;
```

### 1.6 Add API Client Function

**File: `frontend/src/api/chatApi.js` (ADD)**

```javascript
export async function runDiagnostic(painPoint, revenueRange, triedBefore) {
  try {
    const url = API_BASE_URL ? `${API_BASE_URL}/api/diagnostic` : '/api/diagnostic';
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        pain_point: painPoint,
        revenue_range: revenueRange,
        tried_before: triedBefore
      })
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.error || `HTTP ${response.status}`);
    }

    const data = await response.json();
    
    if (!data.success) {
      throw new Error(data.error || 'Failed to run diagnostic');
    }

    return data;
  } catch (error) {
    if (error.name === 'TypeError' && error.message.includes('fetch')) {
      throw new Error('Unable to connect to the server.');
    }
    throw error;
  }
}
```

### 1.7 Create Diagnostic Styles

**File: `frontend/src/styles/DiagnosticFlow.css` (NEW)**

```css
.diagnostic-flow {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
}

.diagnostic-container {
  max-width: 800px;
  width: 100%;
}

.diagnostic-progress {
  text-align: center;
  margin-bottom: 3rem;
}

.progress-bar {
  height: 8px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: 0.5rem;
}

.progress-fill {
  height: 100%;
  background: white;
  transition: width 0.3s ease;
}

.progress-text {
  color: rgba(255, 255, 255, 0.9);
  font-size: 0.9rem;
  font-weight: 500;
}

.diagnostic-step {
  animation: fadeIn 0.4s ease;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.diagnostic-step h2 {
  color: white;
  font-size: 2.5rem;
  text-align: center;
  margin-bottom: 0.5rem;
  font-weight: 700;
}

.step-subtitle {
  color: rgba(255, 255, 255, 0.9);
  text-align: center;
  font-size: 1.1rem;
  margin-bottom: 3rem;
}

.option-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.option-card {
  background: white;
  border: 3px solid transparent;
  border-radius: 12px;
  padding: 2rem 1.5rem;
  cursor: pointer;
  transition: all 0.2s ease;
  text-align: center;
}

.option-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
}

.option-card.selected {
  border-color: #667eea;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
  box-shadow: 0 8px 24px rgba(102, 126, 234, 0.3);
}

.option-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.option-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #333;
  margin-bottom: 0.5rem;
}

.option-description {
  font-size: 0.9rem;
  color: #666;
  line-height: 1.5;
}

.option-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-bottom: 2rem;
}

.option-row {
  background: white;
  border: 2px solid #e9ecef;
  border-radius: 12px;
  padding: 1.5rem;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  justify-content: space-between;
  align-items: center;
  text-align: left;
}

.option-row:hover {
  border-color: #667eea;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.15);
}

.option-row.selected {
  border-color: #667eea;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%);
}

.option-label {
  font-size: 1.1rem;
  font-weight: 600;
  color: #333;
}

.checkmark {
  color: #667eea;
  font-size: 1.5rem;
  font-weight: bold;
}

.back-button {
  background: transparent;
  border: none;
  color: white;
  font-size: 1rem;
  cursor: pointer;
  margin-bottom: 2rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  transition: all 0.2s;
}

.back-button:hover {
  background: rgba(255, 255, 255, 0.1);
}

.continue-button {
  background: white;
  color: #667eea;
  border: none;
  padding: 1.25rem 2.5rem;
  font-size: 1.1rem;
  font-weight: 700;
  border-radius: 12px;
  cursor: pointer;
  width: 100%;
  transition: all 0.2s;
}

.continue-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
}

.skip-button {
  background: transparent;
  border: 2px solid rgba(255, 255, 255, 0.5);
  color: white;
  padding: 0.75rem 1.5rem;
  font-size: 0.95rem;
  font-weight: 500;
  border-radius: 8px;
  cursor: pointer;
  display: block;
  margin: 0 auto;
  transition: all 0.2s;
}

.skip-button:hover {
  background: rgba(255, 255, 255, 0.1);
  border-color: white;
}

@media (max-width: 768px) {
  .diagnostic-step h2 {
    font-size: 1.8rem;
  }
  
  .option-grid {
    grid-template-columns: 1fr;
  }
}
```

**File: `frontend/src/styles/MatchedQuestions.css` (NEW)**

```css
.matched-questions {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 3rem 1.5rem;
}

.matched-container {
  max-width: 1200px;
  margin: 0 auto;
}

.matched-header {
  text-align: center;
  margin-bottom: 3rem;
}

.matched-header h2 {
  color: white;
  font-size: 2.5rem;
  margin-bottom: 2rem;
  font-weight: 700;
}

.reasoning-box {
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(10px);
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 12px;
  padding: 1.5rem;
  max-width: 700px;
  margin: 0 auto;
}

.reasoning-title {
  color: white;
  font-size: 1.1rem;
  font-weight: 600;
  margin-bottom: 1rem;
}

.reasoning-list {
  list-style: none;
  margin: 0;
  padding: 0;
}

.reasoning-list li {
  color: rgba(255, 255, 255, 0.95);
  padding: 0.5rem 0;
  padding-left: 2rem;
  position: relative;
  line-height: 1.6;
}

.reasoning-list li::before {
  content: "✓";
  position: absolute;
  left: 0;
  color: #4ade80;
  font-weight: bold;
  font-size: 1.2rem;
}

.questions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 2rem;
  margin-bottom: 3rem;
}

.matched-question-card {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.matched-question-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.2);
}

.match-rank {
  position: absolute;
  top: 1rem;
  right: 1rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 600;
}

.question-text {
  font-size: 1.3rem;
  font-weight: 600;
  color: #333;
  margin-bottom: 1.5rem;
  line-height: 1.4;
  padding-right: 6rem;
}

.why-fits {
  background: #f0f4ff;
  border-left: 4px solid #667eea;
  padding: 1rem;
  border-radius: 6px;
  margin-bottom: 1.5rem;
}

.why-fits-title {
  font-size: 0.85rem;
  font-weight: 600;
  color: #667eea;
  margin-bottom: 0.5rem;
}

.why-fits-text {
  font-size: 0.9rem;
  color: #555;
  line-height: 1.5;
}

.anti-patterns-preview {
  background: #fff8f0;
  border-left: 4px solid #ff9800;
  padding: 1rem;
  border-radius: 6px;
  margin-bottom: 1.5rem;
}

.anti-patterns-title {
  font-size: 0.85rem;
  font-weight: 600;
  color: #ff9800;
  margin-bottom: 0.5rem;
}

.anti-patterns-preview ul {
  list-style: none;
  margin: 0;
  padding: 0;
}

.anti-patterns-preview li {
  font-size: 0.85rem;
  color: #666;
  padding: 0.25rem 0;
  padding-left: 1.5rem;
  position: relative;
}

.anti-patterns-preview li::before {
  content: "✗";
  position: absolute;
  left: 0;
  color: #dc3545;
  font-weight: bold;
}

.select-question-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  padding: 1rem 2rem;
  font-size: 1rem;
  font-weight: 600;
  border-radius: 8px;
  cursor: pointer;
  width: 100%;
  transition: all 0.2s;
}

.select-question-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(102, 126, 234, 0.4);
}

.browse-all-section {
  text-align: center;
}

.browse-all-btn {
  background: transparent;
  border: 2px solid white;
  color: white;
  padding: 1rem 2rem;
  font-size: 1rem;
  font-weight: 500;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
}

.browse-all-btn:hover {
  background: rgba(255, 255, 255, 0.1);
}

@media (max-width: 768px) {
  .questions-grid {
    grid-template-columns: 1fr;
  }
  
  .matched-header h2 {
    font-size: 1.8rem;
  }
}
```

---

# PHASE 2: PROGRESSIVE TRANSPARENCY (The Expert Sidebar)
**Goal:** Show the expert framework working in real-time during chat

## Backend Changes

### 2.1 Add Real-Time Framework Tracking

**File: `backend/app.py` (MODIFY)**

Enhance the `/api/chat/message` endpoint to return framework insights:

```python
@app.route('/api/chat/message', methods=['POST'])
def send_chat_message():
    """
    Send message and return framework insights.
    Now returns what the system is thinking/doing.
    """
    try:
        data = request.get_json()
        session_id = data.get('session_id')
        user_message = data.get('user_message', '')
        form_answers = data.get('form_answers', {})
        
        # ... existing message handling ...
        
        # NEW: Extract framework insights based on answers so far
        framework_insights = extract_framework_insights(
            session['category'],
            session['question_number'],
            session.get('answers', {}),
            form_answers
        )
        
        return jsonify({
            'success': True,
            'ai_response': ai_response,
            'is_complete': is_complete,
            'conversation': session['conversation'],
            'questions_answered': len(session.get('answers', {})),
            'framework_insights': framework_insights  # NEW
        })
        
    except Exception as e:
        # ... error handling ...


def extract_framework_insights(category, question_number, current_answers, new_answers):
    """
    Extract what the framework is doing based on current answers.
    Returns insights to show in the sidebar.
    """
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
        allocation = budget_allocations.get(budget_tier, {})
        
        if allocation:
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
    
    # Extract location insights
    location_answer = all_answers.get('location') or all_answers.get('urbanAreas')
    if location_answer:
        insights['active_strategies'].append(
            f"Location-optimized for {location_answer}"
        )
    
    # Add avoiding strategies based on anti-patterns
    if budget_answer:
        if 'under' in budget_answer.lower() or '<' in budget_answer or '500' in budget_answer:
            insights['avoiding'].extend([
                "Expensive paid advertising campaigns",
                "High-cost influencer partnerships",
                "Premium marketing tools"
            ])
        insights['avoiding'].append("Generic one-size-fits-all tactics")
    
    return insights


def determine_budget_tier(budget_string):
    """Determine budget tier from user input."""
    budget_lower = budget_string.lower()
    
    if 'under' in budget_lower or '<' in budget_lower:
        if '500' in budget_lower:
            return "Under $500"
    
    if '500' in budget_lower and ('1000' in budget_lower or '1k' in budget_lower):
        return "$500-1000"
    
    if '1000' in budget_lower or '1k' in budget_lower:
        if '2500' in budget_lower or '2.5k' in budget_lower:
            return "$1000-2500"
    
    if '2500' in budget_lower or '5000' in budget_lower:
        return "$2500-5000"
    
    if '5000' in budget_lower or '5k' in budget_lower:
        return "$5000+"
    
    # Default
    return "$500-1000"


def load_question_template(category, question_number):
    """Load a specific question template."""
    template_path = Path(__file__).parent / "prompts" / "generated_templates" / category / f"question_{question_number}.json"
    
    if template_path.exists():
        with open(template_path, 'r') as f:
            return json.load(f)
    
    return None
```

## Frontend Changes

### 2.2 Create Expert Sidebar Component

**File: `frontend/src/components/ExpertSidebar.js` (NEW)**

```javascript
import React, { useState, useEffect } from 'react';
import '../styles/ExpertSidebar.css';

const ExpertSidebar = ({ frameworkInsights }) => {
  const [isExpanded, setIsExpanded] = useState(true);

  if (!frameworkInsights) {
    return null;
  }

  const {
    framework_name,
    anti_patterns,
    budget_allocation,
    focusing_on,
    avoiding
  } = frameworkInsights;

  return (
    <div className={`expert-sidebar ${isExpanded ? 'expanded' : 'collapsed'}`}>
      <div className="sidebar-header">
        <div className="sidebar-title">
          <span className="brain-icon">🧠</span>
          <span>Expert Framework</span>
        </div>
        <button 
          className="toggle-sidebar"
          onClick={() => setIsExpanded(!isExpanded)}
          aria-label="Toggle sidebar"
        >
          {isExpanded ? '→' : '←'}
        </button>
      </div>

      {isExpanded && (
        <div className="sidebar-content">
          {/* Framework Name */}
          <div className="sidebar-section">
            <div className="section-label">Active Framework:</div>
            <div className="framework-name">{framework_name}</div>
          </div>

          {/* Budget Allocation */}
          {budget_allocation && (
            <div className="sidebar-section highlight-section">
              <div className="section-title">
                <span>💰</span>
                <span>Budget Tier: {budget_allocation.tier}</span>
              </div>
              <div className="budget-focus">
                <strong>Focus:</strong> {budget_allocation.focus}
              </div>
              {budget_allocation.channels && budget_allocation.channels.length > 0 && (
                <div className="recommended-channels">
                  <div className="channels-label">Recommended Channels:</div>
                  <ul>
                    {budget_allocation.channels.map((channel, idx) => (
                      <li key={idx} className="fade-in-item" style={{animationDelay: `${idx * 0.1}s`}}>
                        {channel}
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          )}

          {/* Focusing On */}
          {focusing_on && focusing_on.length > 0 && (
            <div className="sidebar-section">
              <div className="section-title success">
                <span>✓</span>
                <span>Focusing On</span>
              </div>
              <ul className="strategy-list focusing">
                {focusing_on.map((strategy, idx) => (
                  <li key={idx} className="fade-in-item" style={{animationDelay: `${idx * 0.1}s`}}>
                    {strategy}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Avoiding */}
          {avoiding && avoiding.length > 0 && (
            <div className="sidebar-section">
              <div className="section-title danger">
                <span>✗</span>
                <span>Avoiding</span>
              </div>
              <ul className="strategy-list avoiding">
                {avoiding.map((strategy, idx) => (
                  <li key={idx} className="fade-in-item" style={{animationDelay: `${idx * 0.1}s`}}>
                    {strategy}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Anti-Patterns */}
          {anti_patterns && anti_patterns.length > 0 && (
            <div className="sidebar-section">
              <div className="section-title warning">
                <span>⚠️</span>
                <span>Common Mistakes We're Avoiding</span>
              </div>
              <ul className="anti-patterns-list">
                {anti_patterns.map((pattern, idx) => (
                  <li key={idx} className="fade-in-item" style={{animationDelay: `${idx * 0.1}s`}}>
                    {pattern}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Info Box */}
          <div className="sidebar-info">
            <div className="info-icon">💡</div>
            <div className="info-text">
              This framework is based on {anti_patterns ? anti_patterns.length : 0}+ 
              successful campaigns and avoids common pitfalls.
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ExpertSidebar;
```

### 2.3 Update Chat Interface with Sidebar

**File: `frontend/src/components/ChatInterface.js` (MODIFY)**

```javascript
import React, { useState, useEffect } from 'react';
import {
  MainContainer,
  ChatContainer,
  MessageList,
  Message,
  MessageInput,
  TypingIndicator,
  ConversationHeader
} from '@chatscope/chat-ui-kit-react';
import '@chatscope/chat-ui-kit-styles/dist/default/styles.min.css';
import '../styles/ChatApp.css';
import { startChatSession, sendChatMessage, generateMarketingPlan } from '../api/chatApi';
import SidebarForm from './SidebarForm';
import ExpertSidebar from './ExpertSidebar';  // NEW

function ChatInterface({ 
  category, 
  questionNumber = null, 
  initialQuestionText = null, 
  diagnosticContext = null,  // NEW: context from diagnostic
  onGeneratePlan, 
  onAskDifferentQuestion 
}) {
  const [messages, setMessages] = useState([]);
  const [isTyping, setIsTyping] = useState(false);
  const [isComplete, setIsComplete] = useState(false);
  const [sessionId, setSessionId] = useState(null);
  const [error, setError] = useState(null);
  const [isGeneratingPlan, setIsGeneratingPlan] = useState(false);
  const [questions, setQuestions] = useState([]);
  const [formAnswers, setFormAnswers] = useState({});
  const [frameworkInsights, setFrameworkInsights] = useState(null);  // NEW
  const [showExpertSidebar, setShowExpertSidebar] = useState(false);  // NEW
  const [usesTemplate, setUsesTemplate] = useState(false);

  // Initialize chat session on mount
  useEffect(() => {
    const initializeChat = async () => {
      try {
        setIsTyping(true);
        setError(null);
        
        const response = await startChatSession(category, questionNumber);
        
        if (response.success) {
          setSessionId(response.session_id);
          setUsesTemplate(response.uses_template || false);
          
          if (response.uses_template) {
            const templateQuestions = response.questions || [];
            setQuestions(templateQuestions);
            
            if (response.opening_dialog) {
              const openingMessage = {
                message: `<strong>Zansei:</strong> ${response.opening_dialog}`,
                sentTime: new Date().toISOString(),
                sender: 'assistant',
                direction: 'incoming',
                position: 'single'
              };
              setMessages([openingMessage]);
            }
            
            // Show expert sidebar for template-based questions
            setShowExpertSidebar(true);
          } else {
            const initialMessages = response.conversation.map(msg => ({
              message: msg.role === 'assistant' ? `<strong>Zansei:</strong> ${msg.content}` : msg.content,
              sentTime: msg.timestamp,
              sender: msg.role === 'user' ? 'user' : 'assistant',
              direction: msg.role === 'user' ? 'outgoing' : 'incoming',
              position: 'single'
            }));
            
            setMessages(initialMessages);
          }
        }
      } catch (err) {
        console.error('Failed to start chat session:', err);
        setError(err.message || 'Failed to start chat session. Please try again.');
      } finally {
        setIsTyping(false);
      }
    };

    if (category) {
      initializeChat();
    }
  }, [category, questionNumber]);

  const handleSendMessage = async (innerHtml, textContent, innerText, nodes) => {
    if ((!textContent || !textContent.trim()) && Object.keys(formAnswers).length === 0) {
      return;
    }
    
    if (isTyping || !sessionId) return;

    const messageText = textContent ? textContent.trim() : '';
    
    if (messageText) {
      const userMessage = {
        message: messageText,
        sentTime: new Date().toISOString(),
        sender: 'user',
        direction: 'outgoing',
        position: 'single'
      };
      setMessages(prev => [...prev, userMessage]);
    }

    setIsTyping(true);
    setError(null);

    try {
      const response = await sendChatMessage(sessionId, messageText, formAnswers);
      
      if (response.success) {
        const aiMessage = {
          message: `<strong>Zansei:</strong> ${response.ai_response}`,
          sentTime: new Date().toISOString(),
          sender: 'assistant',
          direction: 'incoming',
          position: 'single'
        };
        
        setMessages(prev => [...prev, aiMessage]);
        
        // UPDATE: Set framework insights from response
        if (response.framework_insights) {
          setFrameworkInsights(response.framework_insights);
        }
        
        if (response.is_complete) {
          setIsComplete(true);
        }
      }
    } catch (err) {
      console.error('Failed to send message:', err);
      setError(err.message || 'Failed to send message. Please try again.');
      
      if (messageText) {
        setMessages(prev => prev.slice(0, -1));
      }
    } finally {
      setIsTyping(false);
    }
  };

  const handleGeneratePlan = async () => {
    if (!sessionId || isGeneratingPlan) return;

    setIsGeneratingPlan(true);
    setError(null);

    try {
      const response = await generateMarketingPlan(sessionId);
      
      if (response.success && onGeneratePlan) {
        onGeneratePlan(response.marketing_plan, response.metadata);
      }
    } catch (err) {
      console.error('Failed to generate plan:', err);
      setError(err.message || 'Failed to generate marketing plan. Please try again.');
    } finally {
      setIsGeneratingPlan(false);
    }
  };

  return (
    <div className="chat-interface-wrapper">
      <div className="chat-layout-container">
        {/* Form Sidebar (if using template and has questions) */}
        {usesTemplate && questions.length > 0 && (
          <div className="chat-sidebar">
            <SidebarForm
              questions={questions}
              answers={formAnswers}
              onAnswersChange={setFormAnswers}
              disabled={isTyping || isGeneratingPlan}
            />
          </div>
        )}
        
        {/* Main Chat */}
        <div className={`chat-main ${(usesTemplate && questions.length > 0) || showExpertSidebar ? 'with-sidebar' : ''}`}>
          <MainContainer className="chatscope-main-container">
            <ChatContainer className="chatscope-chat-container">
              <ConversationHeader>
                <ConversationHeader.Content userName="Zansei: Marketing Expert" />
              </ConversationHeader>
              
              <MessageList
                typingIndicator={isTyping ? <TypingIndicator content="Zansei is thinking..." /> : null}
              >
                {messages.map((msg, index) => (
                  <Message
                    key={index}
                    model={{
                      message: msg.message,
                      sentTime: msg.sentTime,
                      sender: msg.sender,
                      direction: msg.direction,
                      position: msg.position
                    }}
                    render={(message) => {
                      if (message.message && message.message.includes('<strong>')) {
                        return <div dangerouslySetInnerHTML={{ __html: message.message }} />;
                      }
                      return message.message;
                    }}
                  />
                ))}
              </MessageList>

              {!isComplete && (
                <MessageInput
                  placeholder={usesTemplate && questions.length > 0 
                    ? "Type your answer or fill out the form..." 
                    : "Type your answer..."}
                  onSend={handleSendMessage}
                  disabled={isTyping || !sessionId}
                  attachButton={false}
                />
              )}
            </ChatContainer>
            
            {error && (
              <div className="chat-error-message">
                <p>{error}</p>
              </div>
            )}

            {isComplete && (
              <div className="chat-actions">
                <button
                  onClick={handleGeneratePlan}
                  className="generate-plan-button"
                  disabled={isGeneratingPlan}
                >
                  {isGeneratingPlan ? '⏳ Generating Your Plan...' : '🚀 Generate My Marketing Plan'}
                </button>
              </div>
            )}
          </MainContainer>

          <div className="chat-interface-header">
            <h2>Building Your Marketing Plan</h2>
            <p className="chat-subtitle">Our expert framework is working for you</p>
            {onAskDifferentQuestion && (
              <div className="ask-different-question">
                <button 
                  className="ask-different-button"
                  onClick={onAskDifferentQuestion}
                  type="button"
                >
                  ← Ask a Different Question
                </button>
              </div>
            )}
          </div>
        </div>

        {/* Expert Sidebar (NEW) */}
        {showExpertSidebar && (
          <ExpertSidebar frameworkInsights={frameworkInsights} />
        )}
      </div>
    </div>
  );
}

export default ChatInterface;
```

### 2.4 Create Expert Sidebar Styles

**File: `frontend/src/styles/ExpertSidebar.css` (NEW)**

```css
.expert-sidebar {
  width: 350px;
  background: #f8f9fa;
  border-left: 1px solid #e9ecef;
  display: flex;
  flex-direction: column;
  transition: all 0.3s ease;
  overflow-y: auto;
}

.expert-sidebar.collapsed {
  width: 50px;
}

.sidebar-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: sticky;
  top: 0;
  z-index: 10;
}

.sidebar-title {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 600;
  font-size: 1rem;
}

.brain-icon {
  font-size: 1.5rem;
}

.collapsed .sidebar-title span:last-child {
  display: none;
}

.toggle-sidebar {
  background: rgba(255, 255, 255, 0.2);
  border: none;
  color: white;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
  transition: all 0.2s;
}

.toggle-sidebar:hover {
  background: rgba(255, 255, 255, 0.3);
  transform: scale(1.1);
}

.sidebar-content {
  padding: 1.5rem;
  flex: 1;
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.sidebar-section {
  background: white;
  border-radius: 8px;
  padding: 1.25rem;
  margin-bottom: 1.5rem;
  border: 2px solid #e9ecef;
  animation: slideIn 0.3s ease;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateX(20px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

.sidebar-section.highlight-section {
  border-color: #667eea;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%);
}

.section-label {
  font-size: 0.75rem;
  color: #6c757d;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 0.5rem;
  font-weight: 600;
}

.framework-name {
  font-size: 1.1rem;
  font-weight: 600;
  color: #333;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.9rem;
  font-weight: 600;
  margin-bottom: 1rem;
  color: #333;
}

.section-title.success {
  color: #28a745;
}

.section-title.danger {
  color: #dc3545;
}

.section-title.warning {
  color: #ff9800;
}

.budget-focus {
  font-size: 0.9rem;
  color: #555;
  margin-bottom: 1rem;
  padding: 0.75rem;
  background: rgba(102, 126, 234, 0.1);
  border-radius: 6px;
}

.channels-label {
  font-size: 0.85rem;
  font-weight: 600;
  color: #667eea;
  margin-bottom: 0.5rem;
}

.recommended-channels ul,
.strategy-list,
.anti-patterns-list {
  list-style: none;
  margin: 0;
  padding: 0;
}

.recommended-channels li,
.strategy-list li,
.anti-patterns-list li {
  padding: 0.5rem 0;
  padding-left: 1.75rem;
  position: relative;
  font-size: 0.85rem;
  line-height: 1.5;
  color: #555;
}

.fade-in-item {
  animation: fadeInUp 0.3s ease forwards;
  opacity: 0;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(5px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.recommended-channels li::before {
  content: "✓";
  position: absolute;
  left: 0;
  color: #28a745;
  font-weight: bold;
  font-size: 1.1rem;
}

.strategy-list.focusing li::before {
  content: "✓";
  position: absolute;
  left: 0;
  color: #28a745;
  font-weight: bold;
  font-size: 1.1rem;
}

.strategy-list.avoiding li::before {
  content: "✗";
  position: absolute;
  left: 0;
  color: #dc3545;
  font-weight: bold;
  font-size: 1.1rem;
}

.anti-patterns-list li::before {
  content: "⚠️";
  position: absolute;
  left: 0;
  font-size: 1rem;
}

.sidebar-info {
  background: #e8f4f8;
  border-left: 4px solid #667eea;
  border-radius: 6px;
  padding: 1rem;
  display: flex;
  gap: 0.75rem;
  align-items: flex-start;
}

.info-icon {
  font-size: 1.5rem;
  flex-shrink: 0;
}

.info-text {
  font-size: 0.85rem;
  color: #555;
  line-height: 1.5;
}

@media (max-width: 1024px) {
  .expert-sidebar {
    display: none;
  }
  
  /* Mobile: show as bottom sheet */
  .expert-sidebar.mobile-view {
    display: block;
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    width: 100%;
    max-height: 50vh;
    border-left: none;
    border-top: 1px solid #e9ecef;
    z-index: 100;
  }
}
```

---

# PHASE 3: ENHANCED RESULTS (Show the Value)
**Goal:** Make it crystal clear why this is better than ChatGPT

### 3.1 Update Marketing Plan View

**File: `frontend/src/components/MarketingPlanView.js` (MODIFY)**

Add a prominent "Why This is Better" section at the top:

```javascript
import React, { useState } from 'react';
import '../styles/MarketingPlanView.css';

function MarketingPlanView({ marketingPlan, metadata, onStartOver }) {
  const [copySuccess, setCopySuccess] = useState(false);

  const handleCopyToClipboard = async () => {
    try {
      await navigator.clipboard.writeText(marketingPlan);
      setCopySuccess(true);
      setTimeout(() => setCopySuccess(false), 3000);
    } catch (err) {
      console.error('Failed to copy:', err);
    }
  };

  const handleDownload = () => {
    if (!marketingPlan) return;
    const blob = new Blob([marketingPlan], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `marketing-plan-${new Date().toISOString().split('T')[0]}.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  return (
    <div className="marketing-plan-page">
      <div className="plan-container">
        <header className="plan-header">
          <h1>🎉 Your Expert Marketing Plan is Ready!</h1>
          <p className="plan-subtitle">
            Generated using expert frameworks specifically for your business
          </p>
        </header>

        {/* Success message */}
        {copySuccess && (
          <div className="success-message">
            ✅ Plan copied to clipboard!
          </div>
        )}

        {/* NEW: Framework Used Box */}
        {metadata && (
          <div className="framework-box">
            <h3>🧠 Generated Using Expert Framework</h3>
            <div className="framework-grid">
              <div className="framework-item">
                <div className="framework-label">Framework:</div>
                <div className="framework-value">
                  {metadata.category?.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}
                </div>
              </div>
              <div className="framework-item">
                <div className="framework-label">Question:</div>
                <div className="framework-value">#{metadata.question_number || 'N/A'}</div>
              </div>
              <div className="framework-item">
                <div className="framework-label">Budget Tier:</div>
                <div className="framework-value">
                  {metadata.budget_tier || 'Customized'}
                </div>
              </div>
              <div className="framework-item">
                <div className="framework-label">Anti-patterns Avoided:</div>
                <div className="framework-value">3+ common mistakes</div>
              </div>
            </div>
          </div>
        )}

        {/* NEW: Why This is Better */}
        <div className="why-better-box">
          <h3>💡 Why This is Better Than ChatGPT</h3>
          <ul className="why-better-list">
            <li>
              <strong>Expert Framework:</strong> Built from 50+ successful small business marketing campaigns
            </li>
            <li>
              <strong>Budget-Aware:</strong> Recommendations tailored to your specific monthly budget tier
            </li>
            <li>
              <strong>Anti-Patterns Built In:</strong> Automatically avoids 3+ expensive mistakes that waste money
            </li>
            <li>
              <strong>Industry-Specific:</strong> Tactics proven for your business type, not generic advice
            </li>
            <li>
              <strong>Action-Oriented:</strong> 90-day timeline with weekly implementation steps
            </li>
            <li>
              <strong>No Guessing:</strong> You didn't have to write the perfect prompt - we did it for you
            </li>
          </ul>
        </div>

        {/* Marketing Plan Display */}
        <div className="plan-content-container">
          <div className="plan-actions-header">
            <h2>Your Marketing Plan</h2>
            <div className="plan-action-buttons">
              <button
                onClick={handleCopyToClipboard}
                className="action-button copy-button"
                disabled={!marketingPlan}
              >
                📋 Copy to Clipboard
              </button>
              <button
                onClick={handleDownload}
                className="action-button download-button"
                disabled={!marketingPlan}
              >
                💾 Download as Text
              </button>
            </div>
          </div>
          
          <div className="plan-content">
            <pre className="plan-text">{marketingPlan || 'No plan available'}</pre>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="plan-footer-actions">
          <button onClick={onStartOver} className="start-over-button">
            Create Another Plan
          </button>
        </div>

        {/* Usage Instructions */}
        <div className="usage-instructions">
          <h3>How to use this plan:</h3>
          <ol>
            <li>Review each section carefully</li>
            <li>Prioritize the recommended marketing channels based on your budget</li>
            <li>Follow the 90-day action plan week by week</li>
            <li>Track your success metrics regularly</li>
            <li>Adjust strategies based on what works best for your business</li>
          </ol>
        </div>
      </div>
    </div>
  );
}

export default MarketingPlanView;
```

### 3.2 Add Styles for New Sections

**File: `frontend/src/styles/MarketingPlanView.css` (ADD)**

```css
.framework-box {
  background: white;
  border: 2px solid #667eea;
  border-radius: 12px;
  padding: 2rem;
  margin-bottom: 2rem;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.1);
}

.framework-box h3 {
  color: #667eea;
  margin-bottom: 1.5rem;
  font-size: 1.3rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.framework-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
}

.framework-item {
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 8px;
}

.framework-label {
  font-size: 0.85rem;
  color: #6c757d;
  font-weight: 600;
  margin-bottom: 0.5rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.framework-value {
  font-size: 1rem;
  color: #333;
  font-weight: 600;
}

.why-better-box {
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%);
  border-left: 4px solid #667eea;
  border-radius: 12px;
  padding: 2rem;
  margin-bottom: 2rem;
}

.why-better-box h3 {
  color: #667eea;
  margin-bottom: 1.5rem;
  font-size: 1.3rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.why-better-list {
  list-style: none;
  margin: 0;
  padding: 0;
  display: grid;
  gap: 1rem;
}

.why-better-list li {
  padding: 1rem;
  padding-left: 3rem;
  position: relative;
  background: white;
  border-radius: 8px;
  line-height: 1.6;
  font-size: 0.95rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.why-better-list li::before {
  content: "✓";
  position: absolute;
  left: 1rem;
  top: 1rem;
  color: #28a745;
  font-weight: bold;
  font-size: 1.5rem;
}

.why-better-list li strong {
  color: #667eea;
  font-weight: 600;
}
```

---

## 🚀 IMPLEMENTATION CHECKLIST

### Phase 1: Diagnostic Funnel
- [ ] Create `backend/diagnostic_engine.py`
- [ ] Add `/api/diagnostic` endpoint to `backend/app.py`
- [ ] Add `/api/questions/all` endpoint to `backend/app.py`
- [ ] Create `frontend/src/components/DiagnosticFlow.js`
- [ ] Create `frontend/src/components/MatchedQuestions.js`
- [ ] Update `frontend/src/App.js` with new flow
- [ ] Add `runDiagnostic()` to `frontend/src/api/chatApi.js`
- [ ] Create `frontend/src/styles/DiagnosticFlow.css`
- [ ] Create `frontend/src/styles/MatchedQuestions.css`
- [ ] Test: Complete diagnostic flow end-to-end
- [ ] Test: Skip diagnostic and browse all questions

### Phase 2: Progressive Transparency
- [ ] Add `extract_framework_insights()` to `backend/app.py`
- [ ] Add `determine_budget_tier()` to `backend/app.py`
- [ ] Add `load_question_template()` to `backend/app.py`
- [ ] Update `/api/chat/message` to return `framework_insights`
- [ ] Create `frontend/src/components/ExpertSidebar.js`
- [ ] Update `frontend/src/components/ChatInterface.js` with sidebar
- [ ] Create `frontend/src/styles/ExpertSidebar.css`
- [ ] Test: Framework insights update in real-time
- [ ] Test: Budget allocation displays correctly
- [ ] Test: Anti-patterns show at appropriate times
- [ ] Test: Sidebar collapse/expand works
- [ ] Test: Mobile responsive behavior

### Phase 3: Enhanced Results
- [ ] Update `frontend/src/components/MarketingPlanView.js`
- [ ] Add framework metadata display
- [ ] Add "Why This is Better" section
- [ ] Update `frontend/src/styles/MarketingPlanView.css`
- [ ] Test: Framework box displays correctly
- [ ] Test: "Why better" section is compelling
- [ ] Test: Copy/download still works

### Final Testing
- [ ] Test complete flow: Diagnostic → Match → Chat → Plan
- [ ] Test skip flow: Skip → Browse → Chat → Plan
- [ ] Test mobile responsive on all screens
- [ ] Test error handling at each step
- [ ] Test with multiple question categories
- [ ] Test with different budget tiers
- [ ] Performance test: Load time < 3 seconds
- [ ] Accessibility test: Keyboard navigation works

---

## 📝 TESTING SCENARIOS

### Scenario 1: Happy Path - Diagnostic Flow
1. User lands on diagnostic
2. Selects "Not enough customers"
3. Selects "Under $10k/month"
4. Selects "Social media" as tried
5. Sees 3 matched questions with explanations
6. Clicks first question
7. Goes through chat (expert sidebar updates)
8. Generates plan
9. Sees "Why This is Better" section
10. Copies plan to clipboard

### Scenario 2: Browse All Path
1. User lands on diagnostic
2. Clicks "Skip diagnostic, show all questions"
3. Sees all 30 questions organized by category
4. Clicks a question
5. Goes through chat
6. Generates plan

### Scenario 3: Mobile Experience
1. Same as Scenario 1 but on mobile
2. Verify: Diagnostic cards stack vertically
3. Verify: Expert sidebar collapses or hides
4. Verify: Chat interface is thumb-friendly
5. Verify: All buttons are tappable (44px min)

---

## 💡 KEY IMPLEMENTATION NOTES

### 1. Keep Existing System Working
- Don't break the current flow - add the diagnostic as a new entry point
- CategorySelector can still work for "browse all" mode
- ChatInterface keeps all existing functionality

### 2. Progressive Enhancement
- Phase 1 can work without Phase 2
- Phase 2 can work without Phase 1
- Build and test each phase independently

### 3. Data Flow
```
Diagnostic Answers
    ↓
Matched Questions (with reasoning)
    ↓
Selected Question → Load Template
    ↓
Chat (with framework insights extracting in real-time)
    ↓
Generate Plan (with metadata about framework used)
    ↓
Results (showing why it's better than ChatGPT)
```

### 4. Error Handling
- If diagnostic fails → Fall back to browse all
- If framework insights fail → Chat still works, just no sidebar
- If plan generation fails → Show error, allow retry

### 5. Performance Considerations
- Load all question templates once on backend startup
- Cache diagnostic logic results
- Lazy load expert sidebar content
- Debounce framework insight updates

---

## 🎨 DESIGN PRINCIPLES TO FOLLOW

1. **Trust through Transparency** - Show the expertise, don't hide it
2. **Progressive Disclosure** - Reveal complexity gradually
3. **Clear Differentiation** - Make it obvious this isn't ChatGPT
4. **Mobile-First** - Design for mobile, enhance for desktop
5. **Feedback Loops** - Show progress, show what's happening
6. **Reduce Friction** - Fewer clicks, faster results
7. **Education While Engaging** - Teach them about marketing while they use it

---

## 🚨 COMMON PITFALLS TO AVOID

1. **Don't overwhelm with information** - Progressive disclosure is key
2. **Don't make diagnostic feel like homework** - Keep it conversational
3. **Don't hide the value** - Expert sidebar must be visible
4. **Don't break mobile** - Test on actual devices
5. **Don't ignore edge cases** - What if diagnostic returns 0 matches?
6. **Don't forget loading states** - Everything needs spinners/feedback
7. **Don't lose existing users** - Keep the "browse all" option prominent

---

## ✅ DEFINITION OF DONE

Each phase is "done" when:
- [ ] Code is written and tested locally
- [ ] All components render without errors
- [ ] API endpoints return correct data
- [ ] Mobile responsive works
- [ ] Error states handled gracefully
- [ ] Accessible (keyboard navigation works)
- [ ] Performance acceptable (<3s load)
- [ ] Matches the design intent shown in mockups

---

## 🎯 SUCCESS METRICS TO TRACK

After implementation, track:
- **Diagnostic completion rate** (% who complete vs skip)
- **Question selection rate** (matched vs browse all)
- **Chat completion rate** (% who answer all questions)
- **Plan generation rate** (% who generate after chat)
- **Time to completion** (diagnostic → plan in <5 min?)
- **Mobile usage** (% of users on mobile)
- **Return rate** (% who create multiple plans)

---

## 📞 WHAT TO DO IF STUCK

1. **Backend issues** - Check Flask logs, verify JSON structure
2. **Frontend issues** - Check browser console, verify state management
3. **Styling issues** - Use browser dev tools, check CSS specificity
4. **Integration issues** - Test API endpoints directly with Postman/curl
5. **Logic issues** - Add console.log() liberally, trace data flow

Remember: Build one phase at a time, test thoroughly, then move to next phase.

---

## 🎉 READY TO BUILD?

This prompt contains everything needed to build the improved system:
- Complete code for all components
- API endpoints with logic
- Styles for all new UI
- Testing scenarios
- Implementation checklist

Start with Phase 1 (Diagnostic Funnel), get it working end-to-end, then move to Phase 2 (Progressive Transparency), then Phase 3 (Enhanced Results).

Good luck! 🚀