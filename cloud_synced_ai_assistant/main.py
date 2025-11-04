"""
Main orchestrator for the Cloud-Synced AI Assistant.
- Listens for voice (or fallbacks to CLI input)
- Recognizes intent
- Executes Notion/Obsidian/Calendar actions
- Provides voice feedback and logs history
"""
from __future__ import annotations
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional

import config
from voice_module import VoiceAssistant
from intent_module import recognize_intent
from notion_module import add_page_to_database
from obsidian_module import write_markdown
from calendar_module import create_event

# Logging setup
config.ensure_history_file()
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(config.HISTORY_LOG_FILE, encoding="utf-8"),
    ],
)
logger = logging.getLogger(__name__)


def log_action(message: str) -> None:
    logger.info(message)


def handle_text_command(text: str, voice: Optional[VoiceAssistant] = None) -> str:
    """Handle a single text command and return a response string."""
    intent = recognize_intent(text)
    if intent.intent == "notion_note":
        res = add_page_to_database(intent.payload["title"], intent.payload["content"])
        reply = res["message"]
    elif intent.intent == "obsidian_note":
        res = write_markdown(intent.payload["title"], intent.payload["content"])
        reply = res["message"]
    elif intent.intent == "calendar_event":
        res = create_event(
            summary=intent.payload["summary"],
            start=intent.payload["start"],
            end=intent.payload["end"],
            timezone=config.DEFAULT_TIMEZONE,
        )
        reply = res["message"]
    else:
        reply = "Sorry, I didn't understand. Try mentioning Notion, Obsidian, or Calendar."

    log_action(f"Command: {text} -> {reply}")
    if voice and config.VOICE_FEEDBACK_ENABLED:
        voice.speak(reply)
    return reply


def main() -> None:
    voice = VoiceAssistant() if config.VOICE_INPUT_ENABLED or config.VOICE_FEEDBACK_ENABLED else None
    print(f"{config.APP_NAME} - say something or type. Press Ctrl+C to exit.")
    while True:
        try:
            text = None
            if voice and config.VOICE_INPUT_ENABLED:
                text = voice.listen()
            if not text:
                text = input("> ")
            if text:
                reply = handle_text_command(text, voice)
                print(reply)
        except KeyboardInterrupt:
            print("\nGoodbye.")
            break
        except Exception as e:
            logger.exception("Error: %s", e)
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
