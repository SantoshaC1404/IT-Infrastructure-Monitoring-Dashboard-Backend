from sqlalchemy.orm import Session

from app.repositories.device_repository import DeviceRepository
from app.services.device.validation_service import DeviceValidationService


class MonitoringDeviceService:

    def __init__(self, db: Session):
        self.db = db
        self.device_repository = DeviceRepository(db)
        self.validation_service = DeviceValidationService(db)

    def enable_monitoring(self, device_id: int):

        return self._set_monitoring(device_id, True)

    def disable_monitoring(self, device_id: int):

        return self._set_monitoring(device_id, False)

    def _set_monitoring(
        self,
        device_id: int,
        enabled: bool,
    ):

        device = self.validation_service.get_device_by_id(device_id)

        device.monitoring_enabled = enabled

        self.db.commit()

        self.db.refresh(device)

        return device
