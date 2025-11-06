/**
 * API client for meta-prompt generator backend
 */

const API_BASE_URL = process.env.REACT_APP_API_URL || '';

/**
 * Generate a custom prompt template
 * @param {string} userDomain - What the user needs help with
 * @param {string} userFraming - Optional additional context
 * @returns {Promise<Object>} API response with template data
 */
export async function generateTemplate(userDomain, userFraming = '') {
  try {
    const response = await fetch(`${API_BASE_URL}/api/generate-template`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        userDomain: userDomain.trim(),
        userFraming: userFraming.trim()
      })
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.error || `HTTP ${response.status}: ${response.statusText}`);
    }

    const data = await response.json();
    
    if (!data.success) {
      throw new Error(data.error || 'Failed to generate template');
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
 * Health check endpoint
 * @returns {Promise<Object>} Health status
 */
export async function healthCheck() {
  try {
    const response = await fetch(`${API_BASE_URL}/health`);
    
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }

    return await response.json();
  } catch (error) {
    if (error.name === 'TypeError' && error.message.includes('fetch')) {
      throw new Error('Unable to connect to the server. Please check if the backend is running.');
    }
    throw error;
  }
}
