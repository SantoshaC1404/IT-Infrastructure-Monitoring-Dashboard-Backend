from sqlalchemy.orm import Session

from app.models.server import Server, ServerStatus
from app.repositories.server_repository import ServerRepository
from app.schemas.server import ServerCreate
from app.services.ssh_service import SSHService
from app.core.encryption import encryption_service


class ServerService:
    def __init__(self, db: Session):
        """Service for managing server-related operations."""
        self.db = db
        self.server_repository = ServerRepository(db)
        self.ssh_service = SSHService()

    def create_server(self, server_create: ServerCreate):
        """Create a new server after validating the input and testing SSH connection.
        Args:
            server_create (ServerCreate): The server creation data.
        Returns:
            Server: The created server instance.
        Raises:
            ValueError: If a server with the same IP address already exists.
            ConnectionError: If SSH connection to the server fails.
        """

        # Check if a server with the same IP address already exists
        existing_server = self.server_repository.get_server_by_ip(
            server_create.ip_address
        )
        if existing_server:
            raise ValueError(
                f"A server with IP address {server_create.ip_address} already exists."
            )

        # Test SSH connection to the server
        ssh_connection_successful = self.ssh_service.test_connection(
            hostname=server_create.hostname,
            port=server_create.ssh_port,
            username=server_create.username,
            password=server_create.password,
        )
        if not ssh_connection_successful:
            raise ConnectionError(
                f"Failed to establish SSH connection to {server_create.hostname}."
            )

        # Encrypt the password before storing it
        encrypted_password = encryption_service.encrypt(server_create.password)

        # Create a new Server instance
        new_server = Server(
            name=server_create.name,
            hostname=server_create.hostname,
            ip_address=server_create.ip_address,
            ssh_port=server_create.ssh_port,
            username=server_create.username,
            password=encrypted_password,
            server_type=server_create.server_type,
            status=ServerStatus.ACTIVE,  # Set the initial status to ACTIVE
        )
        return self.server_repository.create(new_server)

    def get_all_servers(self):
        """Retrieve all servers from the database.
        Returns:
            List[Server]: A list of all server instances.
        """
        return self.server_repository.get_all()

    def get_server_by_id(self, server_id: int):
        """Retrieve a server by its ID.
        Args:
            server_id (int): The ID of the server to retrieve.
        Returns:
            Server: The server instance with the specified ID, or None if not found.
        """
        server = self.server_repository.get_by_id(server_id)
        if not server:
            raise ValueError(f"Server with ID {server_id} not found.")

        return server

    def get_server_by_ip(self, ip: str):
        """Retrieve a server by its IP address.
        Args:
            ip (str): The IP address of the server to retrieve.
        Returns:
            Server: The server instance with the specified IP address, or None if not found.
        """
        server = self.server_repository.get_server_by_ip(ip)
        if not server:
            raise ValueError(f"Server with IP address {ip} not found.")

        return server

    def update_server(self, server_id: int, updated_data: dict):
        """Update an existing server with new data.
        Args:
            server_id (int): The ID of the server to update.
            updated_data (dict): A dictionary containing the updated server data.
        Returns:
            Server: The updated server instance.
        Raises:
            ValueError: If the server with the specified ID does not exist.
        """
        server = self.server_repository.get_by_id(server_id)
        if not server:
            raise ValueError(f"Server with ID {server_id} not found.")

        for key, value in updated_data.items():
            setattr(server, key, value)

        return self.server_repository.update(server)

    def delete_server(self, server_id: int):
        """Delete a server by its ID.
        Args:
            server_id (int): The ID of the server to delete.
        Raises:
            ValueError: If the server with the specified ID does not exist.
        """
        server = self.server_repository.get_by_id(server_id)
        if not server:
            raise ValueError(f"Server with ID {server_id} not found.")

        self.server_repository.delete(server)
