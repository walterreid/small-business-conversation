import React, { useState } from 'react';
import CategorySelector from './components/CategorySelector';
import ChatInterface from './components/ChatInterface';
import MarketingPlanView from './components/MarketingPlanView';
import './App.css';

function App() {
  // New 3-step flow state
  const [step, setStep] = useState(1); // 1: Category Selection, 2: Chat, 3: Marketing Plan
  const [selectedCategory, setSelectedCategory] = useState(null);
  const [selectedQuestionNumber, setSelectedQuestionNumber] = useState(null);
  const [selectedQuestionText, setSelectedQuestionText] = useState(null);
  const [marketingPlan, setMarketingPlan] = useState(null);
  const [planMetadata, setPlanMetadata] = useState(null);

  // Handle category selection (legacy - for backward compatibility)
  const handleCategorySelect = (category) => {
    setSelectedCategory(category);
    setSelectedQuestionNumber(null);
    setStep(2); // Move to chat interface
  };

  // Handle question selection from MarketingGoalSelector
  const handleQuestionSelect = (category, questionNumber, questionText, templateData) => {
    setSelectedCategory(category);
    setSelectedQuestionNumber(questionNumber);
    setSelectedQuestionText(questionText);
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
    setSelectedQuestionNumber(null);
    setSelectedQuestionText(null);
    setMarketingPlan(null);
    setPlanMetadata(null);
  };

  // Handle asking a different question (go back to question selection)
  const handleAskDifferentQuestion = () => {
    setStep(1);
    // Keep category/question state so user can see what they had selected
  };

  // Render based on current step
  return (
    <div className="App">
      {step === 1 && (
        <div className="page-enter">
          <CategorySelector 
            onSelectCategory={handleCategorySelect}
            onSelectQuestion={handleQuestionSelect}
          />
        </div>
      )}
      
      {step === 2 && selectedCategory && (
        <div className="page-enter">
          <ChatInterface
            category={selectedCategory}
            questionNumber={selectedQuestionNumber}
            initialQuestionText={selectedQuestionText}
            onComplete={handleChatComplete}
            onGeneratePlan={handleGeneratePlan}
            onAskDifferentQuestion={handleAskDifferentQuestion}
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
