// API Configuration
const API_BASE_URL = 'http://localhost:8000'; // Change this to your backend URL

// API Service
const chatAPI = {
    async sendMessage(customer_mail) {
        const response = await fetch(`${API_BASE_URL}/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                customer_mail: customer_mail
            })
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
        }

        return await response.json();
    }
};

// UI Functions
function showLoader(show) {
    const btnText = document.getElementById('btnText');
    const loader = document.getElementById('loader');
    const sendBtn = document.getElementById('sendBtn');
    
    if (show) {
        btnText.style.display = 'none';
        loader.style.display = 'inline-block';
        sendBtn.disabled = true;
    } else {
        btnText.style.display = 'inline-block';
        loader.style.display = 'none';
        sendBtn.disabled = false;
    }
}

function showError(customer_mail) {
    const errorMsg = document.getElementById('errorMsg');
    errorMsg.textContent = `Error: ${customer_mail}`;
    errorMsg.style.display = 'block';
}

function hideError() {
    const errorMsg = document.getElementById('errorMsg');
    errorMsg.style.display = 'none';
}

// Main function to send message
async function sendMessage() {
    const inputEmail = document.getElementById('inputEmail').value;
    const outputEmail = document.getElementById('outputEmail');
    
    // Validation
    if (!inputEmail.trim()) {
        showError('Please enter an email message');
        return;
    }
    
    // Reset UI
    hideError();
    outputEmail.value = '';
    showLoader(true);
    
    try {
        // Call API
        const data = await chatAPI.sendMessage(inputEmail);
        
        // Display response
        outputEmail.value = data.response || 'No response received';
        
    } catch (error) {
        console.error('Error:', error);
        showError(error.message || 'Failed to get response from backend');
    } finally {
        showLoader(false);
    }
}

// Add keyboard support (Enter to send, Shift+Enter for new line)
document.getElementById('inputEmail').addEventListener('keydown', function(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

// Initialize
console.log('Email Chat Assistant initialized');
console.log('API URL:', API_BASE_URL);