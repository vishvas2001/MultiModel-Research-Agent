from app.utils.logger import get_logger

logger = get_logger("critic")


def critic_node(state):
    context = state.get("context", [])

    logger.info("Evaluating context...")

    if not context:
        logger.warning("No context → retry")
        return {"retry": True}

    total_length = sum(len(c) for c in context)

    logger.info(f"Context length: {total_length}")

    if total_length < 200:
        logger.warning("Weak context → retry")
        return {"retry": True}

    logger.info("Context is sufficient")

    return {"retry": False}