from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.models.device_alert import Alert
from app.utils.enums import AlertStatus


class AlertRepository:

    def __init__(self, db: Session):
        self.db = db

    # CREATE
    def create(self, alert: Alert):

        self.db.add(alert)
        self.db.flush()

        return alert

    # GET OPEN / ACKNOWLEDGED ALERT
    def get_open_alert(
        self,
        device_id: int,
        metric: str,
    ):

        stmt = (
            select(Alert)
            .options(joinedload(Alert.device))
            .where(
                Alert.device_id == device_id,
                Alert.metric == metric,
                Alert.status.in_(
                    [
                        AlertStatus.OPEN,
                        AlertStatus.ACKNOWLEDGED,
                    ]
                ),
            )
            .order_by(Alert.created_at.desc())
        )

        return self.db.scalars(stmt).first()

    # LATEST ALERTS
    def latest(self, limit: int = 20):

        stmt = (
            select(Alert)
            .options(joinedload(Alert.device))
            .order_by(Alert.created_at.desc())
            .limit(limit)
        )

        return list(self.db.scalars(stmt).all())

    # OPEN / ACKNOWLEDGED ALERTS
    def unresolved(self):

        stmt = (
            select(Alert)
            .options(joinedload(Alert.device))
            .where(
                Alert.status.in_(
                    [
                        AlertStatus.OPEN,
                        AlertStatus.ACKNOWLEDGED,
                    ]
                )
            )
            .order_by(Alert.created_at.desc())
        )

        return list(self.db.scalars(stmt).all())

    # GET BY ID
    def get_by_id(self, alert_id: int):

        stmt = (
            select(Alert).options(joinedload(Alert.device)).where(Alert.id == alert_id)
        )

        return self.db.scalars(stmt).first()

    # ACKNOWLEDGE
    def acknowledge(self, alert: Alert):

        alert.status = AlertStatus.ACKNOWLEDGED
        alert.acknowledged_at = datetime.utcnow()

        self.db.flush()

        return alert

    # RESOLVE
    def resolve(self, alert: Alert):

        alert.status = AlertStatus.RESOLVED
        alert.resolved_at = datetime.utcnow()

        self.db.flush()

        return alert
