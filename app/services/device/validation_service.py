from sqlalchemy.orm import Session

from app.core.exceptions import ResourceNotFoundException, DeviceAlreadyExistsException
from app.repositories.device_repository import DeviceRepository


class DeviceValidationService:

    def __init__(self, db: Session):
        self.device_repository = DeviceRepository(db)

    def validate_duplicate_ip(self, ip_address: str):

        if self.device_repository.get_by_ip(ip_address):
            raise DeviceAlreadyExistsException(ip_address)

    # Get By ID
    def get_device_by_id(self, device_id: int):

        device = self.device_repository.get_by_id(device_id)

        if device is None:
            raise ResourceNotFoundException(
                "Device",
                device_id,
            )

        return device

    # Get By IP
    def get_device_by_ip(self, ip_address: int):

        device = self.device_repository.get_by_ip(ip_address)

        if device is None:
            raise ResourceNotFoundException(
                "Device",
                ip_address,
            )

        return device
