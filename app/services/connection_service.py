from app.connections.ssh.ssh_connection import SSHService
from app.core.encryption import encryption_service


class ConnectionService:

    @staticmethod
    def connect(device):

        return SSHService(
            hostname=device.ip_address,
            username=device.username,
            password=encryption_service.decrypt(device.encrypted_password),
            port=device.ssh_port,
        )
