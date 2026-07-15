from sqlalchemy.orm import Session

from app.models.network_interface import NetworkInterface


class NetworkInterfaceRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, server_id: int, interface):

        db_interface = NetworkInterface(
            server_id=server_id,
            interface_name=interface.interface_name,
            ipv4_address=interface.ipv4_address,
            ipv6_address=interface.ipv6_address,
            mac_address=interface.mac_address,
            speed_mbps=interface.speed_mbps,
            is_up=interface.is_up,
        )

        self.db.add(db_interface)

        return db_interface

    def create_many(self, server_id: int, interfaces):

        created = []

        for interface in interfaces:
            created.append(self.create(server_id, interface))

        return created

    def delete_by_server(self, server_id: int):

        self.db.query(NetworkInterface).filter(
            NetworkInterface.server_id == server_id
        ).delete()
