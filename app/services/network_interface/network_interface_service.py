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
        server_id: int,
        interfaces,
    ):
        return self.create_service.create_interfaces(
            server_id,
            interfaces,
        )

    # -----------------------------------
    # Replace
    # -----------------------------------

    def replace_interfaces(
        self,
        server_id: int,
        interfaces,
    ):
        return self.replace_service.replace_interfaces(
            server_id,
            interfaces,
        )

    # -----------------------------------
    # Query
    # -----------------------------------

    def get_by_server(
        self,
        server_id: int,
    ):
        return self.query_service.get_by_server(
            server_id,
        )

    def get_by_id(
        self,
        interface_id: int,
    ):
        return self.query_service.get_by_id(
            interface_id,
        )