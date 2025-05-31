function startRecording() {
    const recognition = new webkitSpeechRecognition() || new SpeechRecognition();
    recognition.lang = 'en-IN';
    recognition.start();

    recognition.onresult = async function (event) {
        const transcript = event.results[0][0].transcript;
        document.getElementById("user-text").textContent = transcript;

        const res = await fetch("/ask", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({message: transcript})
        });

        const data = await res.json();
        document.getElementById("bot-text").textContent = data.reply;

        const synth = window.speechSynthesis;
        const utter = new SpeechSynthesisUtterance(data.reply);
        utter.lang = 'en-IN';
        synth.speak(utter);
    };
}
