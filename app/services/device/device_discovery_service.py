from app.connectors.connector_factory import ConnectorFactory
from app.core import logger
from app.discovery.discovery_factory import DiscoveryFactory
from app.dto.discovery_result import DiscoveryResult
from app.models.device import Device
from app.schemas.device import DeviceCreate

from app.core.exceptions import (
    AppException,
    DeviceConnectionException,
)


class DeviceDiscoveryService:
    """
    Orchestrates device discovery.

    Responsibilities
    ----------------
    - Create the correct connector
    - Create the correct discovery implementation
    - Execute discovery
    """

    @staticmethod
    def discover_device(
        request: DeviceCreate,
    ) -> DiscoveryResult:

        try:

            connection = ConnectorFactory.create(request)

            with connection:

                discovery = DiscoveryFactory.create(
                    request,
                    connection,
                )

                return discovery.discover()

        except AppException:
            raise

        except Exception:
            logger.exception("Unexpected discovery error")

            raise DeviceConnectionException("Failed to discover device.")
