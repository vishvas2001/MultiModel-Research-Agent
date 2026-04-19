from app.utils.logger import get_logger

logger = get_logger("pdf_node")


def pdf_node(state):
    context = state.get("context", [])

    logger.info("Using PDF context")

    return {
        "context": context,
        "source": "pdf"
    }