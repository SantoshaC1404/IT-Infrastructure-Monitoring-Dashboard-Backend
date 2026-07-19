from sqlalchemy.orm import Session

from app.core.encryption import encryption_service
from app.models.device import Device
from app.repositories.device_repository import DeviceRepository
from app.schemas.device import DeviceUpdate
from app.services.device.validation_service import DeviceValidationService


class UpdateDeviceService:

    def __init__(self, db: Session):

        self.db = db
        self.device_repository = DeviceRepository(db)
        self.validation_service = DeviceValidationService(db)

    def update_device(
        self,
        device_id: int,
        request: DeviceUpdate,
    ) -> Device:

        device = self.validation_service.get_device_by_id(device_id)

        update_data = request.model_dump(
            exclude_unset=True,
        )

        if "password" in update_data:

            update_data["encrypted_password"] = encryption_service.encrypt(
                update_data.pop("password")
            )

        for field, value in update_data.items():

            setattr(
                device,
                field,
                value,
            )

        self.db.commit()

        self.db.refresh(device)

        return device
