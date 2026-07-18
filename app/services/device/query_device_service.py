from sqlalchemy.orm import Session

from app.core.exceptions import ResourceNotFoundException
from app.models.device import Server
from app.repositories.device_repository import ServerRepository
from app.core.logger import logger


class QueryServerService:

    def __init__(self, db: Session):
        self.server_repository = ServerRepository(db)

    # GET ALL SERVER
    def get_all_servers(self) -> list[Server]:

        return self.server_repository.get_all()

    # GET BY ID
    def get_server_by_id(self, server_id: int) -> Server:

        server = self.server_repository.get_by_id(server_id)
        # logger.info(f"Server by ip: ${server}")
        logger.info(server)

        if server is None:
            raise ResourceNotFoundException(
                "Server",
                server_id,
            )

        return server

    # GET BY IP
    def get_server_by_ip(self, ip_address: str) -> Server:

        server = self.server_repository.get_by_ip(ip_address)

        if server is None:
            raise ResourceNotFoundException(
                "Server",
                ip_address,
            )

        return server
