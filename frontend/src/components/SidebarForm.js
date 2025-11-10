import React, { useState, useEffect } from 'react';
import '../styles/SidebarForm.css';

/**
 * SidebarForm Component
 * 
 * Displays form questions in a sidebar alongside the chat interface.
 * Users can fill out form fields, and answers are sent with chat messages.
 */
function SidebarForm({ questions = [], answers = {}, onAnswersChange, disabled = false }) {
  const [localAnswers, setLocalAnswers] = useState(answers);

  // Sync with parent answers
  useEffect(() => {
    setLocalAnswers(answers);
  }, [answers]);

  const handleAnswerChange = (questionId, value) => {
    const newAnswers = {
      ...localAnswers,
      [questionId]: value
    };
    setLocalAnswers(newAnswers);
    if (onAnswersChange) {
      onAnswersChange(newAnswers);
    }
  };

  const handleUsePlaceholder = (questionId, placeholder) => {
    handleAnswerChange(questionId, placeholder);
  };

  const renderQuestion = (question) => {
    const questionId = question.id;
    const currentValue = localAnswers[questionId] || '';
    const isRequired = question.required || false;
    const hasValue = currentValue.trim().length > 0;

    return (
      <div 
        key={questionId} 
        className={`sidebar-question ${isRequired && !hasValue ? 'required' : ''} ${hasValue ? 'answered' : ''}`}
      >
        <label htmlFor={questionId} className="question-label">
          {question.question}
        </label>

        {question.why_matters && (
          <p className="question-why">{question.why_matters}</p>
        )}

        {question.type === 'text' && (
          <div className="question-input-wrapper">
            <input
              type="text"
              id={questionId}
              value={currentValue}
              onChange={(e) => handleAnswerChange(questionId, e.target.value)}
              placeholder={question.placeholder || ''}
              disabled={disabled}
              className="question-input"
            />
            {question.placeholder && !hasValue && (
              <button
                type="button"
                className="use-placeholder-btn"
                onClick={() => handleUsePlaceholder(questionId, question.placeholder)}
                disabled={disabled}
                title="Use this placeholder"
              >
                ✓ Use this
              </button>
            )}
          </div>
        )}

        {question.type === 'textarea' && (
          <div className="question-input-wrapper">
            <textarea
              id={questionId}
              value={currentValue}
              onChange={(e) => handleAnswerChange(questionId, e.target.value)}
              placeholder={question.placeholder || ''}
              disabled={disabled}
              rows={4}
              className="question-textarea"
            />
            {question.placeholder && !hasValue && (
              <button
                type="button"
                className="use-placeholder-btn"
                onClick={() => handleUsePlaceholder(questionId, question.placeholder)}
                disabled={disabled}
                title="Use this placeholder"
              >
                ✓ Use this
              </button>
            )}
          </div>
        )}

        {question.type === 'select' && question.options && (() => {
          // Normalize options - handle both array and string formats
          let normalizedOptions = [];
          if (Array.isArray(question.options)) {
            // If options is an array of strings, use as-is
            normalizedOptions = question.options;
          } else if (typeof question.options === 'string') {
            // If options is a string, split by comma or pipe
            normalizedOptions = question.options.split(/[,|]/).map(opt => opt.trim()).filter(opt => opt);
          }
          
          // Ensure "Other" is always present (case-insensitive check)
          const hasOther = normalizedOptions.some(opt => 
            opt.toLowerCase().includes('other') || opt.toLowerCase() === 'other'
          );
          if (!hasOther) {
            normalizedOptions.push('Other');
          }
          
          // Check if "Other" is selected (case-insensitive)
          const isOtherSelected = currentValue && (
            currentValue.toLowerCase() === 'other' || 
            currentValue.toLowerCase().includes('other')
          );
          
          // Get the "Other" text value (stored separately)
          const otherValueKey = `${questionId}_other`;
          const otherTextValue = localAnswers[otherValueKey] || '';
          
          return (
            <div className="select-with-other-wrapper">
              <select
                id={questionId}
                value={isOtherSelected ? 'Other' : currentValue}
                onChange={(e) => {
                  const selectedValue = e.target.value;
                  if (selectedValue.toLowerCase() === 'other' || selectedValue.toLowerCase().includes('other')) {
                    // Store "Other" as the value, and clear any previous other text
                    handleAnswerChange(questionId, 'Other');
                    // Clear the other text field if switching away from other
                    if (otherTextValue) {
                      handleAnswerChange(otherValueKey, '');
                    }
                  } else {
                    // Store the selected option and clear other text
                    handleAnswerChange(questionId, selectedValue);
                    handleAnswerChange(otherValueKey, '');
                  }
                }}
                disabled={disabled}
                className="question-select"
              >
                <option value="">Select an option...</option>
                {normalizedOptions.map((option, idx) => (
                  <option key={idx} value={option}>
                    {option}
                  </option>
                ))}
              </select>
              
              {/* Show text input when "Other" is selected */}
              {isOtherSelected && (
                <div className="other-input-wrapper" style={{ marginTop: '0.5rem' }}>
                  <input
                    type="text"
                    id={otherValueKey}
                    value={otherTextValue}
                    onChange={(e) => {
                      const otherText = e.target.value;
                      handleAnswerChange(otherValueKey, otherText);
                      // Update the main answer to include the other text
                      handleAnswerChange(questionId, otherText ? `Other: ${otherText}` : 'Other');
                    }}
                    placeholder="Please specify..."
                    disabled={disabled}
                    className="question-input other-text-input"
                    autoFocus
                  />
                </div>
              )}
            </div>
          );
        })()}

        {hasValue && (
          <div className="answer-indicator">
            ✓ Answered
          </div>
        )}
      </div>
    );
  };

  // Debug logging
  useEffect(() => {
    console.log('SidebarForm rendered with:', {
      questionsCount: questions?.length || 0,
      answersCount: Object.keys(answers || {}).length,
      questions: questions
    });
  }, [questions, answers]);

  if (!questions || questions.length === 0) {
    return (
      <div className="sidebar-form empty">
        <p>No questions available</p>
        <p style={{fontSize: '0.8rem', color: '#666', marginTop: '0.5rem'}}>
          Questions prop: {questions ? `${questions.length} items` : 'undefined'}
        </p>
      </div>
    );
  }

  const answeredCount = questions.filter(q => localAnswers[q.id] && localAnswers[q.id].trim().length > 0).length;

  return (
    <div className="sidebar-form">
      <div className="sidebar-header">
        <h3>Your Information</h3>
        <div className="progress-indicator">
          <span className="progress-text">
            {answeredCount} of {questions.length} answered
          </span>
        </div>
      </div>

      <div className="sidebar-questions">
        {questions.map(renderQuestion)}
      </div>

      <div className="sidebar-footer">
        <p className="sidebar-help">
          💡 Fill out these questions or chat with us to get your personalized plan based on your question.
        </p>
      </div>
    </div>
  );
}

export default SidebarForm;

