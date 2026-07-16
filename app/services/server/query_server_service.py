from sqlalchemy.orm import Session

from app.core.exceptions import ResourceNotFoundException
from app.models.server import Server
from app.repositories.server_repository import ServerRepository


class QueryServerService:

    def __init__(self, db: Session):
        self.server_repository = ServerRepository(db)

    def get_all_servers(self) -> list[Server]:

        return self.server_repository.get_all()

    def get_server_by_id(self, server_id: int) -> Server:

        server = self.server_repository.get_by_id(server_id)

        if server is None:
            raise ResourceNotFoundException(
                "Server",
                server_id,
            )

        return server
