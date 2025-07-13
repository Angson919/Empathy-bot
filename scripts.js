const chatBox = document.getElementById('chatBox');
const userInput = document.getElementById('userInput');
const sendBtn = document.getElementById('sendBtn');
const typingIndicator = document.getElementById('typingIndicator');
const emotionColors = {
    sadness: '#3498db',
    joy: '#f1c40f',
    anger: '#e74c3c',
    fear: '#9b59b6',
    surprise: '#e67e22',
    love: '#e84393',
    neutral: '#777'
};

sendBtn.addEventListener('click', sendMessage);
userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendMessage();
});

document.getElementById('darkModeToggle').addEventListener('click', toggleDarkMode);

window.addEventListener('DOMContentLoaded', () => {
    const darkModeBtn = document.getElementById('darkModeToggle');
    const icon = darkModeBtn.querySelector('i');
    const isDarkMode = localStorage.getItem('darkMode') === 'true';
    if (isDarkMode) {
        document.body.classList.add('dark');
        icon.className = 'fas fa-sun';
    } else {
        icon.className = 'fas fa-moon';
    }
});

function toggleDarkMode() {
    document.body.classList.toggle('dark');
    const isDark = document.body.classList.contains('dark');
    localStorage.setItem('darkMode', isDark);
    const icon = document.getElementById('darkModeToggle').querySelector('i');
    icon.className = isDark ? 'fas fa-sun' : 'fas fa-moon';
}

function addMessage(text, sender, emotion = null) {
    const messageDiv = document.createElement('div');
    messageDiv.classList.add(`${sender}-message`);

    if (sender === 'bot') {
        messageDiv.innerHTML = `
            <p>${text}</p>
            ${emotion ? `<div class="emotion-indicator" style="color: ${emotionColors[emotion.toLowerCase()] || '#777'}">
                <i class='fas fa-heart'></i> ${emotion}
            </div>` : ''}
        `;
    } else {
        messageDiv.textContent = text;
    }

    chatBox.appendChild(messageDiv);
    chatBox.scrollTo({ top: chatBox.scrollHeight, behavior: 'smooth' });
}

async function sendMessage() {
    const message = userInput.value.trim();
    if (!message) return;

    addMessage(message, 'user');
    userInput.value = '';
    typingIndicator.style.display = 'block';
    chatBox.scrollTo({ top: chatBox.scrollHeight, behavior: 'smooth' });

    try {
        const response = await fetch('http://localhost:8000/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                text: message,
                user_id: 'current_user'
            })
        });

        const data = await response.json();
        typingIndicator.style.display = 'none';

        const reply = data.reply || data.text || "I'm here for you.";
        const emotion = data.emotion || 'neutral';
        addMessage(reply, 'bot', emotion);

    } catch (error) {
        typingIndicator.style.display = 'none';
        addMessage("Sorry, I'm having trouble connecting to the server.", 'bot');
        console.error('Error:', error);
    }
}
