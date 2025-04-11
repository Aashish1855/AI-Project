from flask import Flask, render_template, request, jsonify
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import json
import re
from datetime import datetime

app = Flask(__name__)

tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-small")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-small")

with open("data/products.json", "r") as f:
    product_data = json.load(f)


user_histories = {}

def preprocess_text(text):
    return re.sub(r"[^a-zA-Z0-9 ]", "", text.lower())

def get_ai_reply(user_input, user_id="user"):
    if user_id not in user_histories:
        user_histories[user_id] = None

    input_ids = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors='pt')
    chat_history = user_histories[user_id]

    bot_input_ids = torch.cat([chat_history, input_ids], dim=-1) if chat_history is not None else input_ids
    output = model.generate(bot_input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)

    user_histories[user_id] = output
    response = tokenizer.decode(output[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)
    return response

def match_product_keywords(message):
    message = preprocess_text(message)
    matched = []
    for product in product_data:
        if any(keyword in message for keyword in product["keywords"]):
            matched.append(product)
    return matched

def time_based_greeting():
    hour = datetime.now().hour
    if hour < 12:
        return "Good morning! How can I help you today?"
    elif hour < 18:
        return "Good afternoon! What are you looking for today?"
    else:
        return "Good evening! Need help finding the right product?"

@app.route('/')
def home():
    return render_template("chat.html")

@app.route('/chat', methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")
    user_id = data.get("user_id", "default_user")

    if user_message.strip().lower() in ["hi", "hello"]:
        bot_reply = time_based_greeting()
    else:
        matched_products = match_product_keywords(user_message)
        if matched_products:
            product = matched_products[0]
            bot_reply = f"{product['name']} - {product['description']}. Price: {product.get('price', 'N/A')}."
        else:
            bot_reply = get_ai_reply(user_message, user_id)

    return jsonify({"reply": bot_reply})

if __name__ == '__main__':
    app.run(debug=True)