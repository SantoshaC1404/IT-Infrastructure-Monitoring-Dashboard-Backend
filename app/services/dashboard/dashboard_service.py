from sqlalchemy.orm import Session

from app.services.dashboard.dashboard_summary_service import DashboardSummaryService


class DashboardService:

    def __init__(self, db: Session):

        self.summary_service = DashboardSummaryService(db)

    def get_dasgboard_summary(self):

        return self.summary_service.get_summary()
