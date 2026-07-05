from sqlalchemy.orm import DeclarativeBase

# Import all models
import app.models


class Base(DeclarativeBase):
    pass
