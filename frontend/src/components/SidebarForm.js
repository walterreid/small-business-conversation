import React, { useState, useEffect, useRef } from 'react';
import '../styles/SidebarForm.css';

/**
 * QuestionLabel Component with Tooltip
 * 
 * Displays question label with optional (?) tooltip for "why it matters" text
 */
function QuestionLabel({ questionId, questionText, whyMatters }) {
  const [showTooltip, setShowTooltip] = useState(false);

  if (!whyMatters) {
    return <span className="question-text">{questionText}</span>;
  }

  return (
    <>
      <span className="question-text">{questionText}</span>
      <div 
        className="why-matters-tooltip-wrapper"
        onMouseEnter={() => setShowTooltip(true)}
        onMouseLeave={() => setShowTooltip(false)}
      >
        <button
          type="button"
          className="why-matters-icon"
          onClick={(e) => {
            e.preventDefault();
            e.stopPropagation();
            setShowTooltip(!showTooltip);
          }}
          aria-label="Why this matters"
          title="Why this matters"
        >
          ?
        </button>
        {showTooltip && (
          <div className="why-matters-tooltip">
            <div className="tooltip-arrow"></div>
            <div className="tooltip-content">
              <strong>Why it matters:</strong>
              <p>{whyMatters}</p>
            </div>
          </div>
        )}
      </div>
    </>
  );
}

/**
 * SidebarForm Component
 * 
 * Displays form questions in a sidebar alongside the chat interface.
 * Users can fill out form fields, and answers are sent with chat messages.
 */
function SidebarForm({ questions = [], answers = {}, onAnswersChange, disabled = false }) {
  const [localAnswers, setLocalAnswers] = useState(answers);

  // Sync with parent answers, but be careful not to overwrite local changes
  // Use a ref to track if we're in the middle of a local update
  const isUpdatingRef = useRef(false);
  
  useEffect(() => {
    // Don't overwrite if we just made a local change
    if (!isUpdatingRef.current) {
      setLocalAnswers(answers);
    }
    isUpdatingRef.current = false;
  }, [answers]);

  const handleAnswerChange = (questionId, value) => {
    isUpdatingRef.current = true;
    const newAnswers = {
      ...localAnswers,
      [questionId]: value
    };
    console.log('handleAnswerChange called:', { questionId, value, newAnswers });
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
    // For select dropdowns, check if value is not empty and not the placeholder
    // For other types, check if trimmed length > 0
    const hasValue = question.type === 'select' 
      ? (currentValue && currentValue !== '' && currentValue !== 'Select an option...')
      : (currentValue && typeof currentValue === 'string' && currentValue.trim().length > 0);

    return (
      <div 
        key={questionId} 
        className={`sidebar-question ${isRequired && !hasValue ? 'required' : ''} ${hasValue ? 'answered' : ''}`}
      >
        <label htmlFor={questionId} className="question-label">
          <QuestionLabel
            questionId={questionId}
            questionText={question.question}
            whyMatters={question.why_matters}
          />
        </label>

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
            {/*question.placeholder && !hasValue && (
              <button
                type="button"
                className="use-placeholder-btn"
                onClick={() => handleUsePlaceholder(questionId, question.placeholder)}
                disabled={disabled}
                title="Use this placeholder"
              >
                ✓ Use this
              </button>
            )*/}
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
            {/*question.placeholder && !hasValue && (
              <button
                type="button"
                className="use-placeholder-btn"
                onClick={() => handleUsePlaceholder(questionId, question.placeholder)}
                disabled={disabled}
                title="Use this placeholder"
              >
                ✓ Use this
              </button>
            )*/}
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
          
          // Determine the select value - must match one of the options exactly
          let selectValue = '';
          
          // Check if currentValue matches any option (case-insensitive for comparison)
          const matchingOption = normalizedOptions.find(opt => 
            opt === currentValue || opt.toLowerCase() === currentValue.toLowerCase()
          );
          
          if (isOtherSelected || (currentValue && currentValue.startsWith('Other'))) {
            selectValue = 'Other';
          } else if (matchingOption) {
            // Use the exact option value (preserves casing from options array)
            selectValue = matchingOption;
          } else if (currentValue && currentValue.trim() !== '') {
            // Value exists but doesn't match - might be a partial match or formatted differently
            // Try to find a case-insensitive match
            const caseInsensitiveMatch = normalizedOptions.find(opt => 
              opt.toLowerCase() === currentValue.toLowerCase()
            );
            if (caseInsensitiveMatch) {
              selectValue = caseInsensitiveMatch;
            } else {
              // Value doesn't match any option - show placeholder
              selectValue = '';
            }
          } else {
            // No value, show placeholder
            selectValue = '';
          }
          
          return (
            <div className="select-with-other-wrapper">
              <select
                id={questionId}
                value={selectValue}
                onChange={(e) => {
                  const selectedValue = e.target.value;
                  console.log('Select onChange triggered:', { 
                    questionId, 
                    selectedValue, 
                    currentValue,
                    normalizedOptions,
                    localAnswers: { ...localAnswers }
                  });
                  
                  if (!selectedValue || selectedValue === '') {
                    // User selected placeholder - clear the answer
                    console.log('Clearing answer for:', questionId);
                    handleAnswerChange(questionId, '');
                    handleAnswerChange(otherValueKey, '');
                    return;
                  }
                  
                  // Find the exact option value (preserves casing)
                  const exactOption = normalizedOptions.find(opt => 
                    opt === selectedValue || opt.toLowerCase() === selectedValue.toLowerCase()
                  );
                  
                  if (!exactOption) {
                    console.warn('Selected value does not match any option:', selectedValue, 'Available options:', normalizedOptions);
                    return;
                  }
                  
                  console.log('Setting answer:', { questionId, exactOption });
                  
                  if (exactOption.toLowerCase() === 'other') {
                    // Store "Other" as the value, and clear any previous other text
                    handleAnswerChange(questionId, 'Other');
                    // Clear the other text field if switching away from other
                    if (otherTextValue) {
                      handleAnswerChange(otherValueKey, '');
                    }
                  } else {
                    // Store the exact selected option (preserves casing from options array)
                    handleAnswerChange(questionId, exactOption);
                    handleAnswerChange(otherValueKey, '');
                  }
                  
                  // Log after state update
                  setTimeout(() => {
                    console.log('State after update:', { 
                      questionId, 
                      localAnswers: { ...localAnswers },
                      newValue: localAnswers[questionId]
                    });
                  }, 0);
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

