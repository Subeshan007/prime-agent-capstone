"""
Logging configuration using loguru.
"""
import sys
from loguru import logger
from prime_agent.config import LOG_LEVEL

def setup_logging():
    logger.remove()
    logger.add(sys.stderr, level=LOG_LEVEL)
    logger.add("prime_agent.log", rotation="10 MB", level=LOG_LEVEL)

setup_logging()
