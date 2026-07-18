from sqlalchemy.orm import Session

from app.core.encryption import encryption_service
from app.models.device import Server
from app.repositories.server_repository import ServerRepository
from app.schemas.server import ServerUpdate
from app.services.server.validation_service import ServerValidationService


class UpdateServerService:

    def __init__(self, db: Session):

        self.db = db
        self.server_repository = ServerRepository(db)
        self.validation_service = ServerValidationService(db)

    def update_server(
        self,
        server_id: int,
        request: ServerUpdate,
    ) -> Server:

        server = self.validation_service.get_server_by_id(server_id)

        update_data = request.model_dump(
            exclude_unset=True,
        )

        if "password" in update_data:

            update_data["encrypted_password"] = encryption_service.encrypt(
                update_data.pop("password")
            )

        for field, value in update_data.items():

            setattr(
                server,
                field,
                value,
            )

        self.db.commit()

        self.db.refresh(server)

        return server
