import os
import requests
import speech_recognition as sr
import pyttsx3
from dotenv import load_dotenv

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

API_URL = "https://api.groq.com/openai/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}

def ask_groq(message):
    data = {
        "model": "llama3-70b-8192",
        "messages": [
            {"role": "system", "content": "You are a helpful voice assistant."},
            {"role": "user", "content": message}
        ],
        "temperature": 0.7
    }
    response = requests.post(API_URL, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"Error: {response.status_code}"

# Set up voice engine
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎙️ Listening...")
        audio = r.listen(source)
    try:
        text = r.recognize_google(audio)
        print("You:", text)
        return text
    except:
        return "Sorry, I didn't understand."

# Voice chat loop
if __name__ == "__main__":
    print("🤖 Voice Chatbot (say 'exit' to stop)")
    speak("Hello, I am your voice assistant. What can I do for you?")
    while True:
        user_input = listen()
        if "exit" in user_input.lower():
            speak("Goodbye!")
            break
        reply = ask_groq(user_input)
        print("Bot:", reply)
        speak(reply)

