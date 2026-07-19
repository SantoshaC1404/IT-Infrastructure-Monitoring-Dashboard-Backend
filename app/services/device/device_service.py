from sqlalchemy.orm import Session

from app.models.device import Device
from app.schemas.device import DeviceCreate, DeviceUpdate

from app.services.device.create_device_service import CreateDeviceService
from app.services.device.delete_device_service import DeleteDeviceService
from app.services.device.monitoring_device_service import MonitoringDeviceService
from app.services.device.query_device_service import QueryDeviceService
from app.services.device.update_device_service import UpdateDeviceService


class DeviceService:
    """
    Facade for all device operations.

    Controllers should communicate only with this class.
    """

    def __init__(self, db: Session):

        self.create_service = CreateDeviceService(db)
        self.query_service = QueryDeviceService(db)
        self.update_service = UpdateDeviceService(db)
        self.delete_service = DeleteDeviceService(db)
        self.monitoring_service = MonitoringDeviceService(db)

    # -------------------------
    # CREATE
    # -------------------------

    def create_device(
        self,
        request: DeviceCreate,
    ) -> Device:

        return self.create_service.create_device(request)

    # -------------------------
    # READ
    # -------------------------

    def get_all_devices(self):

        return self.query_service.get_all_devices()

    def get_device_by_id(
        self,
        device_id: int,
    ):

        return self.query_service.get_device_by_id(device_id)

    def get_device_by_ip(
        self,
        ip_address: str,
    ):

        return self.query_service.get_device_by_ip(ip_address)

    # -------------------------
    # UPDATE
    # -------------------------

    def update_device(
        self,
        device_id: int,
        request: DeviceUpdate,
    ):

        return self.update_service.update_device(
            device_id,
            request,
        )

    # -------------------------
    # DELETE
    # -------------------------

    def delete_device_by_id(
        self,
        device_id: int,
    ):

        self.delete_service.delete_device_by_id(device_id)

    def delete_device_by_ip(
        self,
        ip_address: str,
    ):

        self.delete_service.delete_device_by_ip(ip_address)

    # -------------------------
    # MONITORING
    # -------------------------

    def enable_monitoring(
        self,
        device_id: int,
    ):

        return self.monitoring_service.enable_monitoring(device_id)

    def disable_monitoring(
        self,
        device_id: int,
    ):

        return self.monitoring_service.disable_monitoring(device_id)
