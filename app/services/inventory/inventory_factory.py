from app.models.server_inventory import ServerInventory


class InventoryFactory:

    @staticmethod
    def build(server_id: int, inventory):

        return ServerInventory(
            server_id=server_id,
            hostname=inventory.hostname,
            server_type=inventory.server_type,
            operating_system=inventory.operating_system,
            os_version=inventory.os_version,
            kernel_version=inventory.kernel_version,
            architecture=inventory.architecture,
            cpu_model=inventory.cpu_model,
            physical_cores=inventory.physical_cores,
            logical_cores=inventory.logical_cores,
            total_memory_bytes=inventory.total_memory_bytes,
            virtualization=inventory.virtualization,
        )
