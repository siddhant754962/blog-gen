from langchain_core.messages import SystemMessage, HumanMessage
from pydantic import ValidationError
from ..models import get_llm
from ..schemas import Plan, EvidencePack, EvidenceItem
from ..research import tavily_search
from ..state import State
import json
import re

ORCH_SYSTEM = """
You are a senior technical writer. Produce a useful blog outline with 5–7 tasks.
Each task needs a goal, 3–6 bullets, target_words, and flags for research/citations/code.
For open_book topics, use blog_kind=news_roundup and do not invent events.
Use evidence when provided. Output must match the Plan schema.
"""


def _clean_url(url: str) -> str:
    """Normalize common escaped URL characters without inventing a URL."""
    url = (url or "").strip()
    url = url.replace(r"\\/", "/").replace(r"\\.", ".").replace(r"\\:", ":")
    url = url.replace(r"\u0026", "&").replace("\\u0026", "&")
    # Remove wrapping punctuation sometimes included in search snippets.
    return url.rstrip(".,;)]}")


def _evidence_from_search_results(raw: list) -> list[EvidenceItem]:
    """Convert Tavily results directly into validated evidence items."""
    items: list[EvidenceItem] = []
    seen: set[str] = set()

    for result in raw:
        if not isinstance(result, dict):
            continue

        url = _clean_url(str(result.get("url", "")))
        if not (url.startswith("https://") or url.startswith("http://")):
            continue
        if url in seen:
            continue
        seen.add(url)

        title = str(result.get("title") or "Untitled source").strip()
        snippet = result.get("snippet") or result.get("content")
        published_at = result.get("published_at") or result.get("published_date")
        source = result.get("source")

        try:
            items.append(EvidenceItem(
                title=title[:500],
                url=url,
                snippet=str(snippet)[:2000] if snippet else None,
                published_at=str(published_at) if published_at else None,
                source=str(source) if source else None,
            ))
        except (ValidationError, TypeError, ValueError):
            continue

    return items


def research_node(state: State) -> dict:
    raw = []
    for query in (state.get("queries") or [])[:8]:
        try:
            results = tavily_search(query, max_results=5)
            if isinstance(results, list):
                raw.extend(results)
        except Exception:
            # A failed query should not stop the rest of the research run.
            continue

    if not raw:
        return {"evidence": []}

    # Avoid another LLM tool call here: search results already contain the
    # source fields needed for EvidenceItem, and structured tool calls can fail
    # when the model emits malformed arguments.
    evidence = _evidence_from_search_results(raw)
    return {"evidence": evidence}


def orchestrator_node(state: State) -> dict:
    evidence = [
        e.model_dump() if hasattr(e, "model_dump") else e
        for e in state.get("evidence", [])
    ]
    plan = get_llm().with_structured_output(Plan).invoke([
        SystemMessage(content=ORCH_SYSTEM),
        HumanMessage(
            content=(
                f"Topic: {state['topic']}\n"
                f"Mode: {state.get('mode')}\n"
                f"As-of: {state['as_of']}\n"
                f"Evidence: {evidence[:15]}"
            )
        ),
    ])
    if state.get("mode") == "open_book":
        plan.blog_kind = "news_roundup"
    return {"plan": plan}

