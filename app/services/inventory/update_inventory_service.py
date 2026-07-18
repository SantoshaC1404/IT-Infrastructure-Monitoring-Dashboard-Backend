from sqlalchemy.orm import Session

from app.repositories.inventory_repository import (
    DeviceInventoryRepository,
)


class UpdateInventoryService:

    def __init__(self, db: Session):
        self.repository = DeviceInventoryRepository(db)

    def update_inventory(
        self,
        device_id: int,
        inventory,
    ):

        existing = self.repository.get_by_device_id(
            device_id,
        )

        if existing:

            return self.repository.update(
                existing,
                inventory,
            )

        return self.repository.create(
            device_id=device_id,
            inventory=inventory,
        )
