from app.connectors.ssh.ssh_connector import SSHConnector
from app.connectors.winrm.winrm_connector import WinRMConnector
from app.utils.enums import DeviceType


class ConnectorFactory:

    @staticmethod
    def create(
        device_type: DeviceType,
        hostname: str,
        username: str,
        password: str,
        port: int = 22,
    ):

        if device_type == DeviceType.LINUX:
            return SSHConnector(
                hostname=hostname,
                username=username,
                password=password,
                port=port,
            )

        if device_type == DeviceType.WINDOWS:
            return WinRMConnector(
                hostname=hostname,
                username=username,
                password=password,
            )

        raise ValueError(f"Unsupported device type: {device_type}")
