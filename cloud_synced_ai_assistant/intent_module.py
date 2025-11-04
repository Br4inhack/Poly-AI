"""
Naive intent recognition via keyword-based routing.
Supports intents: notion_note, obsidian_note, calendar_event, unknown.
"""
from __future__ import annotations
import re
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional, Dict, Any


@dataclass
class IntentResult:
    intent: str
    payload: Dict[str, Any]


TIME_PATTERN = re.compile(r"\b(\d{1,2})(?::(\d{2}))?\s*(am|pm)?\b", re.IGNORECASE)


def parse_time_and_day(text: str) -> Optional[datetime]:
    """Very naive time parser supporting 'tomorrow' and times like '5 pm' or '17:30'."""
    text_l = text.lower()
    now = datetime.now()
    base_day = now
    if "tomorrow" in text_l:
        base_day = now + timedelta(days=1)
    m = TIME_PATTERN.search(text_l)
    if not m:
        return None
    hour = int(m.group(1))
    minute = int(m.group(2)) if m.group(2) else 0
    ampm = m.group(3)
    if ampm:
        ampm = ampm.lower()
        if ampm == "pm" and hour < 12:
            hour += 12
        if ampm == "am" and hour == 12:
            hour = 0
    return base_day.replace(hour=hour, minute=minute, second=0, microsecond=0)


def recognize_intent(text: str) -> IntentResult:
    t = text.strip()
    tl = t.lower()

    if any(k in tl for k in ["notion", "note to notion", "add a note"]):
        content = t
        # Strip trigger words
        content = re.sub(r"^.*?(notion|note to notion|add a note)\s*", "", content, flags=re.IGNORECASE)
        title = content[:60] or "New Note"
        return IntentResult("notion_note", {"title": title, "content": content})

    if any(k in tl for k in ["obsidian", "write this", "save note"]):
        content = re.sub(r"^.*?(obsidian|write this|save note)\s*", "", t, flags=re.IGNORECASE)
        title = content[:60] or "New Obsidian Note"
        return IntentResult("obsidian_note", {"title": title, "content": content})

    if any(k in tl for k in ["calendar", "meeting", "event", "schedule", "add meeting"]):
        start_dt = parse_time_and_day(t) or (datetime.now() + timedelta(hours=1))
        end_dt = start_dt + timedelta(hours=1)
        summary = t
        return IntentResult("calendar_event", {"summary": summary, "start": start_dt, "end": end_dt})

    return IntentResult("unknown", {"text": t})
