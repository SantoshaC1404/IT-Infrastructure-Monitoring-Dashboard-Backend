from sqlalchemy.orm import Session

from app.core.exceptions import ResourceNotFoundException, ServerAlreadyExistsException
from app.repositories.server_repository import ServerRepository


class ServerValidationService:

    def __init__(self, db: Session):
        self.server_repository = ServerRepository(db)

    def validate_duplicate_ip(self, ip_address: str):

        if self.server_repository.get_by_ip(ip_address):
            raise ServerAlreadyExistsException(ip_address)

    def get_server_by_id(self, server_id: int):

        server = self.server_repository.get_by_id(server_id)

        if server is None:
            raise ResourceNotFoundException(
                "Server",
                server_id,
            )

        return server
