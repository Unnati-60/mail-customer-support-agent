/**
 * API Service for Email Chat Assistant
 * Handles all backend API communications
 */

class ChatAPIService {
    constructor(baseURL = 'http://localhost:8000') {
        this.baseURL = baseURL;
    }

    /**
     * Send a chat message to the backend
     * @param {string} message - The email message to send
     * @returns {Promise<Object>} - The API response
     */
    async sendMessage(message) {
        try {
            const response = await fetch(`${this.baseURL}/chat`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: message
                })
            });

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    }

    /**
     * Health check endpoint (if your backend supports it)
     * @returns {Promise<Object>}
     */
    async healthCheck() {
        try {
            const response = await fetch(`${this.baseURL}/health`);
            return await response.json();
        } catch (error) {
            console.error('Health check failed:', error);
            throw error;
        }
    }

    /**
     * Update the base URL
     * @param {string} newBaseURL
     */
    setBaseURL(newBaseURL) {
        this.baseURL = newBaseURL;
    }
}

// Export for use in other files
// For ES6 modules: export default ChatAPIService;
// For CommonJS: module.exports = ChatAPIService;

// For browser direct use:
const chatAPIService = new ChatAPIService();

// If using this file, you can simplify app.js to:
// const data = await chatAPIService.sendMessage(inputEmail);