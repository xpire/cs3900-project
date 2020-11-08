"""
Checks if the database is awake - creates if not, else passes the instance
"""

import logging
from typing import Any

from src.db.session import SessionLocal
from tenacity import after_log, before_log, retry, stop_after_attempt, wait_fixed

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

max_tries = 60 * 5  # 5 minutes
wait_seconds = 1


@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.WARN),
)
def init(is_test: bool, test_session: Any) -> None:
    try:
        db = test_session if is_test else SessionLocal()
        # Try to create session to check if DB is awake
        db.execute("SELECT 1")
    except Exception as e:
        logger.error(e)
        raise e


def main() -> None:
    logger.info("Initializing service")
    init(is_test=False, test_session=None)
    logger.info("Service finished initializing")


if __name__ == "__main__":
    main()
