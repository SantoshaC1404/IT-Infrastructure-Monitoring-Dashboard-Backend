from app.services.ssh_service import SSHService
from app.core.encryption import encryption_service 


class ConnectionService:

    @staticmethod
    def connect(server):

        return SSHService(
            hostname=server.ip_address,
            username=server.username,
            password=encryption_service.decrypt(server.encrypted_password),
            port=server.ssh_port,
        )
