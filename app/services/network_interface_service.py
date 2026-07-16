from sqlalchemy.orm import Session

from app.repositories.network_interface_repository import (
    NetworkInterfaceRepository,
)


class NetworkInterfaceService:

    def __init__(self, db: Session):
        self.repository = NetworkInterfaceRepository(db)

    def create_interfaces(self, server_id: int, interfaces):

        return self.repository.create_many(server_id, interfaces)

    def replace_interfaces(self, server_id: int, interfaces):

        self.repository.delete_by_server(server_id)

        return self.repository.create_many(server_id, interfaces)
