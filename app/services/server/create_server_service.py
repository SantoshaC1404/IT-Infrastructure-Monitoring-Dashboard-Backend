from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from app.core import logger
from app.core.exceptions import DatabaseException
from app.models.device import Server
from app.repositories.server_repository import ServerRepository
from app.schemas.device import ServerCreate
from app.services.disk.disk_service import DiskService
from app.services.inventory.inventory_service import InventoryService
from app.services.network_interface.network_interface_service import (
    NetworkInterfaceService,
)
from app.services.server.discovery_service import ServerDiscoveryService
from app.services.server.validation_service import ServerValidationService
from app.services.server.server_factory import ServerFactory


class CreateServerService:

    def __init__(self, db: Session):
        self.db = db
        self.server_repository = ServerRepository(db)
        self.validation_service = ServerValidationService(db)
        self.discovery_service = ServerDiscoveryService
        self.inventory_service = InventoryService(db)
        self.disk_service = DiskService(db)
        self.network_service = NetworkInterfaceService(db)

    def create_server(self, request: ServerCreate) -> Server:

        self.validation_service.validate_duplicate_ip(
            request.ip_address,
        )

        discovery = self.discovery_service.discover_server(request)

        server = ServerFactory.build(request)

        self.server_repository.create(
            server,
            commit=False,
        )

        self.db.flush()

        self.inventory_service.save_inventory(
            server.id,
            discovery.inventory,
        )

        self.disk_service.create_disks(
            server.id,
            discovery.disks,
        )

        self.network_service.create_interfaces(
            server.id,
            discovery.interfaces,
        )

        self.db.commit()

        self.db.refresh(server)

        return server
