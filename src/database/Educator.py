
from sqlalchemy import String, Column, Integer, ForeignKey
from .Base import Base
from .connect import engine

class Educator(Base):
    __tablename__ = "educator"

    # Every SQLAlchemy table should have a primary key named 'id'
    id          = Column(Integer, primary_key=True)
    am          = Column(String(length=255))
    name        = Column(String(length=255))
    lastname    = Column(String(length=255))
    father      = Column(String(length=255))
    adt         = Column(String(length=255))

    def createRow(row):
        return Educator(
            am          = row['am'],
            name        = row['name'],
            lastname    = row['lastname'],
            father      = row['father'],
            adt         = row['adt'],
        )
        
    def updateRow(self, row):
        self.name        = row['name'],
        self.lastname    = row['lastname'],
        self.father      = row['father'],
        self.adt         = row['adt'],

    def __repr__(self) -> str:
        return f"Educator(\
            id={self.id!r}, \
            am={self.am!r}, \
            name={self.name!r}, \
            lastname={self.lastname!r}, \
            father={self.father!r}, \
            adt={self.adt!r} \
        )"

Base.metadata.create_all(engine)