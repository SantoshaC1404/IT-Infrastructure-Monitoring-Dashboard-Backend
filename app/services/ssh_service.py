import paramiko

from app.core.encryption import encryption_service
from app.models import Server


class SSHService:

    def __init__(
        self,
        hostname: str,
        username: str,
        password: str,
        port: int = 22,
    ):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.port = port
        self.client = None

    def connect(self):
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        self.client.connect(
            hostname=self.hostname,
            username=self.username,
            password=self.password,
            port=self.port,
            timeout=5,
        )

    def execute(self, command: str) -> str:
        stdin, stdout, stderr = self.client.exec_command(command)

        return stdout.read().decode().strip()

    def close(self):
        if self.client:
            self.client.close()

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
