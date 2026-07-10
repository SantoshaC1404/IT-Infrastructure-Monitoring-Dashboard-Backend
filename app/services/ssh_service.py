import paramiko

from app.core.encryption import encryption_service
from app.models import Server


class SSHService:

    @staticmethod
    def test_connection(
        hostname: str,
        port: int,
        username: str,
        password: str,
    ):
        """Test the SSH connection to a server.
        Args:
            hostname (str): The hostname or IP address of the server.
            port (int): The SSH port number.
            username (str): The SSH username.
            password (str): The SSH password.
        Returns:
            bool: True if the connection is successful, False otherwise.
        """

        ssh = paramiko.SSHClient()

        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        password = encryption_service.decrypt(Server.encrypted_password)

        try:

            ssh.connect(
                hostname=Server.hostname,
                port=Server.ssh_port,
                username=Server.username,
                password=password,
                timeout=5,
            )

            ssh.close()

            return True

        except Exception:
            return False
