from sqlalchemy.orm import Session

from app.repositories.network_interface_repository import (
    NetworkInterfaceRepository,
)


class QueryNetworkInterfaceService:

    def __init__(self, db: Session):
        self.repository = NetworkInterfaceRepository(db)

    def get_by_device_id(
        self,
        device_id: int,
    ):
        return self.repository.get_by_device_id(
            device_id,
        )

    def get_by_interface_id(
        self,
        interface_id: int,
    ):
        return self.repository.get_by_interface_id(
            interface_id,
        )
