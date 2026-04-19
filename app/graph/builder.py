from langgraph.graph import StateGraph
from app.graph.state import AgentState

from app.nodes.router import router_node
from app.nodes.pdf_node import pdf_node
from app.nodes.web_node import web_node
from app.nodes.critic import critic_node
from app.nodes.responder import responder_node


def build_graph():
    builder = StateGraph(AgentState)

    # Nodes
    builder.add_node("router", router_node)
    builder.add_node("pdf", pdf_node)
    builder.add_node("web", web_node)
    builder.add_node("critic", critic_node)
    builder.add_node("responder", responder_node)

    # Entry
    builder.set_entry_point("router")

    # Router → PDF or Web
    builder.add_conditional_edges(
        "router",
        lambda x: x["route"],
        {
            "pdf": "pdf",
            "web": "web"
        }
    )

    # PDF → Critic
    builder.add_edge("pdf", "critic")

    # Critic → Web OR Responder
    builder.add_conditional_edges(
        "critic",
        lambda x: "web" if x["retry"] else "responder"
    )

    # Web → Responder
    builder.add_edge("web", "responder")

    # End
    builder.add_edge("responder", "__end__")

    return builder.compile()