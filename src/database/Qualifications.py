
from sqlalchemy import String, Column, Integer, ForeignKey, Float
from .Base import Base
from .connect import engine

class Qualifications(Base):
    __tablename__ = "qualifications"

    # Every SQLAlchemy table should have a primary key named 'id'
    id = Column(Integer, primary_key=True)

    am = Column(String(length=255))
    totalScore = Column(Float)
    
    degree_first = Column(Float)
    degree_second = Column(Float)
    degree_master = Column(Float)
    degree_doctor = Column(Float)

    file = Column(String(length=255))

    def createRow(row):
        return Qualifications(
            file        = row['file'],
            am          = row['am'],
            totalScore  = float(row['total_score']),
            degree_first = float(row['01.first_degree']),
            degree_second = float(row['02.second_degree']),
            degree_master = float(row['04.master_degree']),
            degree_doctor = float(row['03.doctor_degree']),
        )

Base.metadata.create_all(engine)