from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.network_interface import NetworkInterface


class NetworkInterfaceRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, device_id: int, interface):

        db_interface = NetworkInterface(
            device_id=device_id,
            interface_name=interface.interface_name,
            ipv4_address=interface.ipv4_address,
            ipv6_address=interface.ipv6_address,
            mac_address=interface.mac_address,
            speed_mbps=interface.speed_mbps,
            is_up=interface.is_up,
        )

        self.db.add(db_interface)

        return db_interface

    def create_many(self, device_id: int, interfaces):

        created = []

        for interface in interfaces:
            created.append(self.create(device_id, interface))

        return created

    def delete_by_device_id(self, device_id: int):

        self.db.query(NetworkInterface).filter(
            NetworkInterface.device_id == device_id
        ).delete()

    def get_by_device_id(
        self,
        device_id: int,
    ) -> list[NetworkInterface]:
        stmt = (
            select(NetworkInterface)
            .where(NetworkInterface.device_id == device_id)
            .order_by(NetworkInterface.mount_point)
        )

        return self.db.scalars(stmt).all()

    def get_by_interface_id(
        self,
        interface_id: int,
    ) -> NetworkInterface | None:

        return self.db.get(NetworkInterface, interface_id)
