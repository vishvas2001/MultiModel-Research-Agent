from app.llm.model import llm
from app.llm.prompts import build_prompt
from app.utils.logger import get_logger

logger = get_logger("responder")


def responder_node(state):
    query = state["query"]
    context = state.get("context", [])

    logger.info("Generating final answer...")

    if not context:
        logger.warning("No context available")
        return {
            "answer": "No relevant information found."
        }

    prompt = build_prompt(query, context)

    response = llm.invoke(prompt)

    return {
        "answer": response
    }