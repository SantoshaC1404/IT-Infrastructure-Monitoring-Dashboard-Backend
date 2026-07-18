from app.models.device_inventory import DeviceInventory


class InventoryFactory:

    @staticmethod
    def build(device_id: int, inventory):

        return DeviceInventory(
            device_id=device_id,
            hostname=inventory.hostname,
            device_type=inventory.device_type,
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
