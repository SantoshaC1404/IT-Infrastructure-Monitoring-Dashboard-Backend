from sqlalchemy.orm import Session

from app.core.logger import logger
from app.models.device import Device
from app.schemas.device.device import DeviceCreate, DeviceUpdate

from app.services.device.create_device_service import CreateDeviceService
from app.services.device.delete_device_service import DeleteDeviceService
from app.services.device.monitoring_device_service import MonitoringDeviceService
from app.services.device.query_device_service import QueryDeviceService
from app.services.device.update_device_service import UpdateDeviceService
from app.services.monitoring.collect_metrics_service import CollectMetricsService


class DeviceService:
    """
    Facade for all device operations.

    Controllers should communicate only with this class.
    """

    def __init__(self, db: Session):

        self.db = db
        self.create_service = CreateDeviceService(db)
        self.query_service = QueryDeviceService(db)
        self.update_service = UpdateDeviceService(db)
        self.delete_service = DeleteDeviceService(db)
        self.monitoring_service = MonitoringDeviceService(db)
        self.collect_metrics_service = CollectMetricsService(db)

    # CREATE
    def create_device(
        self,
        request: DeviceCreate,
    ) -> Device:

        return self.create_service.create_device(request)

    # READ
    def get_all_devices(self):

        devices = self.query_service.get_all_devices()

        for device in devices:
            if device.monitoring_enabled and (
                device.login_source is None or device.last_login_time is None
            ):
                try:
                    self.collect_metrics_service.monitor_device(device.id)
                except Exception:
                    logger.exception(
                        "Live metric collection failed for device %s",
                        device.id,
                    )

        return self.query_service.get_all_devices()

    # Get Device by ID
    def get_device_by_id(
        self,
        device_id: int,
    ):

        device = self.query_service.get_device_by_id(device_id)

        if device.monitoring_enabled and (
            device.login_source is None or device.last_login_time is None
        ):
            try:
                self.collect_metrics_service.monitor_device(device.id)
            except Exception:
                logger.exception(
                    "Live metric collection failed for device %s",
                    device.id,
                )

            device = self.query_service.get_device_by_id(device_id)

        return device

    # Get Device by IP
    def get_device_by_ip(
        self,
        ip_address: str,
    ):

        device = self.query_service.get_device_by_ip(ip_address)

        if device.monitoring_enabled and (
            device.login_source is None or device.last_login_time is None
        ):
            try:
                self.collect_metrics_service.monitor_device(device.id)
            except Exception:
                logger.exception(
                    "Live metric collection failed for device %s",
                    device.id,
                )

            device = self.query_service.get_device_by_ip(ip_address)

        return device

    # UPDATE
    def update_device(
        self,
        device_id: int,
        request: DeviceUpdate,
    ):

        return self.update_service.update_device(
            device_id,
            request,
        )

    # DELETE
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

    # MONITORING
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
