import random
import time

from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.types import Send
from ..models import get_llm
from ..schemas import Plan, Task
from ..state import State

WORKER_SYSTEM = """
Write one technical blog section in Markdown. Start with a level-two heading.
Cover every requested bullet in order and aim for target_words ±20%.
For open_book topics, make current claims only when supported by supplied evidence URLs
and cite them as Markdown links. If citations are required, cite supplied evidence.
If code is required, include a minimal working code snippet. Return only section Markdown.
"""


def fanout(state: State):
    plan = state["plan"]
    if plan is None:
        raise ValueError("No plan available for section-writing fanout.")

    # Pass only compact evidence fields to each worker; do not resend the whole plan.
    evidence = []
    for item in state.get("evidence", [])[:8]:
        item = item.model_dump() if hasattr(item, "model_dump") else item
        evidence.append({
            "title": str(item.get("title", ""))[:180],
            "url": str(item.get("url", ""))[:400],
            "published_at": str(item.get("published_at") or "date unknown")[:40],
            "snippet": str(item.get("snippet") or "")[:300],
        })

    plan_info = {
        "blog_title": plan.blog_title,
        "audience": plan.audience,
        "tone": plan.tone,
        "blog_kind": plan.blog_kind,
    }

    return [
        Send("worker", {
            "task": task.model_dump(),
            "topic": state["topic"],
            "mode": state.get("mode", "hybrid"),
            "plan_info": plan_info,
            "evidence": evidence,
        })
        for task in plan.tasks
    ]


def _is_rate_limit_error(exc: Exception) -> bool:
    message = str(exc).lower()
    return (
        "rate limit" in message
        or "rate_limit_exceeded" in message
        or "tokens per minute" in message
        or "error code: 429" in message
    )


def worker_node(payload: dict) -> dict:
    task = Task(**payload["task"])
    plan_info = payload["plan_info"]
    evidence = payload.get("evidence", [])

    evidence_lines = []
    if task.requires_citations or payload.get("mode") == "open_book":
        for item in evidence[:6]:
            line = f"- {item.get('title', 'Source')} | {item.get('url', '')}"
            if item.get("published_at") and item["published_at"] != "date unknown":
                line += f" | {item['published_at']}"
            if item.get("snippet"):
                line += f" | {item['snippet'][:220]}"
            evidence_lines.append(line)

    bullets = "\n".join(f"- {bullet}" for bullet in task.bullets)
    evidence_text = "\n".join(evidence_lines) if evidence_lines else "No external evidence supplied."

    user_prompt = (
        f"Blog title: {plan_info.get('blog_title', payload['topic'])}\n"
        f"Audience: {plan_info.get('audience', 'General technical audience')}\n"
        f"Tone: {plan_info.get('tone', 'Clear and practical')}\n"
        f"Blog kind: {plan_info.get('blog_kind', 'explainer')}\n"
        f"Topic: {payload['topic']}\n"
        f"Mode: {payload.get('mode', 'hybrid')}\n"
        f"Section: {task.title}\n"
        f"Goal: {task.goal}\n"
        f"Target words: {task.target_words}\n"
        f"Requires citations: {task.requires_citations}\n"
        f"Requires code: {task.requires_code}\n"
        f"Bullets to cover in order:\n{bullets}\n"
        f"Allowed evidence sources:\n{evidence_text}\n"
        "Do not invent citations or source URLs."
    )

    llm = get_llm()
    # A short bounded retry handles transient 429s. It cannot bypass a sustained
    # account TPM limit; retries are staggered to reduce simultaneous retries.
    for attempt in range(3):
        try:
            response = llm.invoke([
                SystemMessage(content=WORKER_SYSTEM),
                HumanMessage(content=user_prompt),
            ])
            content = response.content
            if not isinstance(content, str):
                content = str(content)
            return {"sections": [(task.id, content.strip())]}
        except Exception as exc:
            if not _is_rate_limit_error(exc) or attempt == 2:
                raise
            time.sleep((10 * (attempt + 1)) + random.uniform(0, 2))

    raise RuntimeError("Worker generation failed after retries.")
