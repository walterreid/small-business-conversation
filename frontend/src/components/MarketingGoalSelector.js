import React, { useState, useEffect } from 'react';
import '../styles/MarketingGoalSelector.css';
import { getMarketingGoals, getQuestionTemplate } from '../api/chatApi';

/**
 * MarketingGoalSelector Component
 * 
 * Displays marketing goal categories with questions side-by-side.
 * Category on the left, questions on the right - all visible at once.
 * 
 * Props:
 * - onSelectQuestion: Callback when user clicks on a question
 *     (category, question_number, question_text, template)
 */
function MarketingGoalSelector({ onSelectQuestion }) {
  const [goals, setGoals] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Load marketing goals on mount
  useEffect(() => {
    const loadGoals = async () => {
      try {
        setLoading(true);
        const data = await getMarketingGoals();
        setGoals(data.goals);
      } catch (err) {
        console.error('Error loading marketing goals:', err);
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    loadGoals();
  }, []);

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
        <div className="loading">Loading marketing goals...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="marketing-goal-selector">
        <div className="error">Error: {error}</div>
      </div>
    );
  }

  if (!goals) {
    return (
      <div className="marketing-goal-selector">
        <div className="error">No marketing goals found</div>
      </div>
    );
  }

  // Convert goals object to array for rendering
  const goalsArray = Object.values(goals);

  return (
    <div className="marketing-goal-selector">
      <div className="marketing-goals-list">
        {goalsArray.map((goal) => {
          const questions = goal.questions || [];
          
          return (
            <div key={goal.category} className="marketing-goal-row">
              {/* Category Card - Left Side */}
              <div className="marketing-goal-category-card">
                <div className="marketing-goal-icon">{goal.icon}</div>
                <h3 className="marketing-goal-name">{goal.display_name}</h3>
                <p className="marketing-goal-description">{goal.description}</p>
              </div>

              {/* Questions Grid - Right Side (2 columns) */}
              <div className="marketing-goal-questions">
                <div className="questions-grid">
                  {questions.map((question) => (
                    <div
                      key={question.question_number}
                      className="question-item"
                      onClick={() => handleQuestionClick(
                        goal.category,
                        question.question_number,
                        question.question_text
                      )}
                    >
                      <span className="question-number">{question.question_number}</span>
                      <span className="question-text">{question.question_text}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

export default MarketingGoalSelector;

