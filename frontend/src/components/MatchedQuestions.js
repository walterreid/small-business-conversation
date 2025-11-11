import React from 'react';
import '../styles/MatchedQuestions.css';

const MatchedQuestions = ({ matchedQuestions, reasoning, onSelectQuestion, onBrowseAll }) => {
  if (!matchedQuestions || matchedQuestions.length === 0) {
    return (
      <div className="matched-questions">
        <div className="matched-container">
          <div className="no-matches">
            <h2>No matches found</h2>
            <p>Let's browse all questions instead.</p>
            <button className="browse-all-btn" onClick={onBrowseAll}>
              Browse All Questions →
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
      <div className="matched-questions">
      <div className="matched-container">
        <div className="matched-header">
          <h2>✨ Perfect! Here are your top 3 questions</h2>
        </div>

        <div className="questions-grid">
          {matchedQuestions.map((match, idx) => (
            <div 
              key={idx}
              className={`matched-question-card ${idx === 0 ? 'best-match' : ''}`}
            >
              {idx === 0 && (
                <div className="match-rank">#1 Best Match</div>
              )}
              {idx === 1 && (
                <div className="match-rank rank-2">#2 Good Match</div>
              )}
              {idx === 2 && (
                <div className="match-rank rank-3">#3 Alternative</div>
              )}
              
              <div className="question-text">{match.question_text}</div>
              
              <div className="why-fits">
                <div className="why-fits-title">🎯 Why this fits you:</div>
                <div className="why-fits-text">{match.why_this_fits}</div>
              </div>

              {match.unique_value && (
                <div className="unique-value-preview">
                  <div className="unique-value-title">✨ What makes this special:</div>
                  <div className="unique-value-text">{match.unique_value}</div>
                </div>
              )}

              <button 
                className="select-question-btn"
                onClick={() => onSelectQuestion(match.category, match.question_number, match.question_text)}
              >
                Start Conversation →
              </button>
            </div>
          ))}
        </div>

        {reasoning && reasoning.length > 0 && (
          <div className="reasoning-box-bottom">
            <div className="reasoning-title">🎯 Why we matched you to these:</div>
            <ul className="reasoning-list">
              {reasoning.map((reason, idx) => (
                <li key={idx}>{reason}</li>
              ))}
            </ul>
          </div>
        )}

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

