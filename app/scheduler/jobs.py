import logging

from app.db.session import SessionLocal
from app.services.monitoring_service import MonitoringService

logger = logging.getLogger(__name__)


def collect_metrics_job():

    db = SessionLocal()

    try:

        logger.info("Starting scheduled metrics collection")

        monitoring = MonitoringService(db)

        monitoring.monitor_all_servers()

    finally:

        db.close()
