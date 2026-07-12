import logging

from app.db.session import SessionLocal
from app.repositories.server_repository import ServerRepository
from app.services.monitoring_service import MonitoringService

logger = logging.getLogger(__name__)


def collect_metrics_job():

    db = SessionLocal()

    try:

        server_repo = ServerRepository(db)

        monitoring = MonitoringService(db)

        servers = server_repo.get_monitoring_enabled()

        logger.info(
            "Collecting metrics for %s servers",
            len(servers),
        )

        for server in servers:

            try:

                monitoring.collect(server)

            except Exception as ex:

                logger.exception(
                    "Failed collecting metrics for %s : %s",
                    server.hostname,
                    ex,
                )

    finally:

        db.close()
