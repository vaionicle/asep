from sqlalchemy.orm import DeclarativeBase

from .connect import engine, session

class Base(DeclarativeBase):
    pass

    def commit(self):
        session.commit()

    def add(self):
        session.add(self)

Base.metadata.create_all(engine)
