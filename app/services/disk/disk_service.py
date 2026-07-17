from sqlalchemy.orm import Session

from app.services.disk.create_disk_service import CreateDiskService
from app.services.disk.query_disk_service import QueryDiskService
from app.services.disk.replace_disk_service import ReplaceDiskService


class DiskService:

    def __init__(self, db: Session):
        self.create_service = CreateDiskService(db)
        self.replace_service = ReplaceDiskService(db)
        self.query_service = QueryDiskService(db)

    # Create Disks
    def create_disks(
        self,
        server_id: int,
        disks,
    ):

        return self.create_service.create_disks(
            server_id,
            disks,
        )

    # Replace Disks
    def replace_disks(
        self,
        server_id: int,
        disks,
    ):
        return self.replace_service.replace_disks(
            server_id=server_id,
            disks=disks,
        )

    # Get by server id
    def get_by_server_id(
        self,
        server_id: int,
    ):
        return self.query_service.get_disks_by_server_id(server_id)

    # Get by disk id
    def get_by_disk_id(
        self,
        disk_id: int,
    ):
        return self.query_service.get_disk_by_id(disk_id)
