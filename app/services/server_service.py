from sqlalchemy.orm import Session

from app.models.server import Server, ServerStatus
from app.repositories.server_repository import ServerRepository
from app.schemas.server import ServerCreate
from app.services.ssh_service import SSHService
from app.core.encryption import encryption_service


class ServerService:

    def __init__(self, db: Session):
        """Initialize the ServerService with a database session."""
        self.repo = ServerRepository(db)

    def create(self, data: ServerCreate):
        """Create a new server entry in the database.
        Args:
            data (ServerCreate): The server data to be created.
        Returns:
            Server: The created server object.
        """

        # Encrypt the password before storing it
        encrypted_password = encryption_service.encrypt(data.password)

        online = SSHService.test_connection(
            hostname=data.hostname,
            port=data.ssh_port,
            username=data.username,
            password=data.password,
        )

        status = ServerStatus.ONLINE if online else ServerStatus.OFFLINE

        server = Server(
            name=data.name,
            hostname=data.hostname,
            ip_address=data.ip_address,
            ssh_port=data.ssh_port,
            username=data.username,
            encrypted_password=encrypted_password,
            server_type=data.server_type,
            monitoring_enabled=data.monitoring_enabled,
            status=status,
        )

        return self.repo.create(server)

    def get_all(self):
        return self.repo.get_all()
