from typing import Generic, TypeVar

from sqlalchemy.orm import Session

ModelType = TypeVar("ModelType")


class BaseRepository(Generic[ModelType]):
    def __init__(self, db: Session):
        self.db = db

    def add(self, obj: ModelType):
        self.db.add(obj)
        self.db.flush()
        return obj

    def delete(self, obj: ModelType):
        self.db.delete(obj)

    def commit(self):
        self.db.commit()

    def rollback(self):
        self.db.rollback()

    def refresh(self, obj: ModelType):
        self.db.refresh(obj)
