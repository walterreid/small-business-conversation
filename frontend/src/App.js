import React, { useState } from 'react';
import CategorySelector from './components/CategorySelector';
import ChatInterface from './components/ChatInterface';
import MarketingPlanView from './components/MarketingPlanView';
import './App.css';

function App() {
  // New 3-step flow state
  const [step, setStep] = useState(1); // 1: Category Selection, 2: Chat, 3: Marketing Plan
  const [selectedCategory, setSelectedCategory] = useState(null);
  const [marketingPlan, setMarketingPlan] = useState(null);
  const [planMetadata, setPlanMetadata] = useState(null);

  // Handle category selection
  const handleCategorySelect = (category) => {
    setSelectedCategory(category);
    setStep(2); // Move to chat interface
  };

  // Handle chat completion (when all questions answered)
  const handleChatComplete = () => {
    // Chat is complete, user can now generate plan
    // This is handled by the generate button in ChatInterface
  };

  // Handle marketing plan generation
  const handleGeneratePlan = (plan, metadata) => {
    setMarketingPlan(plan);
    setPlanMetadata(metadata);
    setStep(3); // Move to marketing plan view
  };

  // Handle start over
  const handleStartOver = () => {
    setStep(1);
    setSelectedCategory(null);
    setMarketingPlan(null);
    setPlanMetadata(null);
  };

  // Render based on current step
  return (
    <div className="App">
      {step === 1 && (
        <div className="page-enter">
          <CategorySelector onSelectCategory={handleCategorySelect} />
        </div>
      )}
      
      {step === 2 && selectedCategory && (
        <div className="page-enter">
          <ChatInterface
            category={selectedCategory}
            onComplete={handleChatComplete}
            onGeneratePlan={handleGeneratePlan}
          />
        </div>
      )}
      
      {step === 3 && marketingPlan && (
        <div className="page-enter">
          <MarketingPlanView
            marketingPlan={marketingPlan}
            metadata={planMetadata}
            onStartOver={handleStartOver}
          />
        </div>
      )}
    </div>
  );
}

export default App;
