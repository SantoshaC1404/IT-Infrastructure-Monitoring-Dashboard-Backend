import socket
from typing import Optional

import paramiko
from paramiko.ssh_exception import (
    AuthenticationException,
    NoValidConnectionsError,
    SSHException,
    BadHostKeyException,
)

from app.connectors.base.base_connector import BaseConnector
from app.core.logger import logger

from app.core.exceptions import (
    AuthenticationException,
    ConnectionTimeoutException,
    HostUnreachableException,
    ConnectionException,
)
from app.dto.command.command_dto import Command


class SSHConnector(BaseConnector):
    """
    Handles SSH connections and command execution.

    This service is responsible only for:

    - Opening SSH connection
    - Executing commands
    - File transfer
    - Closing SSH connection
    """

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

        self.client: Optional[paramiko.SSHClient] = None

    # Connection
    def connect(self):
        if self.client:
            return

        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            client.connect(
                hostname=self.hostname,
                port=self.port,
                username=self.username,
                password=self.password,
                timeout=self.timeout,
                banner_timeout=self.timeout,
                auth_timeout=self.timeout,
            )

            self.client = client

            logger.info("Connected to %s", self.hostname)

        except AuthenticationException:
            raise ConnectionException("Invalid SSH username or password.")

        except socket.timeout:
            raise ConnectionTimeoutException()

        except NoValidConnectionsError:
            raise ConnectionException(
                "Unable to connect to the device. Verify the IP address, SSH port, and ensure the SSH service is running."
            )

        except OSError:
            raise HostUnreachableException()

        except SSHException:
            raise ConnectionException("SSH protocol error.")

        except BadHostKeyException:
            raise ConnectionException("SSH host key verification failed.")

        except Exception:
            raise ConnectionException()

    # Command Execution
    def execute(self, command: Command) -> str:

        if self.client is None:
            self.connect()

        stdin, stdout, stderr = self.client.exec_command(command.command)

        output = stdout.read().decode().strip()
        error = stderr.read().decode().strip()

        if error:
            logger.warning(error)

        return output

    # Execute With Exit Code
    def execute_with_status(self, command: str):

        if self.client is None:
            self.connect()

        stdin, stdout, stderr = self.client.exec_command(command)
        exit_status = stdout.channel.recv_exit_status()
        output = stdout.read().decode()
        error = stderr.read().decode()

        return exit_status, output, error

    # SFTP
    def upload_file(self, local_path: str, remote_path: str):

        if self.client is None:
            self.connect()

        sftp = self.client.open_sftp()
        sftp.put(local_path, remote_path)
        sftp.close()

    def download_file(self, remote_path: str, local_path: str):

        if self.client is None:
            self.connect()

        sftp = self.client.open_sftp()
        sftp.get(remote_path, local_path)
        sftp.close()

    # Close
    def disconnect(self):

        if self.client:
            self.client.close()
            self.client = None

            logger.info("SSH Closed -> %s", self.hostname)
