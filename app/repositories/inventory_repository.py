from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.device_inventory import DeviceInventory
from app.repositories.base_repository import BaseRepository


class DeviceInventoryRepository(BaseRepository[DeviceInventory]):

    def __init__(self, db: Session):
        super().__init__(db)

    def create(
        self,
        inventory: DeviceInventory,
    ):
        self.add(inventory)

        return inventory

    def get_by_device_id(
        self,
        device_id: int,
    ):

        stmt = select(DeviceInventory).where(DeviceInventory.device_id == device_id)

        return self.db.scalar(stmt)

    def get_by_id(self, inventory_id: int) -> DeviceInventory | None:

        return self.db.get(DeviceInventory, inventory_id)

    def update(
        self,
        inventory: DeviceInventory,
    ):

        self.db.flush()

        return inventory
