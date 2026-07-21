from sqlalchemy.orm import Session

from app.services.disk.disk_service import DiskService
from app.services.inventory.inventory_service import InventoryService
from app.services.network_interface.network_interface_service import (
    NetworkInterfaceService,
)


class DevicePersistenceService:
    """
    Persists everything discovered for a device.

    Responsible for

    • Inventory
    • Disks
    • Network Interfaces

    All within a single transaction.
    """

    def __init__(self, db: Session):

        self.db = db

        self.inventory_service = InventoryService(db)

        self.disk_service = DiskService(db)

        self.network_service = NetworkInterfaceService(db)

    def save(
        self,
        device,
        discovery,
    ):

        self.db.flush()
        print("Device flushed")

        self.inventory_service.save_inventory(
            device.id,
            discovery.inventory,
            device.device_type,
        )

        self.db.flush()
        # print("Inventory saved")

        self.disk_service.create_disks(
            device.id,
            discovery.disks,
        )

        self.db.flush()
        # print("Disks saved")

        self.network_service.create_interfaces(
            device.id,
            discovery.interfaces,
        )

        self.db.flush()
        # print("Interfaces saved")

        self.db.commit()

        self.db.refresh(device)

        return device
