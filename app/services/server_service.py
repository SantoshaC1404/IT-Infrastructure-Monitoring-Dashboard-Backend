from __future__ import annotations

import logging

from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.encryption import encryption_service
from app.core.exceptions import (
    AppException,
    DatabaseException,
    ResourceNotFoundException,
    ServerAlreadyExistsException,
    SSHConnectionException,
)
from app.dto.discovery_result import DiscoveryResult
from app.models.server import Server
from app.repositories.server_repository import ServerRepository
from app.schemas.server import ServerCreate, ServerUpdate
from app.services.discovery_service import DiscoveryService
from app.services.disk_service import DiskService
from app.services.inventory_service import InventoryService
from app.services.network_interface_service import NetworkInterfaceService
from app.services.ssh_service import SSHService
from app.utils.enums import ServerStatus

logger = logging.getLogger(__name__)


class ServerService:

    def __init__(self, db: Session):
        self.db = db
        self.server_repository = ServerRepository(db)
        self.inventory_service = InventoryService(db)

    # CREATE SERVER
    def create_server(self, request: ServerCreate) -> Server:

        # logger.info(
        #     "Creating server %s (%s)",
        #     request.name,
        #     request.ip_address,
        # )

        self._validate_duplicate_ip(request.ip_address)

        try:
            # Discover server details over SSH
            discovery = self._discover_server(request)

            # Create Server model
            server = self._build_server_model(request)

            self.server_repository.create(server, commit=False)

            # Generate server.id
            self.db.flush()

            # Save Inventory
            InventoryService(self.db).save_inventory(
                server_id=server.id, inventory=discovery.inventory
            )

            # Save Disks
            DiskService(self.db).create_disks(
                server_id=server.id,
                disks=discovery.disks,
            )

            # Save Network Interfaces
            NetworkInterfaceService(self.db).create_interfaces(
                server_id=server.id,
                interfaces=discovery.interfaces,
            )

            # Commit everything in a single transaction
            self.db.commit()

            self.db.refresh(server)

            # logger.info(
            #     "Server %s created successfully",
            #     server.ip_address,
            # )

            return server

        except IntegrityError as exc:
            self.db.rollback()
            logger.exception(exc)
            raise DatabaseException("Database integrity error.")

        except SQLAlchemyError as exc:
            self.db.rollback()
            logger.exception(exc)
            raise DatabaseException("Database transaction failed.")

        except Exception:
            self.db.rollback()
            raise

    # GET ALL
    def get_all_servers(self):
        return self.server_repository.get_all()

    # GET ONE
    def get_server_by_id(self, server_id: int) -> Server:

        server = self.server_repository.get_by_id(server_id)

        if server is None:
            raise ResourceNotFoundException(
                "Server",
                server_id,
            )

        return server

    # UPDATE
    def update_server(self, server_id: int, request: ServerUpdate) -> Server:

        server = self.get_server_by_id(server_id)

        update_data = request.model_dump(exclude_unset=True)

        if "password" in update_data:
            update_data["encrypted_password"] = encryption_service.encrypt(
                update_data.pop("password")
            )

        for field, value in update_data.items():
            setattr(server, field, value)

        self.db.commit()
        self.db.refresh(server)

        return server

    # DELETE
    def delete_server(self, server_id: int):

        server = self.get_server_by_id(server_id)
        self.server_repository.delete(server, commit=False)

        self.db.commit()

    # ENABLE
    def enable_monitoring(self, server_id: int):

        server = self.get_server_by_id(server_id)
        server.monitoring_enabled = True
        self.db.commit()

        return server

    # DISABLE
    def disable_monitoring(self, server_id: int):

        server = self.get_server_by_id(server_id)

        server.monitoring_enabled = False
        self.db.commit()

        return server

    # PRIVATE METHODS
    def _validate_duplicate_ip(self, ip_address: str):

        if self.server_repository.get_by_ip(ip_address):

            raise ServerAlreadyExistsException(ip_address)

    def _discover_server(self, request: ServerCreate) -> DiscoveryResult:

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
            # Already a handled application exception.
            raise

        except Exception as exc:
            logger.exception("Unexpected discovery error")
            raise SSHConnectionException("Failed to discover server inventory.")

    def _build_server_model(self, request: ServerCreate) -> Server:

        return Server(
            name=request.name,
            ip_address=request.ip_address,
            ssh_port=request.ssh_port,
            username=request.username,
            encrypted_password=encryption_service.encrypt(
                request.password,
            ),
            monitoring_enabled=True,

            # Inventory decides hostname later.
            status=ServerStatus.UNKNOWN,
        )
