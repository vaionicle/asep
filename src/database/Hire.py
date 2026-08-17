from sqlalchemy import String, Column, Integer, Float, ForeignKey, select

from .Base import Base
from .connect import engine, session

class Hire(Base):
    __tablename__ = "hires"

    # --------------------------------------------------
    # Primary key / relation
    # --------------------------------------------------

    id = Column(Integer, primary_key=True)
    educator_id = Column(Integer, nullable=False, index=True)

    # --------------------------------------------------
    # Import metadata
    # --------------------------------------------------

    school_year = Column(String(length=255), index=True)
    round = Column(String(length=255), index=True)

    # --------------------------------------------------
    # Row information
    # --------------------------------------------------

    aa = Column(Integer)
    aa_row = Column(Integer)

    # --------------------------------------------------
    # Educator classification
    # --------------------------------------------------

    department = Column(String(length=255), index=True)
    specialization = Column(String(length=255), index=True)

    # --------------------------------------------------
    # Ranking table
    # --------------------------------------------------

    main_table_type = Column(String(length=255))
    main_table = Column(String(length=255))
    main_table_order = Column(Integer)
    main_table_score = Column(Float)

    # --------------------------------------------------
    # Placement
    # --------------------------------------------------

    location = Column(String(length=255), index=True)
    working_hours = Column(String(length=255))
    management_sector = Column(String(length=255))
    state = Column(String(length=255), index=True)

    # --------------------------------------------------
    # Factory
    # --------------------------------------------------

    @staticmethod
    def createRow(row):
        hire = Hire()
        hire.updateRow(row)

        return hire

    # --------------------------------------------------
    # Update
    # --------------------------------------------------

    def updateRow(self, row):
        fields = [
            "educator_id",
            "school_year",
            "round",
            "aa",
            "aa_row",
            "department",
            "specialization",
            "main_table_type",
            "main_table",
            "main_table_order",
            "main_table_score",
            "location",
            "working_hours",
            "management_sector",
            "state",
        ]

        for field in fields:
            if field in row:
                setattr(self, field, row[field])

    # --------------------------------------------------
    # Queries
    # --------------------------------------------------

    @staticmethod
    def findByEducatorID(educator_id):
        query = select(Hire).where(
            Hire.educator_id == educator_id
        )

        return session.scalars(query).all()

    @staticmethod
    def findByEducatorIDYearAndRound(educator_id, school_year, round):
        query = (
            select(Hire)
            .where(Hire.educator_id == educator_id)
            .where(Hire.school_year == school_year)
            .where(Hire.round == round)
        )

        return session.scalars(query).all()