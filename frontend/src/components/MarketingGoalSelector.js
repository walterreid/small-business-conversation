import React, { useState, useEffect } from 'react';
import '../styles/MarketingGoalSelector.css';
import { getMarketingGoals, getQuestionTemplate } from '../api/chatApi';

/**
 * MarketingGoalSelector Component
 * 
 * Redesigned with tab-based category selection and engaging question cards.
 * Uses the same design system as diagnostic flow for consistency.
 * 
 * Props:
 * - onSelectQuestion: Callback when user clicks on a question
 *     (category, question_number, question_text, template)
 */
function MarketingGoalSelector({ onSelectQuestion }) {
  const [goals, setGoals] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedCategory, setSelectedCategory] = useState(null);
  const [hoveredQuestion, setHoveredQuestion] = useState(null);
  const [questionTemplates, setQuestionTemplates] = useState({}); // Cache templates for anti-patterns

  // Load marketing goals on mount
  useEffect(() => {
    const loadGoals = async () => {
      try {
        setLoading(true);
        const data = await getMarketingGoals();
        setGoals(data.goals);
        
        // Set first category as default selection
        const goalsArray = Object.values(data.goals);
        if (goalsArray.length > 0) {
          setSelectedCategory(goalsArray[0].category);
        }
      } catch (err) {
        console.error('Error loading marketing goals:', err);
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    loadGoals();
  }, []);

  // Load template for a question when hovered (for anti-patterns preview)
  const handleQuestionHover = async (category, questionNumber) => {
    const cacheKey = `${category}_${questionNumber}`;
    if (questionTemplates[cacheKey]) {
      return; // Already loaded
    }

    try {
      const templateData = await getQuestionTemplate(category, questionNumber);
      setQuestionTemplates(prev => ({
        ...prev,
        [cacheKey]: templateData.template
      }));
    } catch (err) {
      console.error('Error loading question template:', err);
    }
  };

  const handleQuestionClick = async (category, questionNumber, questionText) => {
    if (onSelectQuestion) {
      // Load the full template when question is clicked
      try {
        const templateData = await getQuestionTemplate(category, questionNumber);
        onSelectQuestion(category, questionNumber, questionText, templateData.template);
      } catch (err) {
        console.error('Error loading question template:', err);
        // Still call onSelectQuestion with basic info if template load fails
        onSelectQuestion(category, questionNumber, questionText, null);
      }
    }
  };

  if (loading) {
    return (
      <div className="marketing-goal-selector">
        <div className="loading-state">
          <div className="loading-spinner"></div>
          <p>Loading expert questions...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="marketing-goal-selector">
        <div className="error-state">
          <div className="error-icon">⚠️</div>
          <p>Error: {error}</p>
          <button onClick={() => window.location.reload()} className="retry-button">
            Try Again
          </button>
        </div>
      </div>
    );
  }

  if (!goals) {
    return (
      <div className="marketing-goal-selector">
        <div className="error-state">
          <p>No marketing goals found</p>
        </div>
      </div>
    );
  }

  // Convert goals object to array for rendering
  const goalsArray = Object.values(goals);
  const selectedGoal = goalsArray.find(g => g.category === selectedCategory);
  const questions = selectedGoal?.questions || [];

  return (
    <div className="marketing-goal-selector">
      {/* Category Tabs */}
      <div className="category-tabs">
        {goalsArray.map((goal) => (
          <button
            key={goal.category}
            className={`category-tab ${selectedCategory === goal.category ? 'active' : ''}`}
            onClick={() => setSelectedCategory(goal.category)}
          >
            <span className="tab-icon">{goal.icon}</span>
            <span className="tab-name">{goal.display_name}</span>
            <span className="tab-count">({goal.questions?.length || 0})</span>
          </button>
        ))}
      </div>

      {/* Selected Category Info */}
      {selectedGoal && (
        <div className="category-info">
          <div className="category-info-content">
            <h3>{selectedGoal.display_name}</h3>
            <p>{selectedGoal.description}</p>
          </div>
        </div>
      )}

      {/* Questions Grid */}
      <div className="questions-container">
        {questions.length === 0 ? (
          <div className="no-questions">
            <p>No questions available for this category.</p>
          </div>
        ) : (
          <div className="questions-grid">
            {questions.map((question, idx) => {
              const cacheKey = `${question.category}_${question.question_number}`;
              const template = questionTemplates[cacheKey];
              const antiPatterns = template?.anti_patterns || [];
              
              return (
                <div
                  key={question.question_number}
                  className="question-card"
                  onClick={() => handleQuestionClick(
                    question.category,
                    question.question_number,
                    question.question_text
                  )}
                  onMouseEnter={() => {
                    setHoveredQuestion(`${question.category}_${question.question_number}`);
                    handleQuestionHover(question.category, question.question_number);
                  }}
                  onMouseLeave={() => setHoveredQuestion(null)}
                  style={{ animationDelay: `${idx * 0.05}s` }}
                >
                  <div className="question-card-header">
                    <div className="question-number-badge">
                      #{question.question_number}
                    </div>
                    {hoveredQuestion === `${question.category}_${question.question_number}` && antiPatterns.length > 0 && (
                      <div className="anti-patterns-badge">
                        ⚠️ Avoids {antiPatterns.length} mistakes
                      </div>
                    )}
                  </div>
                  
                  <div className="question-card-content">
                    <h4 className="question-card-text">{question.question_text}</h4>
                  </div>

                  {hoveredQuestion === `${question.category}_${question.question_number}` && antiPatterns.length > 0 && (
                    <div className="question-card-preview">
                      <div className="preview-title">You'll avoid:</div>
                      <ul className="preview-list">
                        {antiPatterns.slice(0, 2).map((pattern, pidx) => (
                          <li key={pidx}>{pattern}</li>
                        ))}
                      </ul>
                    </div>
                  )}

                  <div className="question-card-footer">
                    <button className="start-question-btn">
                      Start This Strategy →
                    </button>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>

      {/* Info Box */}
      <div className="browse-info-box">
        <div className="info-icon">💡</div>
        <div className="info-content">
          <strong>30 Expert Questions</strong>
          <p>Each question uses a proven framework with anti-patterns built in. Hover over questions to see what mistakes you'll avoid.</p>
        </div>
      </div>
    </div>
  );
}

export default MarketingGoalSelector;

