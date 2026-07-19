from __future__ import annotations

import winrm

from app.connections.base import BaseConnection


class WinRMConnection(BaseConnection):

    def __init__(
        self,
        hostname: str,
        username: str,
        password: str,
        port: int = 5985,
        transport: str = "ntlm",
    ):
        self.hostname = hostname
        self.username = username
        self.password = password

        self.port = port
        self.transport = transport

        self.session: winrm.Session | None = None

    def connect(self) -> None:

        endpoint = f"http://{self.hostname}:{self.port}/wsman"

        self.session = winrm.Session(
            target=endpoint,
            auth=(
                self.username,
                self.password,
            ),
            transport=self.transport,
        )

    def disconnect(self):

        self.session = None

    def execute(
        self,
        command: str,
    ) -> str:

        if self.session is None:
            raise RuntimeError("WinRM connection not established.")

        result = self.session.run_ps(command)

        return result.std_out.decode().strip()

    def execute_with_status(
        self,
        command: str,
    ):

        if self.session is None:
            raise RuntimeError("WinRM connection not established.")

        result = self.session.run_ps(command)

        return (
            result.status_code,
            result.std_out.decode(),
            result.std_err.decode(),
        )

    def __enter__(self):

        self.connect()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):

        self.disconnect()
