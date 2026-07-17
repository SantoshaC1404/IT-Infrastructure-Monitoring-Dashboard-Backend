from sqlalchemy.orm import Session

from app.repositories.network_interface_repository import NetworkInterfaceRepository


class CreateNetworkInterfaceService:

    def __init__(self, db: Session):
        self.repository = NetworkInterfaceRepository(db=db)

    def create_interfaces(
        self,
        server_id: int,
        interfaces,
    ):
        return self.repository.create_many(
            server_id=server_id,
            interfaces=interfaces,
        )
