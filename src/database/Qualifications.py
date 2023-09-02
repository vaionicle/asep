
from sqlalchemy import String, Column, Integer, ForeignKey, Float
from .Base import Base
from .connect import engine

class Qualifications(Base):
    __tablename__ = "qualifications"

    # Every SQLAlchemy table should have a primary key named 'id'
    id                      = Column(Integer, primary_key=True)

    am                      = Column(String(length=255))
    year_of_import          = Column(String(length=255))

    total_score             = Column(Float)
    is_amea                 = Column(Float)
    number_of_kids          = Column(Float)

    degree_first            = Column(Float)
    degree_second           = Column(Float)
    degree_master           = Column(Float)
    degree_doctor           = Column(Float)
    
    experience_in_months    = Column(Float)
    score_for_experience    = Column(Float)

    file = Column(String(length=255))

    def createRow(row, year):
        return Qualifications(
            file                    = row['file'],
            am                      = row['am'],
            year_of_import          = year,
            total_score             = float(row['total_score']),
            degree_first            = float(row['01.first_degree']),
            degree_second           = float(row['02.second_degree']),
            degree_master           = float(row['04.master_degree']),
            degree_doctor           = float(row['03.doctor_degree']),
            experience_in_months    = float(row['12.month_of_education_experience']),
            score_for_experience    = float(row['13.score_of_education_experience']),
            number_of_kids          = float(row['25.kids']),
            is_amea                 = float(row['26.amea']),
        )

    def updateRow(self, row):
        self.total_score             = float(row['total_score'])
        self.degree_first            = float(row['01.first_degree'])
        self.degree_second           = float(row['02.second_degree'])
        self.degree_master           = float(row['04.master_degree'])
        self.degree_doctor           = float(row['03.doctor_degree'])
        self.experience_in_months    = float(row['12.month_of_education_experience'])
        self.score_for_experience    = float(row['13.score_of_education_experience'])
        self.number_of_kids          = float(row['25.kids'])
        self.is_amea                 = float(row['26.amea'])


Base.metadata.create_all(engine)