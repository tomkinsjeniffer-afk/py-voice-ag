import sounddevice as sd

print("Available audio devices:")
print(sd.query_devices())

print("\nDefault input device:")
print(sd.default.device)

input("Press Enter to test mic (will record 3 sec)...")
print("Recording...")
audio = sd.rec(int(3 * 16000), samplerate=16000, channels=1, dtype='int16')
sd.wait()
print("✅ Recording finished. If you heard no errors, mic works!")