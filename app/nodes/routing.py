from langchain_core.messages import SystemMessage, HumanMessage
from ..models import get_llm
from ..schemas import RouterDecision
from ..state import State

ROUTER_SYSTEM = '''
You route topics for a technical blog writer.
closed_book = evergreen concept; no web research.
hybrid = evergreen topic needing current tools/examples; research is useful.
open_book = latest/news/pricing/policy; research is required.
If research is needed, return 3–6 focused search queries. Do not invent evidence.
'''

def router_node(state: State) -> dict:
    decision = get_llm().with_structured_output(RouterDecision).invoke([
        SystemMessage(content=ROUTER_SYSTEM),
        HumanMessage(content=f"Topic: {state['topic']}\nAs-of date: {state['as_of']}"),
    ])
    days = 7 if decision.mode == "open_book" else 45 if decision.mode == "hybrid" else 3650
    return {
        "needs_research": decision.needs_research,
        "mode": decision.mode,
        "queries": decision.queries,
        "recency_days": days,
    }

def route_next(state: State) -> str:
    return "research" if state["needs_research"] else "orchestrator"
