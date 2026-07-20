from sqlalchemy.orm import Session

from app.repositories.device_repository import DeviceRepository
from app.services.device.validation_service import DeviceValidationService


class DeleteDeviceService:

    def __init__(self, db: Session):
        self.db = db
        self.device_repository = DeviceRepository(db)
        self.validation_service = DeviceValidationService(db)

    # Delete by ID
    def delete_device_by_id(self, device_id: int):

        device = self.validation_service.get_device_by_id(device_id)

        self.device_repository.delete(
            device,
            commit=False,
        )

        self.db.commit()

    # Delete by IP
    def delete_device_by_ip(self, ip_address: str):

        device = self.validation_service.get_device_by_ip(ip_address)

        self.device_repository.delete(
            device,
            commit=False,
        )

        self.db.commit()
