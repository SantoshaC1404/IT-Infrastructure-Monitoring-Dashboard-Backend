from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.server_inventory import ServerInventory
from app.repositories.base_repository import BaseRepository


class ServerInventoryRepository(BaseRepository[ServerInventory]):

    def __init__(self, db: Session):
        super().__init__(db)

    def create(
        self,
        inventory: ServerInventory,
    ):
        self.add(inventory)

        return inventory

    def get_by_server_id(
        self,
        server_id: int,
    ):

        stmt = select(ServerInventory).where(ServerInventory.server_id == server_id)

        return self.db.scalar(stmt)

    def get_by_id(self, inventory_id: int) -> ServerInventory | None:

        return self.db.get(ServerInventory, inventory_id)

    def update(
        self,
        inventory: ServerInventory,
    ):

        self.db.flush()

        return inventory
