from sqlalchemy.orm import Session

from app.repositories.disk_repository import DiskRepository


class CreateDiskService:

    def __init__(self, db: Session):
        self.disk_repository = DiskRepository(db=db)

    def create_disks(
        self,
        device_id: int,
        disks,
    ):
        return self.disk_repository.create_many(
            device_id=device_id,
            disks=disks,
        )
