from sqlalchemy.orm import Session

from app.repositories.disk_repository import DiskRepository


class ReplaceDiskService:

    def __init__(self, db: Session):
        self.repository = DiskRepository(db=db)

    def replace_disks(
        self,
        device_id: int,
        disks,
    ):

        self.repository.delete_by_device(device_id=device_id)

        return self.repository.create_many(
            device_id=device_id,
            disks=disks,
        )
