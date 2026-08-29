from sqlalchemy.orm import Session

from app.models.device import Device
from app.models.device_alert import Alert
from app.repositories.alert_repository import AlertRepository
from app.utils.constants import (
    CPU_THRESHOLD,
    MEMORY_THRESHOLD,
    DISK_THRESHOLD,
)
from app.utils.enums import AlertSeverity


class AlertService:

    def __init__(self, db: Session):
        self.db = db
        self.alert_repository = AlertRepository(db)

    # EVALUATE DEVICE METRICS
    def evaluate_device(
        self,
        device: Device,
        cpu_usage: float,
        memory_usage: float,
        disk_usage: float,
    ):

        metrics = [
            (
                "CPU",
                cpu_usage,
                CPU_THRESHOLD,
            ),
            (
                "MEMORY",
                memory_usage,
                MEMORY_THRESHOLD,
            ),
            (
                "DISK",
                disk_usage,
                DISK_THRESHOLD,
            ),
        ]

        for metric, value, threshold in metrics:

            if value is None:
                continue

            if value >= threshold:

                self._create_or_update_alert(
                    device=device,
                    metric=metric,
                    value=value,
                    threshold=threshold,
                )

            else:

                self._resolve_alert(
                    device_id=device.id,
                    metric=metric,
                )

    # CREATE OR UPDATE ALERT
    def _create_or_update_alert(
        self,
        device: Device,
        metric: str,
        value: float,
        threshold: float,
    ):

        existing = self.alert_repository.get_open_alerts(
            device_id=device.id,
            metric=metric,
        )

        if existing:

            existing.metric_value = value
            existing.threshold = threshold

            self.db.flush()

            return existing

        alert = Alert(
            device_id=device.id,
            severity=AlertSeverity.CRITICAL,
            title=f"High {metric} Usage",
            message=(
                f"{device.name} {metric.lower()} usage "
                f"has reached {value:.1f}%, "
                f"exceeding the configured threshold "
                f"of {threshold:.1f}%."
            ),
            metric=metric,
            metric_value=value,
            threshold=threshold,
        )

        return self.alert_repository.create(alert)

    # RESOLVE ALERT
    def _resolve_alert(
        self,
        device_id: int,
        metric: str,
    ):

        alert = self.alert_repository.get_open_alerts(
            device_id,
            metric,
        )

        if alert:

            self.alert_repository.resolve(alert)

    # GET LATEST ALERTS
    def get_latest(
        self,
        limit: int = 20,
    ):

        return self.alert_repository.latest(limit)

    # GET OPEN ALERTS
    def get_open_alerts(self):

        return self.alert_repository.unresolved()

    # ACKNOWLEDGE
    def acknowledge(
        self,
        alert_id: int,
    ):

        alert = self.alert_repository.get_by_id(alert_id)

        if alert is None:
            return None

        return self.alert_repository.acknowledge(alert)

    # RESOLVE
    def resolve(
        self,
        alert_id: int,
    ):

        alert = self.alert_repository.get_by_id(alert_id)

        if alert is None:
            return None

        return self.alert_repository.resolve(alert)
