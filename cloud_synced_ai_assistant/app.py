"""
Streamlit UI for the Cloud-Synced AI Assistant.
Provides text input and action buttons. Voice input optional (uses SpeechRecognition if available).
"""
from __future__ import annotations
import streamlit as st
from datetime import datetime, timedelta

import config
from intent_module import recognize_intent
from notion_module import add_page_to_database
from obsidian_module import write_markdown
from calendar_module import create_event
from voice_module import VoiceAssistant

st.set_page_config(page_title=config.APP_NAME, page_icon="🤖", layout="centered")

st.title("🤖 Cloud-Synced AI Assistant")

with st.sidebar:
    st.header("Settings")
    voice_feedback = st.toggle("Voice feedback", value=config.VOICE_FEEDBACK_ENABLED)
    st.info("Voice input in browser is limited. Use desktop app or CLI for continuous listening.")

text = st.text_area("Say or type a command:", placeholder="Add a note to Notion about meeting ideas")

col1, col2, col3 = st.columns(3)

if col1.button("Send"):
    intent = recognize_intent(text)
    if intent.intent == "notion_note":
        res = add_page_to_database(intent.payload["title"], intent.payload["content"])
        if res.get("success"):
            st.success(res["message"])
        else:
            st.error(res["message"])
    elif intent.intent == "obsidian_note":
        res = write_markdown(intent.payload["title"], intent.payload["content"])
        if res.get("success"):
            st.success(res["message"])
        else:
            st.error(res["message"])
    elif intent.intent == "calendar_event":
        res = create_event(intent.payload["summary"], intent.payload["start"], intent.payload["end"], config.DEFAULT_TIMEZONE)
        if res.get("success"):
            st.success(res["message"])
        else:
            st.error(res["message"])
    else:
        st.warning("Try mentioning Notion, Obsidian, or Calendar in your command.")

    if voice_feedback:
        try:
            VoiceAssistant().speak("Action completed")
        except Exception:
            pass

st.markdown("---")
st.caption("Tip: Examples — 'Add a note to Notion about meeting ideas', 'Write this in Obsidian: brain dump', 'Add meeting at 5 pm tomorrow'.")
