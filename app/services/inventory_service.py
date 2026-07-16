from sqlalchemy.orm import Session

from app.dto.discovered_disk import DiscoveredDisk
from app.dto.discovered_inventory import DiscoveredInventory
from app.dto.discovered_network import DiscoveredNetworkInterface

from app.models.disk import Disk
from app.models.network_interface import NetworkInterface
from app.models.server_inventory import ServerInventory

from app.repositories.disk_repository import DiskRepository
from app.repositories.network_interface_repository import (
    NetworkInterfaceRepository,
)
from app.repositories.server_inventory_repository import (
    ServerInventoryRepository,
)


class InventoryService:
    """
    Responsible for persisting server inventory.

    This service NEVER performs SSH operations.

    This service NEVER commits transactions.

    ServerService is responsible for transaction management.
    """

    def __init__(self, db: Session):

        self.db = db

        self.inventory_repository = ServerInventoryRepository(db)

        self.disk_repository = DiskRepository(db)

        self.network_repository = NetworkInterfaceRepository(db)

    # --------------------------------------------------------
    # PUBLIC API
    # --------------------------------------------------------

    def save_inventory(
        self,
        server_id: int,
        inventory: DiscoveredInventory,
    ) -> ServerInventory:

        inventory_model = self._build_inventory_model(
            server_id,
            inventory,
        )

        self.inventory_repository.create(inventory_model)

        # disk_models = self._build_disk_models(
        #     server_id,
        #     disks,
        # )

        # network_models = self._build_network_models(
        #     server_id,
        #     interfaces,
        # )

        # self.disk_repository.create_many(disk_models)

        # self.network_repository.create_many(network_models)

        return inventory_model

    # --------------------------------------------------------

    def update_inventory(
        self,
        server_id: int,
        inventory: DiscoveredInventory,
        disks: list[DiscoveredDisk],
        interfaces: list[DiscoveredNetworkInterface],
    ) -> ServerInventory:

        db_inventory = self.inventory_repository.get_by_server_id(server_id)

        if db_inventory is None:

            return self.save_inventory(
                server_id,
                inventory,
                disks,
                interfaces,
            )

        self._update_inventory_model(
            db_inventory,
            inventory,
        )

        self.disk_repository.delete_by_server(server_id)

        self.network_repository.delete_by_server(server_id)

        self.disk_repository.create_many(
            self._build_disk_models(
                server_id,
                disks,
            )
        )

        self.network_repository.create_many(
            self._build_network_models(
                server_id,
                interfaces,
            )
        )

        return db_inventory

    # --------------------------------------------------------
    # PRIVATE METHODS
    # --------------------------------------------------------

    def _build_inventory_model(
        self,
        server_id: int,
        inventory: DiscoveredInventory,
    ) -> ServerInventory:

        return ServerInventory(
            server_id=server_id,
            hostname=inventory.hostname,
            server_type=inventory.server_type,
            operating_system=inventory.operating_system,
            os_version=inventory.os_version,
            kernel_version=inventory.kernel_version,
            architecture=inventory.architecture,
            cpu_model=inventory.cpu_model,
            # cpu_cores=inventory.physical_cores,
            # logical_processors=inventory.logical_cores,
            # total_memory=inventory.total_memory_bytes,
            virtualization=inventory.virtualization,
            manufacturer=inventory.manufacturer,
            model=inventory.model,
            serial_number=inventory.serial_number,
        )

    # --------------------------------------------------------

    def _update_inventory_model(
        self,
        model: ServerInventory,
        inventory: DiscoveredInventory,
    ):

        model.hostname = inventory.hostname

        model.server_type = inventory.server_type

        model.operating_system = inventory.operating_system

        model.os_version = inventory.os_version

        model.kernel_version = inventory.kernel_version

        model.architecture = inventory.architecture

        model.cpu_model = inventory.cpu_model

        model.cpu_cores = inventory.physical_cores

        model.logical_processors = inventory.logical_cores

        model.total_memory = inventory.total_memory_bytes

        model.virtualization = inventory.virtualization

        model.manufacturer = inventory.manufacturer

        model.model = inventory.model

        model.serial_number = inventory.serial_number

    # --------------------------------------------------------

    def _build_disk_models(
        self,
        server_id: int,
        disks: list[DiscoveredDisk],
    ) -> list[Disk]:

        return [
            Disk(
                server_id=server_id,
                device_name=disk.device_name,
                filesystem=disk.filesystem,
                mount_point=disk.mount_point,
                total_bytes=disk.total_bytes,
                used_bytes=disk.used_bytes,
                free_bytes=disk.free_bytes,
            )
            for disk in disks
        ]

    # --------------------------------------------------------

    def _build_network_models(
        self,
        server_id: int,
        interfaces: list[DiscoveredNetworkInterface],
    ) -> list[NetworkInterface]:

        return [
            NetworkInterface(
                server_id=server_id,
                interface_name=interface.interface_name,
                mac_address=interface.mac_address,
                ipv4_address=interface.ipv4_address,
                ipv6_address=interface.ipv6_address,
                speed_mbps=interface.speed_mbps,
                is_up=interface.is_up,
            )
            for interface in interfaces
        ]
