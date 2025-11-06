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

