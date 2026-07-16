from sqlalchemy.orm import Session

from app.repositories.server_repository import ServerRepository
from app.services.server.validation_service import ServerValidationService


class MonitoringServerService:

    def __init__(self, db: Session):
        self.db = db
        self.server_repository = ServerRepository(db)
        self.validation_service = ServerValidationService(db)

    def enable_monitoring(self, server_id: int):

        return self._set_monitoring(server_id, True)

    def disable_monitoring(self, server_id: int):

        return self._set_monitoring(server_id, False)

    def _set_monitoring(
        self,
        server_id: int,
        enabled: bool,
    ):

        server = self.validation_service.get_server_by_id(server_id)

        server.monitoring_enabled = enabled

        self.db.commit()

        self.db.refresh(server)

        return server
