"""
Notion integration using notion-client.
Provide add_page_to_database() to create a simple page with title and content.
"""
from __future__ import annotations
from typing import Optional, Dict, Any
from notion_client import Client
import config


def get_notion_client() -> Optional[Client]:
    if not config.NOTION_API_KEY:
        return None
    return Client(auth=config.NOTION_API_KEY)


def add_page_to_database(title: str, content: str) -> Dict[str, Any]:
    """Add a page with a title and content to the configured Notion database.
    Returns a dict with keys: success(bool), message(str), data(optional).
    """
    db_id = config.NOTION_DATABASE_ID
    if not db_id:
        return {"success": False, "message": "NOTION_DATABASE_ID not configured"}
    client = get_notion_client()
    if not client:
        return {"success": False, "message": "NOTION_API_KEY not configured"}
    try:
        page = client.pages.create(
            parent={"database_id": db_id},
            properties={
                "Name": {"title": [{"text": {"content": title}}]},
            },
            children=[
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {"rich_text": [{"type": "text", "text": {"content": content}}]},
                }
            ],
        )
        return {"success": True, "message": "Note added to Notion", "data": page}
    except Exception as e:
        return {"success": False, "message": f"Notion error: {e}"}
