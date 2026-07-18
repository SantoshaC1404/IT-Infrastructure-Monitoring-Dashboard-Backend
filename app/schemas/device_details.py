from pydantic import BaseModel

from app.schemas.disk import DiskResponse
from app.schemas.network_interface import NetworkInterfaceResponse
from app.schemas.device import DeviceResponse
from app.schemas.device_inventory import DeviceInventoryResponse


class DeviceDetailResponse(BaseModel):

    device: DeviceResponse

    inventory: DeviceInventoryResponse | None

    disks: list[DiskResponse] = []

    network_interfaces: list[NetworkInterfaceResponse] = []
