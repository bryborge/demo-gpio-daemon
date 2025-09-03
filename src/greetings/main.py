"""Main module for the greetings package."""

import logging


def main() -> str:
    """Return a greeting message."""
    return "Hello World"


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
logger.info(main())
