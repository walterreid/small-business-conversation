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

        {question.type === 'select' && question.options && (
          <select
            id={questionId}
            value={currentValue}
            onChange={(e) => handleAnswerChange(questionId, e.target.value)}
            disabled={disabled}
            className="question-select"
          >
            <option value="">Select an option...</option>
            {question.options.map((option, idx) => (
              <option key={idx} value={option}>
                {option}
              </option>
            ))}
          </select>
        )}

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

