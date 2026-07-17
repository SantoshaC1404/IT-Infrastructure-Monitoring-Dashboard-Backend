from sqlalchemy.orm import Session

from app.repositories.disk_repository import DiskRepository


class ReplaceDiskService:

    def __init__(self, db: Session):
        self.repository = DiskRepository(db=db)

    def replace_disks(
        self,
        server_id: int,
        disks,
    ):

        self.repository.delete_by_server(server_id=server_id)

        return self.repository.create_many(
            server_id=server_id,
            disks=disks,
        )
