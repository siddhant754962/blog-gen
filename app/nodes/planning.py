from langchain_core.messages import SystemMessage, HumanMessage
from ..models import get_llm
from ..schemas import Plan, EvidencePack, EvidenceItem
from ..research import tavily_search
from ..state import State

ORCH_SYSTEM = '''
You are a senior technical writer. Produce a useful blog outline with 5–7 tasks.
Each task needs a goal, 3–6 bullets, target_words, and flags for research/citations/code.
For open_book topics, use blog_kind=news_roundup and do not invent events.
Use evidence when provided. Output must match the Plan schema.
'''

def research_node(state: State) -> dict:
    raw = []
    for query in (state.get("queries") or [])[:8]:
        raw.extend(tavily_search(query, max_results=5))
    if not raw:
        return {"evidence": []}
    pack = get_llm().with_structured_output(EvidencePack).invoke([
        SystemMessage(content="Extract relevant EvidenceItem objects from these search results. Keep only items with URLs; deduplicate URLs; do not guess dates."),
        HumanMessage(content=f"As-of: {state['as_of']}\nResults: {raw}"),
    ])
    unique = {item.url: item for item in pack.evidence if item.url}
    return {"evidence": list(unique.values())}

def orchestrator_node(state: State) -> dict:
    evidence = [e.model_dump() if hasattr(e, "model_dump") else e for e in state.get("evidence", [])]
    plan = get_llm().with_structured_output(Plan).invoke([
        SystemMessage(content=ORCH_SYSTEM),
        HumanMessage(content=f"Topic: {state['topic']}\nMode: {state.get('mode')}\nAs-of: {state['as_of']}\nEvidence: {evidence[:15]}"),
    ])
    if state.get("mode") == "open_book":
        plan.blog_kind = "news_roundup"
    return {"plan": plan}
