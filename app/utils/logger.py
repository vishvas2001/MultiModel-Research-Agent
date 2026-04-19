import logging
import sys

# Global log storage
LOG_STORAGE = []


class ListHandler(logging.Handler):
    def emit(self, record):
        log_entry = self.format(record)
        LOG_STORAGE.append(log_entry)


def get_logger(name: str):
    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "[%(levelname)s] [%(name)s] %(message)s"
    )

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    # Memory handler (for UI)
    memory_handler = ListHandler()
    memory_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(memory_handler)
    
    

    return logger


def get_logs():
    return LOG_STORAGE


def clear_logs():
    LOG_STORAGE.clear()