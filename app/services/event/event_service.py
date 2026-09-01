from app.models.device import Device
from app.models.event import Event

from app.repositories.event_repository import EventRepository

from app.utils.enums import (
    EventSeverity,
    EventType,
)


class EventService:

    def __init__(self, db):

        self.event_repository = EventRepository(db)

    def create_metric_event(
        self,
        device: Device,
        metric: str,
        value: float,
        threshold: float,
        severity: EventSeverity = EventSeverity.CRITICAL,
    ):

        event = Event(
            device_id=device.id,
            event_type=EventType.METRIC_THRESHOLD,
            severity=severity,
            metric=metric,
            current_value=value,
            threshold=threshold,
            title=f"High {metric} Usage",
            message=(
                f"{device.name} {metric.lower()} usage "
                f"is currently {value:.1f}%, "
                f"which exceeds the configured threshold "
                f"of {threshold:.1f}%."
            ),
        )

        return self.event_repository.create(event)

    def create_device_offline_event(
        self,
        device: Device,
    ):

        event = Event(
            device_id=device.id,
            event_type=EventType.DEVICE_OFFLINE,
            severity=EventSeverity.CRITICAL,
            title="Device Offline",
            message=(f"{device.name} is currently offline."),
        )

        return self.event_repository.create(event)

    def create_device_online_event(
        self,
        device: Device,
    ):

        event = Event(
            device_id=device.id,
            event_type=EventType.DEVICE_ONLINE,
            severity=EventSeverity.INFO,
            title="Device Online",
            message=(f"{device.name} is back online."),
        )

        return self.event_repository.create(event)

    def get_latest(
        self,
        limit: int = 50,
    ):

        return self.event_repository.latest(limit)

    def get_device_events(
        self,
        device_id: int,
        limit: int = 50,
    ):

        return self.event_repository.get_by_device(
            device_id=device_id,
            limit=limit,
        )
