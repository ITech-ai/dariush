import speech_recognition as sr
import keyboard
import sys
import time

print("listening.py = True")
r = sr.Recognizer()

with sr.Microphone() as source_init:
    r.adjust_for_ambient_noise(source_init, duration=1)

def listen():
    if keyboard.is_pressed('esc'):
        print("Exiting...")
        sys.exit(0) 

    if keyboard.is_pressed('m'):
        print("m")
        with sr.Microphone() as source:
            audio_frames = []
            while keyboard.is_pressed('m'):
                try:
                    raw_data = source.stream.read(source.CHUNK)
                    audio_frames.append(raw_data)
                except Exception:
                    break
            
            
            if audio_frames:
                combined_raw_data = b"".join(audio_frames)
                audio_data = sr.AudioData(combined_raw_data, source.SAMPLE_RATE, source.SAMPLE_WIDTH)
                
                try:
                    text = r.recognize_google(audio_data, language="fa-IR")
                    print(text)
                    return text
                except sr.UnknownValueError:
                    return None
                except sr.RequestError:
                    return None
                except Exception as e:
                    print(f"[Error: {e}]")
                    return None
                
    return None
