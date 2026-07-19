from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from app.core import logger
from app.core.exceptions import DatabaseException
from app.models.device import Device
from app.repositories.device_repository import DeviceRepository
from app.schemas.device import DeviceCreate
from app.services.disk.disk_service import DiskService
from app.services.inventory.inventory_service import InventoryService
from app.services.network_interface.network_interface_service import (
    NetworkInterfaceService,
)
from app.services.device.device_discovery_service import DeviceDiscoveryService
from app.services.device.validation_service import DeviceValidationService
from app.services.device.device_factory import DeviceFactory


class CreateDeviceService:

    def __init__(self, db: Session):
        self.db = db
        self.device_repository = DeviceRepository(db)
        self.validation_service = DeviceValidationService(db)
        self.discovery_service = DeviceDiscoveryService
        self.inventory_service = InventoryService(db)
        self.disk_service = DiskService(db)
        self.network_service = NetworkInterfaceService(db)

    def create_device(self, request: DeviceCreate) -> Device:

        self.validation_service.validate_duplicate_ip(
            request.ip_address,
        )

        discovery = self.discovery_service.discover_device(request)

        device = DeviceFactory.build(request)

        self.server_repository.create(
            device,
            commit=False,
        )

        self.db.flush()

        self.inventory_service.save_inventory(
            device.id,
            discovery.inventory,
        )

        self.disk_service.create_disks(
            device.id,
            discovery.disks,
        )

        self.network_service.create_interfaces(
            device.id,
            discovery.interfaces,
        )

        self.db.commit()

        self.db.refresh(device)

        return device
