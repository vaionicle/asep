from sqlalchemy.orm import DeclarativeBase
from database.connect import engine

class Base(DeclarativeBase):
    pass

Base.metadata.create_all(engine)
