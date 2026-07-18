from sqlalchemy.orm import Session

from app.models.device import Server
from app.schemas.server import ServerCreate, ServerUpdate
from app.services.server.create_server_service import CreateServerService
from app.services.server.delete_server_service import DeleteServerService
from app.services.server.monitoring_server_service import (
    MonitoringServerService,
)
from app.services.server.query_server_service import QueryServerService
from app.services.server.update_server_service import UpdateServerService


class ServerService:

    def __init__(self, db: Session):

        self.create_service = CreateServerService(db)
        self.query_service = QueryServerService(db)
        self.update_service = UpdateServerService(db)
        self.delete_service = DeleteServerService(db)
        self.monitoring_service = MonitoringServerService(db)

    # CREATE
    def create_server(
        self,
        request: ServerCreate,
    ) -> Server:

        return self.create_service.create_server(request)

    # READ
    def get_all_servers(self) -> list[Server]:

        return self.query_service.get_all_servers()

    def get_server_by_id(
        self,
        server_id: int,
    ) -> Server:

        return self.query_service.get_server_by_id(server_id)

    def get_server_by_ip(
        self,
        ip_address: str,
    ) -> Server:

        return self.query_service.get_server_by_ip(ip_address)

    # UPDATE
    def update_server(
        self,
        server_id: int,
        request: ServerUpdate,
    ) -> Server:

        return self.update_service.update_server(
            server_id,
            request,
        )

    # DELETE BY ID
    def delete_server_by_id(
        self,
        server_id: int,
    ):

        self.delete_service.delete_server_id(server_id)

    # DELETE BY IP
    def delete_server_by_ip(
        self,
        ip_address: str,
    ):

        self.delete_service.delete_server_ip(ip_address)

    # MONITORING
    def enable_monitoring(
        self,
        server_id: int,
    ) -> Server:

        return self.monitoring_service.enable_monitoring(server_id)

    def disable_monitoring(
        self,
        server_id: int,
    ) -> Server:

        return self.monitoring_service.disable_monitoring(server_id)
