from sqlalchemy.orm import Session

from app.repositories.server_repository import ServerRepository
from app.services.server.validation_service import ServerValidationService


class DeleteServerService:

    def __init__(self, db: Session):
        self.db = db
        self.server_repository = ServerRepository(db)
        self.validation_service = ServerValidationService(db)

    def delete_server(self, server_id: int):

        server = self.validation_service.get_server_by_id(server_id)

        self.server_repository.delete(
            server,
            commit=False,
        )

        self.db.commit()
