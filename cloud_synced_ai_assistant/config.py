"""
Configuration module for Cloud-Synced AI Assistant.
Values are primarily sourced from environment variables and optional .env file.
Edit these defaults or create a .env file at project root.
"""
from __future__ import annotations
import os
from pathlib import Path
from dotenv import load_dotenv
try:
    import streamlit as st  # type: ignore
except Exception:  # pragma: no cover
    st = None  # type: ignore

# Load .env if present
load_dotenv()

# Project root
PROJECT_ROOT = Path(__file__).resolve().parent
ASSETS_DIR = PROJECT_ROOT / "assets"
SCREENSHOTS_DIR = ASSETS_DIR / "screenshots"
HISTORY_LOG_FILE = PROJECT_ROOT / "history.txt"

# Ensure directories exist
ASSETS_DIR.mkdir(parents=True, exist_ok=True)
SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)

# General
APP_NAME = os.getenv("APP_NAME", "Cloud-Synced AI Assistant")
DEFAULT_TIMEZONE = os.getenv("DEFAULT_TIMEZONE", "UTC")
STREAMLIT_PORT = int(os.getenv("STREAMLIT_PORT", "8501"))

# Notion
NOTION_API_KEY = os.getenv("NOTION_API_KEY", "")  # e.g., secret_xxx
NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID", "")  # target DB for pages

# Obsidian
OBSIDIAN_VAULT_PATH = Path(os.getenv("OBSIDIAN_VAULT_PATH", str(PROJECT_ROOT / "obsidian_vault")))
OBSIDIAN_VAULT_PATH.mkdir(parents=True, exist_ok=True)

# Google Calendar OAuth files
GOOGLE_CREDENTIALS_FILE = Path(os.getenv("GOOGLE_CREDENTIALS_FILE", str(PROJECT_ROOT / "credentials.json")))
GOOGLE_TOKEN_FILE = Path(os.getenv("GOOGLE_TOKEN_FILE", str(PROJECT_ROOT / "token.json")))
GOOGLE_CALENDAR_ID = os.getenv("GOOGLE_CALENDAR_ID", "primary")

# Feature toggles
VOICE_FEEDBACK_ENABLED = os.getenv("VOICE_FEEDBACK_ENABLED", "true").lower() == "true"
VOICE_INPUT_ENABLED = os.getenv("VOICE_INPUT_ENABLED", "true").lower() == "true"


def ensure_history_file() -> Path:
    """Ensure history log file exists."""
    if not HISTORY_LOG_FILE.exists():
        HISTORY_LOG_FILE.touch()
    return HISTORY_LOG_FILE


def secrets_get(key: str, default: str = "") -> str:
    """Helper to get a string from Streamlit secrets if running on Streamlit Cloud."""
    if st and hasattr(st, "secrets") and key in st.secrets:  # type: ignore[attr-defined]
        try:
            val = st.secrets[key]  # type: ignore[index]
            if isinstance(val, (str, bytes)):
                return str(val)
        except Exception:
            pass
    return default


def write_google_oauth_files_from_secrets() -> None:
    """If Streamlit secrets provide GOOGLE_CREDENTIALS_JSON or GOOGLE_TOKEN_JSON, write them to files.
    This allows Streamlit Cloud deployment without committing JSON credentials.
    """
    creds_json = secrets_get("GOOGLE_CREDENTIALS_JSON", "")
    if creds_json:
        try:
            GOOGLE_CREDENTIALS_FILE.write_text(creds_json, encoding="utf-8")
        except Exception:
            pass
    token_json = secrets_get("GOOGLE_TOKEN_JSON", "")
    if token_json:
        try:
            GOOGLE_TOKEN_FILE.write_text(token_json, encoding="utf-8")
        except Exception:
            pass


# Override certain configs from Streamlit secrets when available
NOTION_API_KEY = secrets_get("NOTION_API_KEY", NOTION_API_KEY)
NOTION_DATABASE_ID = secrets_get("NOTION_DATABASE_ID", NOTION_DATABASE_ID)
GOOGLE_CALENDAR_ID = secrets_get("GOOGLE_CALENDAR_ID", GOOGLE_CALENDAR_ID)
