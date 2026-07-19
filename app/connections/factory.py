from app.connections.ssh import SSHConnection
from app.connections.winrm import WinRMConnection

from app.models.device import Device
from app.utils.enums import (
    ConnectionProtocol,
)


class ConnectionFactory:

    @staticmethod
    def create(device: Device):

        if device.connection_protocol == ConnectionProtocol.SSH:

            return SSHConnection(
                hostname=device.ip_address,
                username=device.username,
                password=device.password,
                port=device.port,
            )

        if device.connection_protocol == ConnectionProtocol.WINRM:

            return WinRMConnection(
                hostname=device.ip_address,
                username=device.username,
                password=device.password,
                port=device.port,
            )

        raise ValueError(
            f"Unsupported connection protocol: {device.connection_protocol}"
        )
