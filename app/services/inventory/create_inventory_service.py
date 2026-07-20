from sqlalchemy.orm import Session

from app.repositories.inventory_repository import (
    DeviceInventoryRepository,
)
from app.services.inventory.inventory_factory import InventoryFactory


class CreateInventoryService:

    def __init__(self, db: Session):
        self.repository = DeviceInventoryRepository(db)

    def create_inventory(
        self,
        device_id: int,
        inventory,
        device_type,
    ):
        db_inventory = InventoryFactory.build(
            device_id=device_id,
            inventory=inventory,
            device_type=device_type,
        )

        return self.repository.create(db_inventory)
