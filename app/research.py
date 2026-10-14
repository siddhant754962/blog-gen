import os
from typing import List
from .config import TAVILY_API_KEY

def tavily_search(query: str, max_results: int = 5) -> List[dict]:
    if not TAVILY_API_KEY:
        return []
    try:
        from langchain_community.tools.tavily_search import TavilySearchResults
        tool = TavilySearchResults(max_results=max_results)
        results = tool.invoke({"query": query})
        return [{
            "title": r.get("title") or "",
            "url": r.get("url") or "",
            "snippet": r.get("content") or r.get("snippet") or "",
            "published_at": r.get("published_date") or r.get("published_at"),
            "source": r.get("source"),
        } for r in (results or []) if r.get("url")]
    except Exception as exc:
        print(f"[research] Search skipped: {exc}")
        return []
