from app.tools.web_search import search_web
from app.utils.logger import get_logger

logger = get_logger("web_node")


def web_node(state):
    query = state["query"]

    logger.info("Fetching web results...")

    context = search_web(query)

    if not context:
        logger.warning("No web results found")

    return {
        "context": context,
        "source": "web"
    }