from sqlalchemy.orm import Session

from app.repositories.network_interface_repository import NetworkInterfaceRepository


class ReplaceNetworkInterfaceService:

    def __init__(self, db: Session):
        self.repository = NetworkInterfaceRepository(db)

    def replace_interfaces(
        self,
        device_id: int,
        interfaces,
    ):

        self.repository.delete_by_device_id(
            device_id,
        )

        return self.repository.create_many(
            device_id=device_id,
            interfaces=interfaces,
        )
