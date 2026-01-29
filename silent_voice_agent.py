import os
import json
import pyttsx3
import sounddevice as sd
from vosk import Model, KaldiRecognizer

MODEL_FOLDER = "vosk-model-small-en-us-0.15"
SAMPLE_RATE = 16000

script_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(script_dir, MODEL_FOLDER)

if not os.path.exists(model_path):
    print("❌ Model missing")
    exit(1)

tts = pyttsx3.init()
tts.setProperty('rate', 150)

def speak(text):
    print(f"🤖 AI: {text}")
    tts.say(text)
    tts.runAndWait()

# === START ===
print("🔇 Listening... (speak now)")

model = Model(model_path)
recognizer = KaldiRecognizer(model, SAMPLE_RATE)

with sd.RawInputStream(
    samplerate=SAMPLE_RATE,
    blocksize=8000,
    dtype='int16',
    channels=1
):
    while True:
        data = sd.rec(4000, samplerate=SAMPLE_RATE, channels=1, dtype='int16')
        sd.wait()
        
        # Always feed to Vosk
        recognizer.AcceptWaveform(data.tobytes())
        result = recognizer.Result()  # Get partial results too
        res_dict = json.loads(result)
        
        text = res_dict.get("text", "").strip()
        partial = res_dict.get("partial", "").strip()
        
        # Show what Vosk is hearing
        if partial:
            print(f"👂 Partial: '{partial}'")
        if text:
            print(f"✅ Final: '{text}'")
            if "goodbye" in text.lower():
                speak("Goodbye!")
                break
            else:
                speak("I heard you!")