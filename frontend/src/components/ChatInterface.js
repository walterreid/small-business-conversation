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

function ChatInterface({ category, onComplete, onGeneratePlan }) {
  const [messages, setMessages] = useState([]);
  const [isTyping, setIsTyping] = useState(false);
  const [isComplete, setIsComplete] = useState(false);
  const [sessionId, setSessionId] = useState(null);
  const [error, setError] = useState(null);
  const [isGeneratingPlan, setIsGeneratingPlan] = useState(false);

  // Initialize chat session on mount
  useEffect(() => {
    const initializeChat = async () => {
      try {
        setIsTyping(true);
        setError(null);
        
        const response = await startChatSession(category);
        
        if (response.success) {
          setSessionId(response.session_id);
          
          // Convert conversation history to Chatscope message format
          const initialMessages = response.conversation.map(msg => ({
            message: msg.content,
            sentTime: msg.timestamp,
            sender: msg.role === 'user' ? 'user' : 'assistant',
            direction: msg.role === 'user' ? 'outgoing' : 'incoming',
            position: 'single'
          }));
          
          setMessages(initialMessages);
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
  }, [category]);

  const handleSendMessage = async (innerHtml, textContent, innerText, nodes) => {
    if (!textContent.trim() || isTyping || !sessionId) return;

    const userMessage = {
      message: textContent.trim(),
      sentTime: new Date().toISOString(),
      sender: 'user',
      direction: 'outgoing',
      position: 'single'
    };

    setMessages(prev => [...prev, userMessage]);
    setIsTyping(true);
    setError(null);

    try {
      const response = await sendChatMessage(sessionId, textContent.trim());
      
      if (response.success) {
        // Add AI response to messages
        const aiMessage = {
          message: response.ai_response,
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
      
      // Remove user message on error
      setMessages(prev => prev.slice(0, -1));
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
      <div className="chat-interface-header">
        <h2>Let's build your marketing plan</h2>
        <p className="chat-subtitle">Answer a few questions to get started</p>
      </div>
      
      <MainContainer className="chatscope-main-container">
        <ChatContainer className="chatscope-chat-container">
          <ConversationHeader>
            <ConversationHeader.Content userName="Marketing Plan Assistant" />
          </ConversationHeader>
          
          <MessageList
            typingIndicator={isTyping ? <TypingIndicator content="AI is typing" /> : null}
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
              />
            ))}
          </MessageList>

          {error && (
            <div className="chat-error-message">
              <p>{error}</p>
            </div>
          )}

          {isComplete ? (
            <div className="chat-actions">
              <button
                onClick={handleGeneratePlan}
                className="generate-plan-button"
                disabled={isGeneratingPlan}
              >
                {isGeneratingPlan ? '⏳ Generating Plan...' : '🚀 Generate Marketing Plan'}
              </button>
            </div>
          ) : (
            <MessageInput
              placeholder="Type your answer..."
              onSend={handleSendMessage}
              disabled={isTyping || !sessionId}
              attachButton={false}
            />
          )}
        </ChatContainer>
      </MainContainer>
    </div>
  );
}

export default ChatInterface;

