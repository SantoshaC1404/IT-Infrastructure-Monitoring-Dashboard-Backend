from sqlalchemy.orm import Session

from app.repositories.inventory_repository import (
    ServerInventoryRepository,
)
from app.services.inventory.inventory_factory import InventoryFactory



class CreateInventoryService:

    def __init__(self, db: Session):
        self.repository = ServerInventoryRepository(db)

    def create_inventory(
        self,
        server_id: int,
        inventory,
    ):
        # return self.repository.create(
        #     server_id=server_id,
        #     inventory=inventory,
        # )
        db_inventory=InventoryFactory.build(
            server_id=server_id,
            inventory=inventory,
        )
        
        return self.repository.create(db_inventory)
