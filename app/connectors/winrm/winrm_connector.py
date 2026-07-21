import socket
from typing import Optional

import winrm
from requests.exceptions import ConnectTimeout, ConnectionError

from app.connectors.base.base_connector import BaseConnector
from app.core.logger import logger
from app.core.exceptions import (
    AuthenticationException,
    ConnectionTimeoutException,
    HostUnreachableException,
    ConnectionException,
)


class WinRMConnector(BaseConnector):
    """
    Handles Windows Remote Management (WinRM).

    Responsibilities
    ----------------
    • Establish WinRM session
    • Execute PowerShell / CMD commands
    • Close session

    Similar interface as SSHConnector so higher
    layers remain platform independent.
    """

    def __init__(
        self,
        hostname: str,
        username: str,
        password: str,
        port: int = 5985,
        transport: str = "ntlm",
        use_ssl: bool = False,
        timeout: int = 15,
    ):

        self.hostname = hostname
        self.username = username
        self.password = password
        self.port = port
        self.transport = transport
        self.use_ssl = use_ssl
        self.timeout = timeout

        self.session: Optional[winrm.Session] = None

    # Connection
    def connect(self):

        if self.session:
            return

        protocol = "https" if self.use_ssl else "http"

        endpoint = f"{protocol}://{self.hostname}:{self.port}/wsman"

        try:
            self.session = winrm.Session(
                target=endpoint,
                auth=(
                    self.username,
                    self.password,
                ),
                transport=self.transport,
            )

            # Validate credentials / connectivity

            result = self.session.run_cmd("hostname")

            if result.status_code != 0:

                stderr = result.std_err.decode().strip()

                raise AuthenticationException(
                    stderr or "Unable to authenticate using WinRM."
                )

            logger.info("WinRM Connected -> %s", self.hostname)

        except ConnectTimeout:
            logger.warning("WinRM timeout.")

            raise ConnectionTimeoutException()

        except ConnectionError:
            logger.warning("Host unreachable.")
            raise HostUnreachableException()

        except socket.timeout:
            logger.warning("Socket timeout.")
            raise ConnectionTimeoutException()

        except Exception as e:
            logger.exception("Unexpected WinRM error")
            raise ConnectionException(str(e))

    # Execute Command
    def execute(
        self,
        command: str,
    ) -> str:

        if self.session is None:
            self.connect()

        result = self.session.run_cmd(command)

        output = result.std_out.decode().strip()

        error = result.std_err.decode().strip()

        if result.status_code != 0:

            logger.warning(error)

            raise ConnectionException(error or "Command execution failed.")

        return output

    # Execute With Exit Code
    def execute_with_status(
        self,
        command: str,
    ):

        if self.session is None:
            self.connect()

        result = self.session.run_cmd(command)

        return (
            result.status_code,
            result.std_out.decode(),
            result.std_err.decode(),
        )

    # PowerShell
    def execute_powershell(
        self,
        script: str,
    ) -> str:

        if self.session is None:
            self.connect()

        result = self.session.run_ps(script)

        output = result.std_out.decode().strip()

        error = result.std_err.decode().strip()

        if result.status_code != 0:

            raise ConnectionException(error or "PowerShell execution failed.")

        return output

    # Disconnect
    def disconnect(self):

        self.session = None

        logger.info(
            "WinRM Closed -> %s",
            self.hostname,
        )
