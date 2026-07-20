from datetime import datetime

from app.core.encryption import encryption_service
from app.models.device import Device
from app.schemas.device import DeviceCreate
from app.utils.enums import DeviceStatus, DeviceType


class DeviceFactory:

    @staticmethod
    def build(
        request: DeviceCreate,
        device_type: DeviceType,
    ) -> Device:

        return Device(
            name=request.name,
            ip_address=request.ip_address,
            ssh_port=request.ssh_port,
            username=request.username,
            encrypted_password=encryption_service.encrypt(
                request.password,
            ),
            device_type=device_type,
            monitoring_enabled=True,
            status=DeviceStatus.ONLINE,
            last_seen=datetime.utcnow(),
        )
