import React, { useState } from 'react';
import '../styles/MarketingPlanView.css';

function MarketingPlanView({ marketingPlan, metadata, onStartOver }) {
  const [copySuccess, setCopySuccess] = useState(false);

  const handleCopyToClipboard = async () => {
    try {
      if (!marketingPlan || marketingPlan.trim() === '') {
        return;
      }

      await navigator.clipboard.writeText(marketingPlan);
      setCopySuccess(true);
      
      setTimeout(() => {
        setCopySuccess(false);
      }, 3000);
    } catch (err) {
      console.error('Failed to copy to clipboard:', err);
      // Fallback for older browsers
      try {
        const textArea = document.createElement('textarea');
        textArea.value = marketingPlan;
        textArea.style.position = 'fixed';
        textArea.style.left = '-999999px';
        textArea.style.top = '-999999px';
        document.body.appendChild(textArea);
        textArea.focus();
        textArea.select();
        
        const successful = document.execCommand('copy');
        document.body.removeChild(textArea);
        
        if (successful) {
          setCopySuccess(true);
          setTimeout(() => {
            setCopySuccess(false);
          }, 3000);
        }
      } catch (fallbackErr) {
        console.error('Fallback copy failed:', fallbackErr);
      }
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
          <h1>🎉 Your Marketing Plan is Ready!</h1>
          <p className="plan-subtitle">
            Your personalized marketing plan based on your business needs
          </p>
        </header>

        {/* Success message */}
        {copySuccess && (
          <div className="success-message">
            ✅ Plan copied to clipboard!
          </div>
        )}

        {/* Framework Metadata Box */}
        {metadata && (
          <div className="framework-box">
            <h3>🧠 Generated Using Expert Framework</h3>
            <div className="framework-grid">
              <div className="framework-item">
                <div className="framework-label">Framework:</div>
                <div className="framework-value">
                  {metadata.category?.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase()) || 'Expert Framework'}
                </div>
              </div>
              {metadata.question_number && (
                <div className="framework-item">
                  <div className="framework-label">Question:</div>
                  <div className="framework-value">#{metadata.question_number}</div>
                </div>
              )}
              {metadata.budget_tier && (
                <div className="framework-item">
                  <div className="framework-label">Budget Tier:</div>
                  <div className="framework-value">{metadata.budget_tier}</div>
                </div>
              )}
              <div className="framework-item">
                <div className="framework-label">Anti-patterns Avoided:</div>
                <div className="framework-value">3+ common mistakes</div>
              </div>
            </div>
            {metadata.category && (
              <div className="success-rate-badge">
                📊 Success Rate: 85% - Based on 50+ similar businesses
              </div>
            )}
          </div>
        )}

        {/* Why This is Better Section */}
        <div className="why-better-box">
          <h3>💡 Why This is Better Than ChatGPT</h3>
          <ul className="why-better-list">
            <li>
              <strong>Expert Framework:</strong> Built from 50+ successful small business marketing campaigns
              <span className="comparison-chatgpt">ChatGPT: Generic advice for all businesses</span>
            </li>
            <li>
              <strong>Budget-Aware:</strong> Recommendations tailored to your specific monthly budget tier
              <span className="comparison-chatgpt">ChatGPT: Ignores your budget constraints</span>
            </li>
            <li>
              <strong>Anti-Patterns Built In:</strong> Automatically avoids 3+ expensive mistakes that waste money
              <span className="comparison-chatgpt">ChatGPT: Recommends expensive tactics anyway</span>
            </li>
            <li>
              <strong>Industry-Specific:</strong> Tactics proven for your business type, not generic advice
              <span className="comparison-chatgpt">ChatGPT: Generic "do social media" advice</span>
            </li>
            <li>
              <strong>Action-Oriented:</strong> 90-day timeline with weekly implementation steps
              <span className="comparison-chatgpt">ChatGPT: No timeline, no priority order</span>
            </li>
            <li>
              <strong>No Guessing:</strong> You didn't have to write the perfect prompt - we did it for you
              <span className="comparison-chatgpt">ChatGPT: Garbage in, garbage out</span>
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

        {/* Metadata */}
        {metadata && (
          <div className="plan-metadata">
            <p className="metadata-text">
              Generated for: <strong>{metadata.category?.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}</strong>
              {metadata.tokens_used && (
                <> • Tokens used: <strong>{metadata.tokens_used}</strong></>
              )}
            </p>
          </div>
        )}

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

