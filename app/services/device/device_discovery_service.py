from app.connectors.connector_factory import ConnectorFactory

from app.core.exceptions.discovery import DiscoveryException
from app.discovery.discovery_factory import DiscoveryFactory
from app.dto.discovery_result import DiscoveryResult
from app.schemas.device import DeviceCreate
from app.core.logger import logger


class DeviceDiscoveryService:

    @staticmethod
    def discover_device(
        request: DeviceCreate,
    ) -> DiscoveryResult:

        try:

            connector = ConnectorFactory.create(
                device_type=request.device_type,
                hostname=request.ip_address,
                username=request.username,
                password=request.password,
                port=request.ssh_port,
            )

            with connector:

                discovery = DiscoveryFactory.create(
                    device_type=request.device_type,
                    connector=connector,
                )

                return discovery.discover()

        except DiscoveryException:
            # logger.exception("Unexpected discovery error")
            raise
