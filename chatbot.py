from flask import Flask, render_template, request, jsonify
app = Flask(__name__)
def chatbot_response(message):
    responses = {
        "hi": "Hello! How can I help you today?",
        "how are you": "I'm just a bot, but I'm doing great! How about you?",
        "recommend a lipstick": "Sure! You might love our Matte Red Lipstick. It’s long-lasting and vibrant!",
        "bye": "Goodbye! Have a great day!"
    }
    return responses.get(message.lower(), "Sorry, I didn't understand that. Can you rephrase?")

@app.route('/')
def home():
    return render_template('chat.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get("message")
    bot_reply = chatbot_response(user_message)
    return jsonify({"reply": bot_reply})

if __name__ == '__main__':
    app.run(debug=True)
