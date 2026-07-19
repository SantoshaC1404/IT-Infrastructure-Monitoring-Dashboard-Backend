from app.connectors.rest.rest_connector import RESTConnector
from app.connectors.snmp.snmp_connector import SNMPConnector
from app.connectors.ssh.ssh_connector import SSHConnector
from app.connectors.winrm.winrm_connector import WinRMConnector
from app.models.device import Device
from app.utils.enums import (
    ConnectionProtocol,
)


class ConnectorFactory:

    @staticmethod
    def create(device: Device):

        if device.device_type == ConnectionProtocol.SSH:

            return SSHConnector(
                hostname=device.ip_address,
                username=device.username,
                password=device.password,
                port=device.port,
            )

        if device.device_type == ConnectionProtocol.WINRM:

            return WinRMConnector(
                hostname=device.ip_address,
                username=device.username,
                password=device.password,
                port=device.port,
            )

        if device.device_type == ConnectionProtocol.REST:

            return RESTConnector(
                hostname=device.ip_address,
                username=device.username,
                password=device.password,
                port=device.port,
            )

        if device.device_type == ConnectionProtocol.SNMP:

            return SNMPConnector(
                hostname=device.ip_address,
                username=device.username,
                password=device.password,
                port=device.port,
            )

        raise ValueError(f"Unsupported connection protocol: {device.device_type}")
