from __future__ import annotations

import paramiko

from app.connectors import BaseConnector


class SSHConnection(BaseConnector):

    def __init__(
        self,
        hostname: str,
        username: str,
        password: str,
        port: int = 22,
        timeout: int = 10,
    ):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.port = port
        self.timeout = timeout

        self.client: paramiko.SSHClient | None = None

    def connect(self) -> None:

        self.client = paramiko.SSHClient()

        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        self.client.connect(
            hostname=self.hostname,
            username=self.username,
            password=self.password,
            port=self.port,
            timeout=self.timeout,
        )

    def disconnect(self) -> None:

        if self.client:
            self.client.close()
            self.client = None

    def execute(
        self,
        command: str,
    ) -> str:

        if self.client is None:
            raise RuntimeError("SSH connection is not established.")

        stdin, stdout, stderr = self.client.exec_command(command)

        return stdout.read().decode().strip()

    def execute_with_status(
        self,
        command: str,
    ) -> tuple[int, str, str]:

        if self.client is None:
            raise RuntimeError("SSH connection is not established.")

        stdin, stdout, stderr = self.client.exec_command(command)

        status = stdout.channel.recv_exit_status()

        return (
            status,
            stdout.read().decode(),
            stderr.read().decode(),
        )

    def __enter__(self):

        self.connect()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):

        self.disconnect()
