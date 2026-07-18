from sqlalchemy.orm import Session

from app.repositories.disk_repository import DiskRepository


class QueryDiskService:

    def __init__(self, db: Session):
        self.repository = DiskRepository(db=db)

    def get_disks_by_device_id(
        self,
        device_id: int,
    ):

        return self.repository.get_by_device_id(device_id=device_id)

    def get_disk_by_id(
        self,
        disk_id: int,
    ):
        return self.repository.get_by_id(disk_id=disk_id)
