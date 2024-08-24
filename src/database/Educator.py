from sqlalchemy import String, Column, Integer, ForeignKey, select, Boolean
from sqlalchemy.orm import aliased

from .Base import Base
from .connect import engine, session
from .Qualifications import Qualifications

import logging
logger = logging.getLogger('qualifications')


class Educator(Base):
    __tablename__ = "educator"

    # Every SQLAlchemy table should have a primary key named 'id'
    id              = Column(Integer, primary_key=True)
    am              = Column(String(length=255), index=True)
    name            = Column(String(length=255))
    lastname        = Column(String(length=255))
    father          = Column(String(length=255))
    adt             = Column(String(length=255), index=True)
    penalty         = Column(Boolean, default=False)
    hired           = Column(Boolean, default=False)

    def createRow(row):
        educator = Educator()
        educator.updateRow(row)

        return educator

    def updateRow(self, row):
        self.am             = row['am']
        self.lastname       = row['lastname']      if not isinstance(row['lastname'], list)   else " ".join(row['lastname'])
        self.name           = row['name']          if not isinstance(row['name'], list)       else " ".join(row['name'])
        self.father         = row['father']        if not isinstance(row['father'], list)     else " ".join(row['father'])
        self.adt            = row['adt']
        self.penalty        = False
        self.hired          = False

    def __repr__(self) -> str:
        return f"Educator(\
            id={self.id!r}, \
            am={self.am!r}, \
            name={self.name!r}, \
            lastname={self.lastname!r}, \
            father={self.father!r}, \
            adt={self.adt!r} \
        )"

    def findAll(lastName, name, father):
        select_educator = select(Educator)
        if isinstance(lastName, list):
            select_educator = select_educator.where(
                (Educator.lastname.like(f"%{lastName[0]}%")) |
                (Educator.lastname.like(f"%{lastName[1]}%"))
            )
        else:
            select_educator = select_educator \
                .where(Educator.lastname.like(f"%{lastName}%"))

        if isinstance(name, list):
            select_educator = select_educator.where(
                (Educator.name.like(f"{name[0][0:3]}%")) |
                (Educator.name.like(f"{name[1][0:3]}%"))
            )
        else:
            select_educator = select_educator \
                .where(Educator.name.like(f"{name[0:3]}%"))

        if isinstance(father, list):
            select_educator = select_educator.where(
                (Educator.father.like(f"{father[0][0:3]}%")) |
                (Educator.father.like(f"{father[1][0:3]}%"))
            )
        else:
            select_educator = select_educator \
                .where(Educator.father.like(f"{father[0:3]}%"))

        educators = session.scalars(select_educator).all()

        return educators

    def findByNameAndSpecAll(lastName, name, father, spec):
        # user_cls = aliased(User, name="user_cls")
        # >>> email_cls = aliased(Address, name="email")
        # >>> stmt = (
        # ...     select(user_cls, email_cls)
        # ...     .join(user_cls.addresses.of_type(email_cls))
        # ...     .order_by(user_cls.id, email_cls.id)
        # ... )
        # >>> row = session.execute(stmt).first()

        educator_cls = aliased(Educator, name="e")
        qualifications_cls = aliased(Qualifications, name="q")

        select_join = select(educator_cls, qualifications_cls)

        if isinstance(lastName, list):
            select_join = select_join.where(
                (educator_cls.lastname.like(f"%{lastName[0]}%")) |
                (educator_cls.lastname.like(f"%{lastName[1]}%"))
            )
        else:
            select_join = select_join \
                .where(educator_cls.lastname.like(f"%{lastName}%"))

        if isinstance(name, list):
            select_join = select_join.where(
                (educator_cls.name.like(f"{name[0][0:3]}%")) |
                (educator_cls.name.like(f"{name[1][0:3]}%"))
            )
        else:
            select_join = select_join \
                .where(educator_cls.name.like(f"{name[0:3]}%"))

        if isinstance(father, list):
            select_join = select_join.where(
                (educator_cls.father.like(f"{father[0][0:3]}%")) |
                (educator_cls.father.like(f"{father[1][0:3]}%"))
            )
        else:
            select_join = select_join \
                .where(educator_cls.father.like(f"{father[0:3]}%"))

        select_join = select_join.join_from(educator_cls, qualifications_cls, educator_cls.am == qualifications_cls.am)
        select_join = select_join.where(qualifications_cls.spec.like(f"{spec}%"))

        logger.debug(select_join.compile(engine, compile_kwargs={"literal_binds": True}))

        educators = session.scalars(select_join).all()

        return educators

    def findByAm(am):
        select_educator = select(Educator).where(Educator.am == am)
        educators = session.scalars(select_educator).all()

        return educators


Base.metadata.create_all(engine)