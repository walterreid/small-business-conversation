/**
 * Chat API client for marketing plan generator backend
 */

// Use proxy in development, or explicit URL in production
const API_BASE_URL = process.env.REACT_APP_API_URL || '';

/**
 * Start a new chat session for a business category or marketing goal question
 * @param {string} category - Business category or marketing goal (restaurant, increase_sales, etc.)
 * @param {number|null} questionNumber - Optional question number (1-5) for question-specific templates
 * @returns {Promise<Object>} API response with session_id and first_question
 */
export async function startChatSession(category, questionNumber = null) {
  try {
    // Use proxy in development (empty string uses package.json proxy)
    // Or use full URL if REACT_APP_API_URL is set
    const url = API_BASE_URL ? `${API_BASE_URL}/api/chat/start` : '/api/chat/start';
    const requestBody = {
      category: category
    };
    
    // Add question_number if provided
    if (questionNumber !== null && questionNumber !== undefined) {
      requestBody.question_number = questionNumber;
    }
    
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(requestBody)
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

/**
 * Get all marketing goal categories with their questions
 * @returns {Promise<Object>} API response with goals data
 */
export async function getMarketingGoals() {
  try {
    const url = API_BASE_URL ? `${API_BASE_URL}/api/marketing-goals` : '/api/marketing-goals';
    const response = await fetch(url);

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.error || `HTTP ${response.status}: ${response.statusText}`);
    }

    const data = await response.json();
    
    if (!data.success) {
      throw new Error(data.error || 'Failed to load marketing goals');
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
 * Get full question template for a specific marketing goal question
 * @param {string} category - Marketing goal category
 * @param {number} questionNumber - Question number (1-5)
 * @returns {Promise<Object>} API response with template data
 */
export async function getQuestionTemplate(category, questionNumber) {
  try {
    const url = API_BASE_URL 
      ? `${API_BASE_URL}/api/marketing-goals/${category}/question/${questionNumber}`
      : `/api/marketing-goals/${category}/question/${questionNumber}`;
    
    const response = await fetch(url);

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.error || `HTTP ${response.status}: ${response.statusText}`);
    }

    const data = await response.json();
    
    if (!data.success) {
      throw new Error(data.error || 'Failed to load question template');
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
 * Run diagnostic to match user to best questions
 * @param {string} painPoint - User's main pain point (not_enough_customers, no_visibility, etc.)
 * @param {string} revenueRange - Monthly revenue range (under_10k, 10k_to_50k, etc.)
 * @param {Array<string>} triedBefore - List of what they've already tried
 * @returns {Promise<Object>} API response with matched_questions and overall_reasoning
 */
export async function runDiagnostic(painPoint, revenueRange, triedBefore = []) {
  try {
    const url = API_BASE_URL ? `${API_BASE_URL}/api/diagnostic` : '/api/diagnostic';
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        pain_point: painPoint,
        revenue_range: revenueRange,
        tried_before: triedBefore
      })
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.error || `HTTP ${response.status}`);
    }

    const data = await response.json();
    
    if (!data.success) {
      throw new Error(data.error || 'Failed to run diagnostic');
    }

    return data;
  } catch (error) {
    if (error.name === 'TypeError' && error.message.includes('fetch')) {
      throw new Error('Unable to connect to the server.');
    }
    throw error;
  }
}

