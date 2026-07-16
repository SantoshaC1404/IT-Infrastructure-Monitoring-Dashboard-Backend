from sqlalchemy.orm import DeclarativeBase

"""
Every model class should inherit from this base class. 
This is the base class for all models in the application.
"""


class Base(DeclarativeBase):
    pass
