from datetime import datetime

from app.core.encryption import encryption_service
from app.models.device import Devices
from app.schemas.device import DeviceCreate
from app.utils.enums import DeviceStatus


class DeviceFactory:

    @staticmethod
    def build(request: DeviceCreate) -> Devices:

        return Devices(
            name=request.name,
            ip_address=request.ip_address,
            ssh_port=request.ssh_port,
            username=request.username,
            encrypted_password=encryption_service.encrypt(
                request.password,
            ),
            monitoring_enabled=True,
            status=DeviceStatus.ONLINE,
            last_seen=datetime.utcnow(),
        )
