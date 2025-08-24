import logging
import sys
import traceback

def setup_logger():
    logger = logging.getLogger("chatbot")
    logger.setLevel(logging.DEBUG)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s", "%Y-%m-%d %H:%M:%S"
    )
    handler.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(handler)

    return logger

logger = setup_logger()

def log_exception(e: Exception):
    logger.error("Exception occurred: %s", str(e))
    traceback_str = "".join(traceback.format_exception(type(e), e, e.__traceback__))
    logger.debug("Traceback:\n%s", traceback_str)
