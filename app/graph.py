from langgraph.graph import StateGraph, START, END
from .state import State
from .nodes.routing import router_node, route_next
from .nodes.planning import research_node, orchestrator_node
from .nodes.writing import worker_node, fanout
from .nodes.finalize import finalize_blog


def build_graph():
    graph = StateGraph(State)
    graph.add_node("router", router_node)
    graph.add_node("research", research_node)
    graph.add_node("orchestrator", orchestrator_node)
    graph.add_node("worker", worker_node)
    graph.add_node("finalize", finalize_blog)

    graph.add_edge(START, "router")
    graph.add_conditional_edges(
        "router",
        route_next,
        {"research": "research", "orchestrator": "orchestrator"},
    )
    graph.add_edge("research", "orchestrator")
    graph.add_conditional_edges("orchestrator", fanout, ["worker"])
    graph.add_edge("worker", "finalize")
    graph.add_edge("finalize", END)
    return graph.compile()


blog_graph = build_graph()
