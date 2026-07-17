from sqlalchemy.orm import Session

from app.repositories.network_interface_repository import (
    NetworkInterfaceRepository,
)


class QueryNetworkInterfaceService:

    def __init__(self, db: Session):
        self.repository = NetworkInterfaceRepository(db)

    def get_by_server(
        self,
        server_id: int,
    ):
        return self.repository.get_by_server(
            server_id,
        )

    def get_by_id(
        self,
        interface_id: int,
    ):
        return self.repository.get_by_id(
            interface_id,
        )