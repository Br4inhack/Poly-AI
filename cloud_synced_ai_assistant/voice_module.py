"""
Voice input/output utilities using SpeechRecognition and pyttsx3.
- listen(): capture microphone audio and return transcribed text.
- speak(): synthesize speech for feedback.
"""
from __future__ import annotations
import sys
import time
from typing import Optional

try:
    import speech_recognition as sr
except Exception:  # pragma: no cover - optional at runtime
    sr = None  # type: ignore

try:
    import pyttsx3  # Offline TTS
except Exception:  # pragma: no cover - optional at runtime
    pyttsx3 = None  # type: ignore


class VoiceAssistant:
    def __init__(self, rate: int = 180, volume: float = 1.0, voice_name: Optional[str] = None) -> None:
        self.recognizer = sr.Recognizer() if sr else None
        self.engine = pyttsx3.init() if pyttsx3 else None
        if self.engine:
            try:
                self.engine.setProperty("rate", rate)
                self.engine.setProperty("volume", volume)
                if voice_name:
                    for v in self.engine.getProperty("voices"):
                        if voice_name.lower() in v.name.lower():
                            self.engine.setProperty("voice", v.id)
                            break
            except Exception:
                pass

    def listen(self, timeout: int = 5, phrase_time_limit: int = 10) -> Optional[str]:
        """Listen from default microphone and return transcribed text (en-US).
        Returns None if microphone or recognizer not available.
        """
        if not self.recognizer or not sr:
            return None
        try:
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            text = self.recognizer.recognize_google(audio, language="en-US")
            return text.strip()
        except sr.WaitTimeoutError:
            return None
        except Exception:
            return None

    def speak(self, text: str) -> None:
        """Speak text using pyttsx3 if available; otherwise prints to stdout."""
        if not text:
            return
        if self.engine:
            try:
                self.engine.say(text)
                self.engine.runAndWait()
            except Exception:
                print(f"[TTS] {text}")
        else:
            print(f"[TTS] {text}")


def demo() -> None:  # Simple CLI demo
    va = VoiceAssistant()
    print("Say something (Ctrl+C to exit)...")
    while True:
        try:
            text = va.listen()
            if text:
                print("You said:", text)
                va.speak(f"You said: {text}")
            else:
                print("(No input)")
            time.sleep(0.5)
        except KeyboardInterrupt:
            print("Exiting...")
            sys.exit(0)


if __name__ == "__main__":
    demo()
