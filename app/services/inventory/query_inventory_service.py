from sqlalchemy.orm import Session

from app.repositories.inventory_repository import (
    DeviceInventoryRepository,
)


class QueryInventoryService:

    def __init__(self, db: Session):
        self.repository = DeviceInventoryRepository(db)

    def get_by_device(
        self,
        device_id: int,
    ):
        return self.repository.get_by_device_id(
            device_id,
        )

    def get_by_id(
        self,
        inventory_id: int,
    ):
        return self.repository.get_by_id(
            inventory_id,
        )
