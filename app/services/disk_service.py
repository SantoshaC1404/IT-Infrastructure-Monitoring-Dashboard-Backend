from sqlalchemy.orm import Session

from app.repositories.disk_repository import DiskRepository


class DiskService:

    def __init__(self, db: Session):
        self.repository = DiskRepository(db)

    def create_disks(self, server_id: int, disks):

        return self.repository.create_many(server_id, disks)

    def replace_disks(self, server_id: int, disks):

        self.repository.delete_by_server(server_id)

        return self.repository.create_many(server_id, disks)
