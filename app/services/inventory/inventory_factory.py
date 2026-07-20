from app.models.device_inventory import DeviceInventory


from app.models.device_inventory import DeviceInventory
from app.utils.enums import DeviceType


class InventoryFactory:

    @staticmethod
    def build(
        device_id: int,
        inventory,
        device_type: DeviceType,
    ):
        return DeviceInventory(
            device_id=device_id,
            hostname=inventory.hostname,
            device_type=device_type,
            operating_system=inventory.operating_system,
            os_version=inventory.os_version,
            kernel_version=inventory.kernel_version,
            architecture=inventory.architecture,
            cpu_model=inventory.cpu_model,
            cpu_vendor=inventory.cpu_vendor,
            cpu_architecture=inventory.cpu_architecture,
            physical_cores=inventory.physical_cores,
            logical_cores=inventory.logical_cores,
            total_memory_bytes=inventory.total_memory_bytes,
            available_memory_bytes=inventory.available_memory_bytes,
            used_memory_bytes=inventory.used_memory_bytes,
            total_disk_bytes=inventory.total_disk_bytes,
            virtualization=inventory.virtualization,
            manufacturer=inventory.manufacturer,
            model=inventory.model,
            serial_number=inventory.serial_number,
        )
