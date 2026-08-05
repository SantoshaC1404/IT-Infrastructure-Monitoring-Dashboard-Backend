from sqlalchemy.orm import Session

from app.repositories.dashboard_repository import DashboardRepository
from app.core.logger import logger


class DashboardSummaryService:

    def __init__(self, db: Session):
        self.repository = DashboardRepository(db=db)

    # Dashboard Summary
    def get_summary(self):

        summary = self.repository.get_summary()

        # logger.info("Summary: %s", summary)

        return summary
