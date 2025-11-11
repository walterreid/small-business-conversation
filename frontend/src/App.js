import React, { useState } from 'react';
import DiagnosticFlow from './components/DiagnosticFlow';
import MatchedQuestions from './components/MatchedQuestions';
import CategorySelector from './components/CategorySelector';
import ChatInterface from './components/ChatInterface';
import MarketingPlanView from './components/MarketingPlanView';
import { runDiagnostic } from './api/chatApi';
import './App.css';

function App() {
  // Flow state: 'diagnostic' | 'matched' | 'browse' | 'chat' | 'plan'
  const [step, setStep] = useState('diagnostic'); // Start with diagnostic
  const [diagnosticAnswers, setDiagnosticAnswers] = useState(null);
  const [matchedQuestions, setMatchedQuestions] = useState(null);
  const [matchReasoning, setMatchReasoning] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState(null);
  const [selectedQuestionNumber, setSelectedQuestionNumber] = useState(null);
  const [selectedQuestionText, setSelectedQuestionText] = useState(null);
  const [marketingPlan, setMarketingPlan] = useState(null);
  const [planMetadata, setPlanMetadata] = useState(null);

  // Handle diagnostic completion
  const handleDiagnosticComplete = async (answers) => {
    setDiagnosticAnswers(answers);
    
    try {
      const result = await runDiagnostic(
        answers.pain_point,
        answers.revenue_range,
        answers.tried_before
      );
      
      if (result.success) {
        setMatchedQuestions(result.matched_questions);
        setMatchReasoning(result.overall_reasoning || []);
        setStep('matched');
      }
    } catch (error) {
      console.error('Diagnostic error:', error);
      // Fallback to browse all
      setStep('browse');
    }
  };

  // Handle skip diagnostic
  const handleSkipDiagnostic = () => {
    setStep('browse');
  };

  // Handle selecting a matched question
  const handleSelectMatchedQuestion = (category, questionNumber, questionText) => {
    setSelectedCategory(category);
    setSelectedQuestionNumber(questionNumber);
    setSelectedQuestionText(questionText);
    setStep('chat');
  };

  // Handle browse all
  const handleBrowseAll = () => {
    setStep('browse');
  };

  // Handle category selection (legacy - for backward compatibility)
  const handleCategorySelect = (category) => {
    setSelectedCategory(category);
    setSelectedQuestionNumber(null);
    setStep('chat'); // Move to chat interface
  };

  // Handle question selection from MarketingGoalSelector
  const handleQuestionSelect = (category, questionNumber, questionText, templateData) => {
    setSelectedCategory(category);
    setSelectedQuestionNumber(questionNumber);
    setSelectedQuestionText(questionText);
    setStep('chat'); // Move to chat interface
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
    setStep('plan'); // Move to marketing plan view
  };

  // Handle start over
  const handleStartOver = () => {
    setStep('diagnostic');
    setDiagnosticAnswers(null);
    setMatchedQuestions(null);
    setMatchReasoning([]);
    setSelectedCategory(null);
    setSelectedQuestionNumber(null);
    setSelectedQuestionText(null);
    setMarketingPlan(null);
    setPlanMetadata(null);
  };

  // Handle asking a different question (go back to question selection)
  const handleAskDifferentQuestion = () => {
    setStep('browse');
    // Keep category/question state so user can see what they had selected
  };

  // Render based on current step
  return (
    <div className="App">
      {step === 'diagnostic' && (
        <DiagnosticFlow
          onComplete={handleDiagnosticComplete}
          onSkip={handleSkipDiagnostic}
        />
      )}

      {step === 'matched' && (
        <MatchedQuestions
          matchedQuestions={matchedQuestions}
          reasoning={matchReasoning}
          onSelectQuestion={handleSelectMatchedQuestion}
          onBrowseAll={handleBrowseAll}
        />
      )}

      {step === 'browse' && (
        <div className="page-enter">
          <CategorySelector 
            onSelectCategory={handleCategorySelect}
            onSelectQuestion={handleQuestionSelect}
          />
        </div>
      )}
      
      {step === 'chat' && selectedCategory && (
        <div className="page-enter">
          <ChatInterface
            category={selectedCategory}
            questionNumber={selectedQuestionNumber}
            initialQuestionText={selectedQuestionText}
            diagnosticContext={diagnosticAnswers}
            onComplete={handleChatComplete}
            onGeneratePlan={handleGeneratePlan}
            onAskDifferentQuestion={handleAskDifferentQuestion}
          />
        </div>
      )}
      
      {step === 'plan' && marketingPlan && (
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
