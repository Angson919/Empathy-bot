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
    love: '#e84393'
};

sendBtn.addEventListener('click', sendMessage);
userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendMessage();
});

document.getElementById('darkModeToggle').addEventListener('click', toggleDarkMode);

// Initialize dark mode state from localStorage on page load
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
