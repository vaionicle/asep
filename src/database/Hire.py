
from sqlalchemy import String, Column, Integer, ForeignKey, Float

from .Base import Base
from .connect import engine

class Hire(Base):
    __tablename__ = "school_hire"

    # Every SQLAlchemy table should have a primary key named 'id'
    id                  = Column(Integer, primary_key=True)
    am                  = Column(String(length=255))
    file                = Column(String(length=255))

    school_year         = Column(String(length=255))
    round               = Column(Integer)

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

    def createRow(self, row):
        pass

    # def updateRow(self, row):

        # school_year         =
        # round               =

        # location            =
        # state               =
        # management_sector   =
        # working_hours       =

        # aa                  =
        # aa_row              =

        # department          =
        # specification       =

        # main_table_score    =
        # main_table_order    =
        # main_table_type     =
        # main_table          =


Base.metadata.create_all(engine)