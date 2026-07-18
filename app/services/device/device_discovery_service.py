from app.core import logger
from app.core.exceptions import AppException, SSHConnectionException
from app.dto.discovery_result import DiscoveryResult
from app.schemas.device import DeviceCreate
from app.services.discovery.discovery_service import DiscoveryService
from app.services.ssh_service import SSHService


class DeviceDiscoveryService:

    @staticmethod
    def discover_device(request: DeviceCreate) -> DiscoveryResult:

        try:
            with SSHService(
                hostname=request.ip_address,
                username=request.username,
                password=request.password,
                port=request.ssh_port,
            ) as ssh:

                discovery_service = DiscoveryService(ssh)

                return discovery_service.discover()

        except AppException:
            raise

        except Exception:
            logger.exception("Unexpected discovery error")
            raise SSHConnectionException("Failed to discover device inventory.")
