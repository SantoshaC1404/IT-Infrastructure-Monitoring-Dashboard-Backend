from sqlalchemy.orm import Session

from app.repositories.inventory_repository import (
    ServerInventoryRepository,
)


class QueryInventoryService:

    def __init__(self, db: Session):
        self.repository = ServerInventoryRepository(db)

    def get_by_server(
        self,
        server_id: int,
    ):
        return self.repository.get_by_server_id(
            server_id,
        )

    def get_by_id(
        self,
        inventory_id: int,
    ):
        return self.repository.get_by_id(
            inventory_id,
        )
