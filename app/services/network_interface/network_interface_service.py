from sqlalchemy.orm import Session

from app.services.network_interface.create_network_interface_service import (
    CreateNetworkInterfaceService,
)
from app.services.network_interface.query_network_interface_service import (
    QueryNetworkInterfaceService,
)
from app.services.network_interface.replace_network_interface_service import (
    ReplaceNetworkInterfaceService,
)


class NetworkInterfaceService:

    def __init__(self, db: Session):

        self.create_service = CreateNetworkInterfaceService(db)

        self.replace_service = ReplaceNetworkInterfaceService(db)

        self.query_service = QueryNetworkInterfaceService(db)

    # -----------------------------------
    # Create
    # -----------------------------------

    def create_interfaces(
        self,
        device_id: int,
        interfaces,
    ):
        return self.create_service.create_interfaces(
            device_id,
            interfaces,
        )

    # -----------------------------------
    # Replace
    # -----------------------------------

    def replace_interfaces(
        self,
        device_id: int,
        interfaces,
    ):
        return self.replace_service.replace_interfaces(
            device_id,
            interfaces,
        )

    # -----------------------------------
    # Query
    # -----------------------------------

    def get_by_device_id(
        self,
        device_id: int,
    ):
        return self.query_service.get_by_device_id(
            device_id,
        )

    def get_by_interface_id(
        self,
        interface_id: int,
    ):
        return self.query_service.get_by_interface_id(
            interface_id,
        )
