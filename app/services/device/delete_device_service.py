from sqlalchemy.orm import Session

from app.repositories.device_repository import ServerRepository
from app.services.device.validation_service import ServerValidationService


class DeleteServerService:

    def __init__(self, db: Session):
        self.db = db
        self.server_repository = ServerRepository(db)
        self.validation_service = ServerValidationService(db)

    # Delete by ID
    def delete_server_id(self, server_id: int):

        server = self.validation_service.get_server_by_id(server_id)

        self.server_repository.delete(
            server,
            commit=False,
        )

        self.db.commit()

    # Delete by IP
    def delete_server_ip(self, ip_address: str):

        server = self.validation_service.get_server_by_ip(ip_address)

        self.server_repository.delete(
            server,
            commit=False,
        )

        self.db.commit()
