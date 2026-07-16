from pydantic import BaseModel

from app.schemas.disk import DiskResponse
from app.schemas.network_interface import NetworkInterfaceResponse
from app.schemas.server import ServerResponse
from app.schemas.server_inventory import ServerInventoryResponse


class ServerDetailResponse(BaseModel):

    server: ServerResponse

    inventory: ServerInventoryResponse | None

    disks: list[DiskResponse] = []

    network_interfaces: list[NetworkInterfaceResponse] = []
