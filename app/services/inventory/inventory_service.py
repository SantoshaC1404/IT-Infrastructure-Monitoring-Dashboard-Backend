from sqlalchemy.orm import Session

from app.services.inventory.create_inventory_service import (
    CreateInventoryService,
)
from app.services.inventory.update_inventory_service import (
    UpdateInventoryService,
)
from app.services.inventory.query_inventory_service import (
    QueryInventoryService,
)


class InventoryService:

    def __init__(self, db: Session):

        self.create_service = CreateInventoryService(db)

        self.update_service = UpdateInventoryService(db)

        self.query_service = QueryInventoryService(db)

    # -----------------------------------------
    # Create
    # -----------------------------------------

    def save_inventory(
        self,
        device_id: int,
        inventory,
        device_type,
    ):
        return self.create_service.create_inventory(
            device_id,
            inventory,
            device_type,
        )

    # -----------------------------------------
    # Update
    # -----------------------------------------

    def update_inventory(
        self,
        device_id: int,
        inventory,
    ):
        return self.update_service.update_inventory(
            device_id,
            inventory,
        )

    # -----------------------------------------
    # Query
    # -----------------------------------------

    def get_by_device(
        self,
        device_id: int,
    ):
        return self.query_service.get_by_device(
            device_id,
        )

    def get_by_id(
        self,
        inventory_id: int,
    ):
        return self.query_service.get_by_id(
            inventory_id,
        )
