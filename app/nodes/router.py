from app.rag.retriever import retrieve
from app.utils.logger import get_logger

logger = get_logger("router")

THRESHOLD = 1  # adjust based on your embedding scores


def router_node(state):
    query = state["query"]

    logger.info(f"Query: {query}")

    result = retrieve(query)

    scores = result["scores"]
    contexts = result["contexts"]

    best_score = min(scores) if scores else 999

    logger.info(f"Scores: {scores}")
    logger.info(f"Best Score: {best_score}")

    if best_score < THRESHOLD:
        route = "pdf"
        logger.info("Decision: PDF")
    else:
        route = "web"
        logger.info("Decision: WEB")

    return {
        "route": route,
        "context": contexts
    }