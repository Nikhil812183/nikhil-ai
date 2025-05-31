from flask import Flask, request, jsonify, render_template
import os
import requests
import wikipedia
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
API_URL = "https://api.groq.com/openai/v1/chat/completions"
HEADERS = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}

@app.route("/")
def text_chat():
    return render_template("index.html")

@app.route("/voice")
def voice_chat():
    return render_template("voice.html")

@app.route("/ask", methods=["POST"])
def ask():
    user_input = request.json.get("message", "")
    data = {
        "model": "llama3-70b-8192",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_input}
        ],
        "temperature": 0.7
    }

    response = requests.post(API_URL, headers=HEADERS, json=data)
    if response.status_code == 200:
        answer = response.json()["choices"][0]["message"]["content"].strip()
        if len(answer) < 20:
            try:
                wiki_summary = wikipedia.summary(user_input, sentences=2)
                answer += "\n\n(Wikipedia says): " + wiki_summary
            except wikipedia.exceptions.DisambiguationError:
                answer += "\n\n(Wikipedia Disambiguation, please be more specific.)"
            except wikipedia.exceptions.PageError:
                answer += "\n\n(Wikipedia page not found.)"
            except Exception:
                answer += "\n\n(Couldn't find info on Wikipedia.)"
        return jsonify({"reply": answer})
    else:
        return jsonify({"reply": "Sorry, there was an error with the AI service."})

if __name__ == "__main__":
    app.run(debug=False)
