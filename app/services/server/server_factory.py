from datetime import datetime

from app.core.encryption import encryption_service
from app.models.device import Server
from app.schemas.server import ServerCreate
from app.utils.enums import ServerStatus


class ServerFactory:

    @staticmethod
    def build(request: ServerCreate) -> Server:

        return Server(
            name=request.name,
            ip_address=request.ip_address,
            ssh_port=request.ssh_port,
            username=request.username,
            encrypted_password=encryption_service.encrypt(
                request.password,
            ),
            monitoring_enabled=True,
            status=ServerStatus.ONLINE,
            last_seen=datetime.utcnow(),
        )
