import React from 'react';
import MarketingGoalSelector from './MarketingGoalSelector';
import '../styles/CategorySelector.css';

/**
 * CategorySelector Component
 * 
 * Now only shows Marketing Goals (Business Type section removed)
 * Uses MarketingGoalSelector to display expandable goal categories with questions
 */
function CategorySelector({ onSelectCategory, onSelectQuestion }) {
  // If onSelectQuestion is provided, use MarketingGoalSelector
  // Otherwise, fall back to simple category selection (for backward compatibility)
  if (onSelectQuestion) {
    return (
      <div className="category-selector-page">
        <div className="category-container">
          <header className="category-header">
            <h1>What's your marketing goal?</h1>
            <p className="category-subtitle">
              Choose a marketing goal to see specific questions and get personalized guidance
            </p>
          </header>
          <MarketingGoalSelector onSelectQuestion={onSelectQuestion} />
        </div>
      </div>
    );
  }

  // Legacy mode: simple category selection (if needed for backward compatibility)
  return (
    <div className="category-selector-page">
      <div className="category-container">
        <header className="category-header">
          <h1>What's your marketing goal?</h1>
          <p className="category-subtitle">
            Choose a marketing goal to get started
          </p>
        </header>
        <div className="category-grid">
          <p>Please use MarketingGoalSelector component for full functionality.</p>
        </div>
      </div>
    </div>
  );
}

export default CategorySelector;

