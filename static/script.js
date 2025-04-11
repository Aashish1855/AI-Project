async function sendMessage() {
    const userInput = document.getElementById('user-input');
    const chatBox = document.getElementById('chat-box');
    const message = userInput.value.trim();
  
    if (!message) return;
  

    const userMsg = document.createElement('div');
    userMsg.className = 'message user-message';
    userMsg.textContent = message;
    chatBox.appendChild(userMsg);
  

    userInput.value = '';
  

    chatBox.scrollTop = chatBox.scrollHeight;
  

    try {
      const response = await fetch('/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: message })
      });
  
      const data = await response.json();
  

      const botMsg = document.createElement('div');
      botMsg.className = 'message bot-message';
      botMsg.textContent = data.reply;
      chatBox.appendChild(botMsg);
  
      chatBox.scrollTop = chatBox.scrollHeight;
    } catch (error) {
      console.error('Error:', error);
    }
  }
  