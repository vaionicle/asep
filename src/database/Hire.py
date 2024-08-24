
from sqlalchemy import String, Column, Integer, ForeignKey, Float, select

from .Base import Base
from .connect import engine, session

class Hire(Base):
    __tablename__ = "school_hire"

    # Every SQLAlchemy table should have a primary key named 'id'
    id                  = Column(Integer, primary_key=True)
    am                  = Column(String(length=255))
    file                = Column(String(length=255))

    school_year         = Column(String(length=255))
    round               = Column(String(length=255))

    location            = Column(String(length=255))
    state               = Column(String(length=255))
    management_sector   = Column(String(length=255))
    working_hours       = Column(String(length=255))

    aa                  = Column(String(length=255))
    aa_row              = Column(String(length=255))

    department          = Column(String(length=255))
    specification       = Column(String(length=255))

    main_table_score    = Column(String(length=255))
    main_table_order    = Column(String(length=255))
    main_table_type     = Column(String(length=255))
    main_table          = Column(String(length=255))

    def createRow(row, am, file):
        hire = Hire()
        hire.updateRow(row, am, file)

        return hire

    def updateRow(self, row, am, file):
        self.am                  = am
        self.file                = file

        self.school_year         = row['school_year']
        self.round               = row['round']

        self.location            = row['location']
        self.state               = row['state']
        self.management_sector   = row['management_sector']
        self.working_hours       = row['working_hours']

        self.aa                  = row['a/a']
        self.aa_row              = row['a/a_row']

        self.department          = row['department']
        self.specification       = row['spec']

        self.main_table          = row['main_table']
        self.main_table_score    = row['main_table_score']
        self.main_table_order    = row['main_table_order']
        self.main_table_type     = row['main_table_type']

    def findByAmYearRoundAndSpec(am, year, round, spec):
        select_hire = select(Hire) \
            .where(Hire.am == am) \
            .where(Hire.school_year == year) \
            .where(Hire.round == round) \
            .where(Hire.specification == spec)

        hires = session.scalars(select_hire).all()

        return hires

Base.metadata.create_all(engine)