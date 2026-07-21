"""
import logging

from app.core.config import settings


def setup_logging():
    logging.basicConfig(
        level=settings.LOG_LEVEL,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )


logger = logging.getLogger("it-monitoring")
"""

import logging

from app.core.logging_config import LOGGING

logger = logging.getLogger("it_monitoring")
