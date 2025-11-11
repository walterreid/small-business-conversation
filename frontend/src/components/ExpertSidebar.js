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

