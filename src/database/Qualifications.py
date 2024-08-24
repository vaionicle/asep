
from sqlalchemy import String, Column, Integer, ForeignKey, Float, select

from .Base import Base
from .connect import engine, session

class Qualifications(Base):
    __tablename__ = "qualifications"

    # Every SQLAlchemy table should have a primary key named 'id'
    id                      = Column(Integer, primary_key=True)

    am                      = Column(String(length=255))
    year_of_import          = Column(String(length=255))
    spec                    = Column(String(length=255))

    total_score             = Column(Float)
    total_score_of_academic = Column(Float)
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
        qualification = Qualifications()
        qualification.updateRow(row, year)

        return qualification

    def updateRow(self, row, year):
        self.file                    = row['file']
        self.am                      = row['am']
        self.year_of_import          = year
        self.spec                    = row['specification']
        self.total_score             = float(row['total_score'])
        self.total_score_of_academic = float(row['11.total_score_of_academic'])
        self.degree_first            = float(row['01.first_degree'])
        self.degree_second           = float(row['02.second_degree'])
        self.degree_master           = float(row['04.master_degree'])
        self.degree_doctor           = float(row['03.doctor_degree'])
        self.experience_in_months    = float(row['12.month_of_education_experience'])
        self.score_for_experience    = float(row['13.score_of_education_experience'])
        self.number_of_kids          = float(row['25.kids'])
        self.is_amea                 = float(row['26.amea'])

    def findBy(am, year, spec):
        select_qualification = select(Qualifications) \
            .where(Qualifications.am == am) \
            .where(Qualifications.year_of_import == year) \
            .where(Qualifications.spec == spec)
        qualifications = session.scalars(select_qualification).all()

        return qualifications

Base.metadata.create_all(engine)