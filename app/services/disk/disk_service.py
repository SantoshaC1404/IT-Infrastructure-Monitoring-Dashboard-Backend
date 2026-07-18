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
        device_id: int,
        disks,
    ):

        return self.create_service.create_disks(
            device_id,
            disks,
        )

    # Replace Disks
    def replace_disks(
        self,
        device_id: int,
        disks,
    ):
        return self.replace_service.replace_disks(
            device_id=device_id,
            disks=disks,
        )

    # Get by server id
    def get_by_device_id(
        self,
        device_id: int,
    ):
        return self.query_service.get_disks_by_device_id(device_id)

    # Get by disk id
    def get_by_disk_id(
        self,
        disk_id: int,
    ):
        return self.query_service.get_disk_by_id(disk_id)
