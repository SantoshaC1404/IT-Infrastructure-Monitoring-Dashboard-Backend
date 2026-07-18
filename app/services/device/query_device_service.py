from sqlalchemy.orm import Session

from app.core.exceptions import ResourceNotFoundException
from app.models.device import Devices
from app.repositories.device_repository import DeviceRepository
from app.core.logger import logger


class QueryDeviceService:

    def __init__(self, db: Session):
        self.device_repository = DeviceRepository(db)

    # GET ALL DEVICES
    def get_all_devices(self) -> list[Devices]:

        return self.device_repository.get_all()

    # GET BY ID
    def get_device_by_id(self, device_id: int) -> Devices:

        device = self.device_repository.get_by_id(device_id)
        # logger.info(f"Device by ip: ${device}")
        logger.info(device)

        if device is None:
            raise ResourceNotFoundException(
                "Device",
                device_id,
            )

        return device

    # GET BY IP
    def get_device_by_ip(self, ip_address: str) -> Devices:

        device = self.device_repository.get_by_ip(ip_address)

        if device is None:
            raise ResourceNotFoundException(
                "Device",
                ip_address,
            )

        return device
