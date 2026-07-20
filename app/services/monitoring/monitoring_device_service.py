from datetime import datetime

from sqlalchemy.orm import Session

from app.utils.enums import DeviceStatus


class MonitoringDeviceService:

    def __init__(self, db: Session):

        self.db = db

    # -----------------------------------------------------

    def mark_online(
        self,
        device,
    ):

        device.status = DeviceStatus.ONLINE

        device.last_seen = datetime.utcnow()

        self.db.commit()

    # -----------------------------------------------------

    def mark_offline(
        self,
        device,
    ):

        device.status = DeviceStatus.OFFLINE

        self.db.commit()
