const API_BASE_URL = 'http://localhost:8080';

async function uploadDocument() {
    const fileInput = document.getElementById('uploadFile');
    const file = fileInput.files[0];
    const formData = new FormData();
    formData.append('file', file);

    const spinner = document.getElementById('spinner');
    spinner.style.display = 'block'; // Show spinner

    const response = await fetch(`${API_BASE_URL}/api/upload`, {
        method: 'POST',
        body: formData
    });

    spinner.style.display = 'none'; // Hide spinner

    if (response.ok) {
        const data = await response.json();
        alert(`File uploaded successfully! Saved at: ${data.location}`);
    } else {
        alert('File upload failed.');
    }
}

async function sendMessage() {
    const inputMessage = document.getElementById('inputMessage');
    const message = inputMessage.value;

    const chatbox = document.getElementById('chatbox');
    const chatSpinner = document.getElementById('chat-spinner');
    
    // Add user message to chatbox
    chatbox.innerHTML += `<div><strong>You:</strong> ${message}</div>`;
    
    // Clear and disable the input field, show spinner
    inputMessage.value = '';
    inputMessage.disabled = true;
    chatSpinner.style.display = 'block'; // Show spinner

    const response = await fetch(`${API_BASE_URL}/api/chat`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message })
    });

    chatSpinner.style.display = 'none'; // Hide spinner
    inputMessage.disabled = false;

    if (response.ok) {
        const data = await response.json();
        chatbox.innerHTML += `<div><strong>LLM:</strong> ${data.response}</div>`;
    } else {
        alert('Message sending failed.');
    }
}
