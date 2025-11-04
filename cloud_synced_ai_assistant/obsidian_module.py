"""
Obsidian integration: write markdown files into a specified vault folder.
"""
from __future__ import annotations
from datetime import datetime
from pathlib import Path
import re
from typing import Dict, Any
import config


def _sanitize_filename(name: str) -> str:
    name = name.strip() or "New Note"
    name = re.sub(r"[^a-zA-Z0-9\-_\s]", "", name)
    name = re.sub(r"\s+", " ", name)
    return name[:80]


def write_markdown(title: str, content: str) -> Dict[str, Any]:
    """Create a markdown file in the Obsidian vault with timestamped filename."""
    vault: Path = config.OBSIDIAN_VAULT_PATH
    vault.mkdir(parents=True, exist_ok=True)
    safe_title = _sanitize_filename(title)
    ts = datetime.now().strftime("%Y-%m-%d_%H-%M")
    filename = f"{ts} - {safe_title}.md"
    path = vault / filename
    body = f"# {title}\n\n{content}\n"
    try:
        path.write_text(body, encoding="utf-8")
        return {"success": True, "message": f"Saved to Obsidian: {path}", "path": str(path)}
    except Exception as e:
        return {"success": False, "message": f"Obsidian write error: {e}"}
