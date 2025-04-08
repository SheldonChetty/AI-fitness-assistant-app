from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

BASE_PROMPT = """
You are Donnie, a friendly gym assistant that helps users build workout routines, answer fitness questions, 
and give suggestions based on fitness goals. Keep responses short, friendly, and only fitness-related.
"""

messages = [{"role": "system", "content": BASE_PROMPT}]

OPENROUTER_API_KEY = "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"

@app.route("/")
def home():
    return render_template("chatbot.html")

@app.route("/chatbot", methods=["POST"])
def chatbot():
    user_message = request.json["message"]
    messages.append({"role": "user", "content": user_message})

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "HTTP-Referer": "http://localhost",
        "Content-Type": "application/json",
    }

    payload = {
        "model": "mistralai/mistral-7b-instruct",
        "messages": messages,
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)

    if response.status_code == 200:
        reply = response.json()["choices"][0]["message"]["content"]
        messages.append({"role": "assistant", "content": reply})
        return jsonify({"reply": reply})
    else:
        return jsonify({"reply": f"Error {response.status_code}: {response.text}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
