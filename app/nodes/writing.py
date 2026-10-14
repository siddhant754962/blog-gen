from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.types import Send
from ..models import get_llm
from ..schemas import Plan, Task, EvidenceItem
from ..state import State

WORKER_SYSTEM = '''
Write one technical blog section in Markdown. Start with "## <Section Title>".
Cover every requested bullet in order and aim for target_words ±20%.
For open_book topics, make specific current claims only when supported by supplied evidence URLs and cite them as Markdown links.
If requires_citations is true, cite provided evidence for external claims.
If requires_code is true, include a minimal working code snippet.
Return only the section Markdown.
'''

def fanout(state: State):
    plan = state["plan"]
    if plan is None:
        raise ValueError("No plan available for section-writing fanout.")
    return [Send("worker", {
        "task": task.model_dump(),
        "topic": state["topic"],
        "mode": state["mode"],
        "as_of": state["as_of"],
        "plan": plan.model_dump(),
        "evidence": [e.model_dump() if hasattr(e, "model_dump") else e for e in state.get("evidence", [])],
    }) for task in plan.tasks]

def worker_node(payload: dict) -> dict:
    task = Task(**payload["task"])
    plan = Plan(**payload["plan"])
    evidence = payload.get("evidence", [])
    evidence_text = "\n".join(f"- {e.get('title')} | {e.get('url')} | {e.get('published_at') or 'date unknown'}" for e in evidence[:20])
    bullets = "\n".join(f"- {b}" for b in task.bullets)
    response = get_llm().invoke([
        SystemMessage(content=WORKER_SYSTEM),
        HumanMessage(content=(
            f"Blog title: {plan.blog_title}\nAudience: {plan.audience}\nTone: {plan.tone}\n"
            f"Blog kind: {plan.blog_kind}\nTopic: {payload['topic']}\nMode: {payload['mode']}\n"
            f"Section: {task.title}\nGoal: {task.goal}\nTarget words: {task.target_words}\n"
            f"requires_citations: {task.requires_citations}\nrequires_code: {task.requires_code}\n"
            f"Bullets:\n{bullets}\nEvidence URLs allowed:\n{evidence_text}"
        )),
    ])
    content = response.content
    if not isinstance(content, str):
        content = str(content)
    return {"sections": [(task.id, content.strip())]}
