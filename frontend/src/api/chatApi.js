/**
 * Chat API client for marketing plan generator backend
 */

// Use proxy in development, or explicit URL in production
const API_BASE_URL = process.env.REACT_APP_API_URL || '';

/**
 * Start a new chat session for a business category
 * @param {string} category - Business category (restaurant, retail_store, etc.)
 * @returns {Promise<Object>} API response with session_id and first_question
 */
export async function startChatSession(category) {
  try {
    // Use proxy in development (empty string uses package.json proxy)
    // Or use full URL if REACT_APP_API_URL is set
    const url = API_BASE_URL ? `${API_BASE_URL}/api/chat/start` : '/api/chat/start';
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        category: category
      })
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.error || `HTTP ${response.status}: ${response.statusText}`);
    }

    const data = await response.json();
    
    if (!data.success) {
      throw new Error(data.error || 'Failed to start chat session');
    }

    return data;
  } catch (error) {
    // Re-throw with more context if it's a network error
    if (error.name === 'TypeError' && error.message.includes('fetch')) {
      throw new Error('Unable to connect to the server. Please check if the backend is running.');
    }
    throw error;
  }
}

/**
 * Send a message in an ongoing chat session
 * @param {string} sessionId - Session ID from startChatSession
 * @param {string} message - User's message/answer (optional if form_answers provided)
 * @param {Object} formAnswers - Form answers from sidebar (optional)
 * @returns {Promise<Object>} API response with ai_response and is_complete
 */
export async function sendChatMessage(sessionId, message = '', formAnswers = {}) {
  try {
    const url = API_BASE_URL ? `${API_BASE_URL}/api/chat/message` : '/api/chat/message';
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        session_id: sessionId,
        user_message: message,
        form_answers: formAnswers
      })
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.error || `HTTP ${response.status}: ${response.statusText}`);
    }

    const data = await response.json();
    
    if (!data.success) {
      throw new Error(data.error || 'Failed to send message');
    }

    return data;
  } catch (error) {
    if (error.name === 'TypeError' && error.message.includes('fetch')) {
      throw new Error('Unable to connect to the server. Please check if the backend is running.');
    }
    throw error;
  }
}

/**
 * Generate marketing plan from completed chat session
 * @param {string} sessionId - Session ID
 * @returns {Promise<Object>} API response with marketing_plan
 */
export async function generateMarketingPlan(sessionId) {
  try {
    const url = API_BASE_URL ? `${API_BASE_URL}/api/chat/generate-plan` : '/api/chat/generate-plan';
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        session_id: sessionId
      })
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.error || `HTTP ${response.status}: ${response.statusText}`);
    }

    const data = await response.json();
    
    if (!data.success) {
      throw new Error(data.error || 'Failed to generate marketing plan');
    }

    return data;
  } catch (error) {
    if (error.name === 'TypeError' && error.message.includes('fetch')) {
      throw new Error('Unable to connect to the server. Please check if the backend is running.');
    }
    throw error;
  }
}

/**
 * Get chat session history
 * @param {string} sessionId - Session ID
 * @returns {Promise<Object>} API response with session data
 */
export async function getChatSession(sessionId) {
  try {
    const url = API_BASE_URL ? `${API_BASE_URL}/api/chat/session/${sessionId}` : `/api/chat/session/${sessionId}`;
    const response = await fetch(url);

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.error || `HTTP ${response.status}: ${response.statusText}`);
    }

    const data = await response.json();
    
    if (!data.success) {
      throw new Error(data.error || 'Failed to get session');
    }

    return data;
  } catch (error) {
    if (error.name === 'TypeError' && error.message.includes('fetch')) {
      throw new Error('Unable to connect to the server. Please check if the backend is running.');
    }
    throw error;
  }
}

