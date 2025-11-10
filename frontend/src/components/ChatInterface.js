import React, { useState, useEffect } from 'react';
import {
  MainContainer,
  ChatContainer,
  MessageList,
  Message,
  MessageInput,
  TypingIndicator,
  ConversationHeader
} from '@chatscope/chat-ui-kit-react';
import '@chatscope/chat-ui-kit-styles/dist/default/styles.min.css';
import '../styles/ChatApp.css';
import { startChatSession, sendChatMessage, generateMarketingPlan } from '../api/chatApi';
import SidebarForm from './SidebarForm';

function ChatInterface({ category, questionNumber = null, initialQuestionText = null, onComplete, onGeneratePlan, onAskDifferentQuestion }) {
  const [messages, setMessages] = useState([]);
  const [isTyping, setIsTyping] = useState(false);
  const [isComplete, setIsComplete] = useState(false);
  const [sessionId, setSessionId] = useState(null);
  const [error, setError] = useState(null);
  const [isGeneratingPlan, setIsGeneratingPlan] = useState(false);
  const [questions, setQuestions] = useState([]);
  const [formAnswers, setFormAnswers] = useState({});
  const [openingDialog, setOpeningDialog] = useState('');
  const [usesTemplate, setUsesTemplate] = useState(false);
  const [antiPatterns, setAntiPatterns] = useState([]);
  const [showHelpModal, setShowHelpModal] = useState(false);

  // Initialize chat session on mount
  useEffect(() => {
    const initializeChat = async () => {
      try {
        setIsTyping(true);
        setError(null);
        
        // Pass question_number if provided (for question-specific templates)
        const response = await startChatSession(category, questionNumber);
        
        if (response.success) {
          setSessionId(response.session_id);
          setUsesTemplate(response.uses_template || false);
          
          // Handle template-based flow
          if (response.uses_template) {
            const templateQuestions = response.questions || [];
            console.log('Template questions received:', templateQuestions.length, templateQuestions);
            setQuestions(templateQuestions);
            setOpeningDialog(response.opening_dialog || '');
            setAntiPatterns(response.anti_patterns || []);
            
            // Add opening dialog as first message
            if (response.opening_dialog) {
              const openingMessage = {
                message: `<strong>Zansei:</strong> ${response.opening_dialog}`,
                sentTime: new Date().toISOString(),
                sender: 'assistant',
                direction: 'incoming',
                position: 'single'
              };
              setMessages([openingMessage]);
            }
          } else {
            // Handle chat_flows-based flow
            // Convert conversation history to Chatscope message format
            const initialMessages = response.conversation.map(msg => ({
              message: msg.role === 'assistant' ? `<strong>Zansei:</strong> ${msg.content}` : msg.content,
              sentTime: msg.timestamp,
              sender: msg.role === 'user' ? 'user' : 'assistant',
              direction: msg.role === 'user' ? 'outgoing' : 'incoming',
              position: 'single'
            }));
            
            setMessages(initialMessages);
          }
        }
      } catch (err) {
        console.error('Failed to start chat session:', err);
        setError(err.message || 'Failed to start chat session. Please try again.');
      } finally {
        setIsTyping(false);
      }
    };

    if (category) {
      initializeChat();
    }
  }, [category, questionNumber]);

  const handleFormAnswersChange = (newAnswers) => {
    setFormAnswers(newAnswers);
  };

  const handleSendMessage = async (innerHtml, textContent, innerText, nodes) => {
    // Allow sending even if message is empty if form answers exist
    if ((!textContent || !textContent.trim()) && Object.keys(formAnswers).length === 0) {
      return;
    }
    
    if (isTyping || !sessionId) return;

    const messageText = textContent ? textContent.trim() : '';
    
    // Only add user message to UI if there's actual text
    if (messageText) {
      const userMessage = {
        message: messageText,
        sentTime: new Date().toISOString(),
        sender: 'user',
        direction: 'outgoing',
        position: 'single'
      };
      setMessages(prev => [...prev, userMessage]);
    }

    setIsTyping(true);
    setError(null);

    try {
      // Send both message and form answers
      const response = await sendChatMessage(sessionId, messageText, formAnswers);
      
      if (response.success) {
        // Add AI response to messages
        const aiMessage = {
          message: `<strong>Zansei:</strong> ${response.ai_response}`,
          sentTime: new Date().toISOString(),
          sender: 'assistant',
          direction: 'incoming',
          position: 'single'
        };
        
        setMessages(prev => [...prev, aiMessage]);
        
        // Check if flow is complete
        if (response.is_complete) {
          setIsComplete(true);
          if (onComplete) {
            onComplete();
          }
        }
      }
    } catch (err) {
      console.error('Failed to send message:', err);
      setError(err.message || 'Failed to send message. Please try again.');
      
      // Remove user message on error (if we added one)
      if (messageText) {
        setMessages(prev => prev.slice(0, -1));
      }
    } finally {
      setIsTyping(false);
    }
  };

  const handleGeneratePlan = async () => {
    if (!sessionId || isGeneratingPlan) return;

    setIsGeneratingPlan(true);
    setError(null);

    try {
      const response = await generateMarketingPlan(sessionId);
      
      if (response.success && onGeneratePlan) {
        onGeneratePlan(response.marketing_plan, response.metadata);
      }
    } catch (err) {
      console.error('Failed to generate plan:', err);
      setError(err.message || 'Failed to generate marketing plan. Please try again.');
    } finally {
      setIsGeneratingPlan(false);
    }
  };

  return (
    <div className="chat-interface-wrapper">
      {/* Main layout: Sidebar + Chat */}
      <div className="chat-layout-container">
        {/* Sidebar Form (only show if using template and has questions) */}
        {usesTemplate && questions.length > 0 && (
          <div className="chat-sidebar">
            <SidebarForm
              questions={questions}
              answers={formAnswers}
              onAnswersChange={handleFormAnswersChange}
              disabled={isTyping || isGeneratingPlan}
            />
          </div>
        )}
        
        {/* Debug info (remove in production) - outside ChatContainer */}
        {usesTemplate && questions.length === 0 && (
          <div className="chat-sidebar" style={{padding: '2rem', background: '#fff3cd', border: '2px solid #ffc107'}}>
            <p><strong>Debug:</strong> Template mode but no questions received.</p>
            <p>usesTemplate: {usesTemplate.toString()}</p>
            <p>questions.length: {questions.length}</p>
            <p>Check browser console for details.</p>
          </div>
        )}

        {/* Chat Interface */}
        <div className={`chat-main ${usesTemplate && questions.length > 0 ? 'with-sidebar' : ''}`}>
          <MainContainer className="chatscope-main-container">
            <ChatContainer className="chatscope-chat-container">
              <ConversationHeader>
                <ConversationHeader.Content userName="Zansei: Marketing Plan Assistant" />
              </ConversationHeader>
              
              <MessageList
                typingIndicator={isTyping ? <TypingIndicator content="Zansei is typing" /> : null}
              >
                {messages.map((msg, index) => (
                  <Message
                    key={index}
                    model={{
                      message: msg.message,
                      sentTime: msg.sentTime,
                      sender: msg.sender,
                      direction: msg.direction,
                      position: msg.position
                    }}
                    render={(message) => {
                      // Render HTML if message contains HTML tags
                      if (message.message && message.message.includes('<strong>')) {
                        return <div dangerouslySetInnerHTML={{ __html: message.message }} />;
                      }
                      return message.message;
                    }}
                  />
                ))}
              </MessageList>

              {!isComplete && (
                <MessageInput
                  placeholder={usesTemplate && questions.length > 0 
                    ? "Type your answer or fill out the form on the left..." 
                    : "Type your answer..."}
                  onSend={handleSendMessage}
                  disabled={isTyping || !sessionId}
                  attachButton={false}
                />
              )}
            </ChatContainer>
            
            {/* Error and actions outside ChatContainer (not allowed as children) */}
            {error && (
              <div className="chat-error-message">
                <p>{error}</p>
              </div>
            )}

            {isComplete && (
              <div className="chat-actions">
                <button
                  onClick={handleGeneratePlan}
                  className="generate-plan-button"
                  disabled={isGeneratingPlan}
                >
                  {isGeneratingPlan ? '⏳ Generating Plan...' : '🚀 Generate Marketing Plan'}
                </button>
              </div>
            )}
          </MainContainer>

          {/* Header Text - Below Chat (in same column) */}
          <div className="chat-interface-header">
            <h2>Let's build your marketing plan</h2>
            <p className="chat-subtitle">Answer a few questions to get started</p>
            {onAskDifferentQuestion && (
              <div className="ask-different-question">
                <span className="ask-different-or">or</span>
                <button 
                  className="ask-different-button"
                  onClick={onAskDifferentQuestion}
                  type="button"
                >
                  Ask A Different Question
                </button>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Help Button - Bottom Right */}
      {antiPatterns.length > 0 && (
        <>
          <button 
            className="chat-help-button"
            onClick={() => setShowHelpModal(true)}
            title="What we'll help you avoid"
          >
            ?
          </button>

          {/* Help Modal */}
          {showHelpModal && (
            <div className="chat-help-modal-overlay" onClick={() => setShowHelpModal(false)}>
              <div className="chat-help-modal" onClick={(e) => e.stopPropagation()}>
                <div className="chat-help-modal-header">
                  <h3>💡 We'll help you avoid:</h3>
                  <button 
                    className="chat-help-modal-close"
                    onClick={() => setShowHelpModal(false)}
                    aria-label="Close"
                  >
                    ×
                  </button>
                </div>
                <div className="chat-help-modal-content">
                  <ul>
                    {antiPatterns.map((pattern, idx) => (
                      <li key={idx}>{pattern}</li>
                    ))}
                  </ul>
                </div>
              </div>
            </div>
          )}
        </>
      )}
    </div>
  );
}

export default ChatInterface;

