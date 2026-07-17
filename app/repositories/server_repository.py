from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.models.server import Server
from app.repositories.base_repository import BaseRepository


class ServerRepository(BaseRepository[Server]):

    def __init__(self, db: Session):
        super().__init__(db)

    
    # GET ALL 
    def get_all(self):
        stmt = (
            select(Server)
            .options(joinedload(Server.inventory))
            .order_by(Server.name)
        )
        
        return list(self.db.scalars(stmt).unique())


    # GET BY ID
    def get_by_id(self, server_id: int):
        stmt = (
            select(Server)
            .options(joinedload(Server.inventory))
            .where(Server.id == server_id)
        )

        return self.db.scalar(stmt)


    # GET BY IP
    def get_by_ip(self, ip_address: str):

        stmt = (
            select(Server)
            .where(Server.ip_address == ip_address)
        )

        return self.db.scalar(stmt)


    # CREATE
    def create(
        self,
        server: Server,
        commit: bool = True,
    ):
        self.db.add(server)
        if commit:
            self.db.commit()
            self.db.refresh(server)
        return server


    # UPDATE
    def update(self, server: Server):
        self.db.flush()
        return server


    # DELETE
    def delete(
        self,
        server: Server,
        commit: bool = True,
    ):
        self.db.delete(server)
        if commit:
            self.db.commit()


    # GET MONITORING STATUS
    def get_monitoring_enabled(self):

        stmt = (
            select(Server)
            .where(Server.monitoring_enabled.is_(True))
        )

        return list(self.db.scalars(stmt).all())
