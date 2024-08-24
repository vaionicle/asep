
from sqlalchemy import String, Column, Integer, ForeignKey, Float, select

from .Base import Base
from .connect import engine, session

class SchoolCategory(Base):
    __tablename__ = "school-categories"

    # Every SQLAlchemy table should have a primary key named 'id'
    id     = Column(Integer, primary_key=True)
    type   = Column(String(length=255))
    name   = Column(String(length=255))

    def createRow(row, type, name):
        schoolCat = SchoolCategory()
        schoolCat.updateRow(type, name)

        return schoolCat

    def updateRow(self, type, name):
        self.type = type
        self.name = name

Base.metadata.create_all(engine)