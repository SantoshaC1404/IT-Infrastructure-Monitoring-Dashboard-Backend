from sqlalchemy.orm import Session

from app.models.server import Server, ServerStatus
from app.repositories.server_repository import ServerRepository
from app.schemas.server import ServerCreate
from app.services.ssh_service import SSHService


class ServerService:

    def __init__(self, db: Session):
        self.repo = ServerRepository(db)

    def create(self, data: ServerCreate):

        online = SSHService.test_connection(
            hostname=data.hostname,
            port=data.ssh_port,
            username=data.username,
            password=data.password,
        )

        status = ServerStatus.ONLINE if online else ServerStatus.OFFLINE

        server = Server(
            **data.model_dump(),
            status=status,
        )

        return self.repo.create(server)

    def get_all(self):
        return self.repo.get_all()
