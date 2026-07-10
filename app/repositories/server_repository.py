from sqlalchemy.orm import Session

from app.models.server import Server


class ServerRepository:

    def __init__(self, db: Session):
        """Repository for managing server-related database operations."""
        self.db = db

    def get_all(self):
        """Retrieve all servers from the database."""
        return self.db.query(Server).all()

    def get_by_id(self, server_id: int):
        """Retrieve a server by its ID."""
        return self.db.query(Server).filter(Server.id == server_id).first()

    def get_server_by_ip(self, ip: str):
        """Retrieve a server by its IP address."""
        return self.db.query(Server).filter(Server.ip_address == ip).first()

    def create(self, server: Server):
        """Create a new server in the database."""
        self.db.add(server)
        self.db.commit()
        self.db.refresh(server)
        return server

    def update(self, server: Server):
        """Update an existing server in the database."""
        self.db.commit()
        self.db.refresh(server)
        return server

    def delete(self, server: Server):
        """Delete a server from the database."""
        self.db.delete(server)
        self.db.commit()
