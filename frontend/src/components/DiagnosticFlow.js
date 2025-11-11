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
    },
    {
      id: 'competing_with_big_brands',
      icon: '⚔️',
      title: 'Competing With Big Brands',
      description: 'Big competitors are outspending me'
    },
    {
      id: 'sleeping_on_money',
      icon: '💤',
      title: 'I Sleep on a Big Bag of Money',
      description: 'Just experimenting (I sleep like a baby)'
    }
  ];

  const revenueRanges = [
    { id: 'under_10k', label: 'Under $10k/month', description: 'Just getting started', icon: '💰' },
    { id: '10k_to_50k', label: '$10k-50k/month', description: 'Growing steadily', icon: '💰💰' },
    { id: '1k_to_2k', label: '$1k-2k/month', description: 'Small marketing budget', icon: '💰' },
    { id: '2k_to_5k', label: '$2k-5k/month', description: 'Moderate marketing budget', icon: '💰💰' }
  ];

  const triedOptions = [
    { id: 'social_media', label: 'Social Media Marketing', icon: '📱' },
    { id: 'ads', label: 'Paid Advertising (Google/Facebook)', icon: '💰' },
    { id: 'email', label: 'Email Marketing', icon: '📧' },
    { id: 'seo', label: 'SEO / Content Marketing', icon: '🔍' },
    { id: 'influencer', label: 'Influencer Marketing', icon: '⭐' },
    { id: 'events', label: 'Events / Networking', icon: '🎪' },
    { id: 'nothing', label: 'Nothing yet / Just starting', icon: '🌱' }
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
                  {answers.pain_point === option.id && (
                    <div className="checkmark">✓</div>
                  )}
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
                  <div className="option-row-content">
                    <span className="option-icon-small">{option.icon}</span>
                    <div>
                      <div className="option-label">{option.label}</div>
                      <div className="option-description">{option.description}</div>
                    </div>
                  </div>
                  {answers.revenue_range === option.id && (
                    <span className="checkmark">✓</span>
                  )}
                </button>
              ))}
            </div>
            <p className="privacy-note">
              💡 Don't worry - we won't share this with anyone
            </p>
          </div>
        )}

        {/* Step 3: What Tried */}
        {step === 3 && (
          <div className="diagnostic-step step-3 fade-in">
            <button className="back-button" onClick={handleBack}>
              ← Back
            </button>
            <h2>What have you already tried?</h2>
            <p className="step-subtitle">
              Select all that apply (we'll suggest alternatives)
            </p>
            <div className="option-grid-two-col">
              {triedOptions.map(option => (
                <button
                  key={option.id}
                  className={`option-card multi-select ${
                    answers.tried_before.includes(option.id) ? 'selected' : ''
                  }`}
                  onClick={() => handleTriedToggle(option.id)}
                >
                  <div className="option-icon">{option.icon}</div>
                  <div className="option-label">{option.label}</div>
                  {answers.tried_before.includes(option.id) && (
                    <div className="checkmark">✓</div>
                  )}
                </button>
              ))}
            </div>
            <button 
              className="continue-button"
              onClick={handleComplete}
            >
              Find My Perfect Strategy →
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default DiagnosticFlow;

