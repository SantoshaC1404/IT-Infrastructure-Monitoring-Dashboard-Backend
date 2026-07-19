from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.exceptions import DatabaseException
from app.models.device import Device
from app.repositories.device_repository import DeviceRepository
from app.schemas.device import DeviceCreate

from app.services.device.device_discovery_service import DeviceDiscoveryService
from app.services.device.device_factory import DeviceFactory
from app.services.device.persistence_service import DevicePersistenceService
from app.services.device.validation_service import DeviceValidationService


class CreateDeviceService:
    """
    Handles complete device onboarding.

    Steps

    1. Validate
    2. Discover device
    3. Build Device model
    4. Save device
    5. Save inventory/disks/interfaces
    """

    def __init__(self, db: Session):

        self.db = db

        self.repository = DeviceRepository(db)

        self.validation = DeviceValidationService(db)

        self.persistence = DevicePersistenceService(db)

    def create_device(
        self,
        request: DeviceCreate,
    ) -> Device:

        self.validation.validate_duplicate_ip(
            request.ip_address,
        )

        discovery = DeviceDiscoveryService.discover_device(
            request,
        )

        device = DeviceFactory.build(
            request,
        )

        try:

            self.repository.create(
                device,
                commit=False,
            )

            self.persistence.save(
                device,
                discovery,
            )

            return device

        except IntegrityError:

            self.db.rollback()

            raise DatabaseException("Database integrity error.")

        except SQLAlchemyError:

            self.db.rollback()

            raise DatabaseException("Database transaction failed.")

        except Exception:

            self.db.rollback()
            raise
