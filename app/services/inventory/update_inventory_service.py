from sqlalchemy.orm import Session

from app.repositories.inventory_repository import (
    ServerInventoryRepository,
)


class UpdateInventoryService:

    def __init__(self, db: Session):
        self.repository = ServerInventoryRepository(db)

    def update_inventory(
        self,
        server_id: int,
        inventory,
    ):

        existing = self.repository.get_by_server(
            server_id,
        )

        if existing:

            return self.repository.update(
                existing,
                inventory,
            )

        return self.repository.create(
            server_id=server_id,
            inventory=inventory,
        )
