import re

from sqlalchemy import String, Column, Integer, ForeignKey, select, Boolean
from sqlalchemy.orm import aliased

from .Base import Base
from .connect import engine, session
from .Qualifications import Qualifications

import logging
logger = logging.getLogger('qualifications')

# Current-format ADT: one Greek letter followed by 8 digits (eg. Α00576786).
# Older files use two letters followed by 6 digits (eg. ΑΙ519314); those are
# never mistaken for the current format, so a new ADT only ever replaces an
# old one, never the other way round.
NEW_ADT_PATTERN = re.compile(r"^[Α-Ω]\d{8}$")


def _is_new_format_adt(adt):
    return bool(adt) and bool(NEW_ADT_PATTERN.match(adt))


class Educator(Base):
    __tablename__ = "educator"

    # Every SQLAlchemy table should have a primary key named 'id'
    id              = Column(Integer, primary_key=True)
    name            = Column(String(length=255), index=True)
    lastname        = Column(String(length=255), index=True)
    father          = Column(String(length=255), index=True)
    adt             = Column(String(length=255), index=True)
    previous_adt    = Column(String(length=255), index=True)
    penalty         = Column(Boolean, default=False)
    hired           = Column(Boolean, default=False)

    def createRow(row):
        educator = Educator()
        educator.updateRow(row)

        return educator

    def updateRow(self, row):
        self.lastname       = row['lastName']      if not isinstance(row['lastName'], list)   else " ".join(row['lastName'])
        self.name           = row['name']          if not isinstance(row['name'], list)       else " ".join(row['name'])
        self.father         = row['father']        if not isinstance(row['father'], list)     else " ".join(row['father'])

        incoming_adt = row['adt']

        if incoming_adt not in ("", "0", None):
            if self.adt in ("", "0", None):
                self.adt = incoming_adt
            elif incoming_adt != self.adt:
                # The ADT changed for this person (eg. the old
                # ΑΙ519314-style adt being replaced by the new
                # Α00576786-style one). Keep both instead of losing the
                # old one: promote the incoming value only if it's the
                # current format (or self.adt isn't), otherwise just
                # remember it as a historical alias.
                if _is_new_format_adt(incoming_adt) or not _is_new_format_adt(self.adt):
                    self.previous_adt = self.adt
                    self.adt = incoming_adt
                else:
                    self.previous_adt = incoming_adt

        self.penalty        = False
        self.hired          = False

    def __repr__(self) -> str:
        return f"Educator(\
            id={self.id!r}, \
            name={self.name!r}, \
            lastname={self.lastname!r}, \
            father={self.father!r}, \
            adt={self.adt!r} \
        )"

    def findByAdtWithLike(adt):
        select_educator = select(Educator)
        select_educator = select_educator.where(Educator.adt.like(f"%{adt}%"))

        educators = session.scalars(select_educator).all()

        return educators

    def findByAdt(adt):
        select_educator = select(Educator)
        select_educator = select_educator.where(Educator.adt == adt)
        select_educator = select_educator.order_by(Educator.id)

        educators = session.scalars(select_educator).all()

        return educators

    def findByAnyAdt(adt):
        # Matches on either the current adt or a previously-seen one, so
        # re-importing an older file (with an older-format adt) still
        # finds the same educator instead of creating a duplicate.
        select_educator = select(Educator)
        select_educator = select_educator.where(
            (Educator.adt == adt) | (Educator.previous_adt == adt)
        )
        select_educator = select_educator.order_by(Educator.id)

        educators = session.scalars(select_educator).all()

        return educators

    def findByFullNameAndSpec(lastName, name, father, spec):
        # Unlike findByNameAndSpecAll (which joins on the non-existent
        # Educator.am), this joins Qualifications back to Educator via
        # educator_id, which is the actual foreign key.
        educator_cls = aliased(Educator, name="e")
        qualifications_cls = aliased(Qualifications, name="q")

        select_join = select(educator_cls).distinct()
        select_join = select_join.join_from(
            educator_cls,
            qualifications_cls,
            qualifications_cls.educator_id == educator_cls.id,
        )
        select_join = select_join.where(qualifications_cls.specialization == spec)

        # LASTNAME
        if isinstance(lastName, list) and len(lastName) == 1:
            select_join = select_join.where(
                (educator_cls.lastname.like(f"{lastName[0]}%"))
            )
        elif isinstance(lastName, list) and len(lastName) >= 2:
            select_join = select_join.where(
                (educator_cls.lastname.like(f"{lastName[0]}%")) |
                (educator_cls.lastname.like(f"{lastName[1]}%"))
            )
        else:
            select_join = select_join \
                .where(educator_cls.lastname.like(f"{lastName}%"))

        # NAME
        if isinstance(name, list) and len(name) == 1:
            select_join = select_join.where(
                (educator_cls.name.like(f"{name[0][0:4]}%"))
            )
        elif isinstance(name, list) and len(name) >= 2:
            select_join = select_join.where(
                (educator_cls.name.like(f"{name[0][0:4]}%")) |
                (educator_cls.name.like(f"{name[1][0:4]}%"))
            )
        else:
            select_join = select_join \
                .where(educator_cls.name.like(f"{name[0:3]}%"))

        # FATHER
        if isinstance(father, list) and len(father) == 1:
            select_join = select_join.where(
                (educator_cls.father.like(f"{father[0][0:4]}%"))
            )
        elif isinstance(father, list) and len(father) >= 2:
            select_join = select_join.where(
                (educator_cls.father.like(f"{father[0][0:4]}%")) |
                (educator_cls.father.like(f"{father[1][0:4]}%"))
            )
        else:
            select_join = select_join \
                .where(educator_cls.father.like(f"{father[0:4]}%"))

        select_join = select_join.order_by(educator_cls.id)

        try:
            educators = session.scalars(select_join).all()
            return educators
        except Exception as e:
            logger.error(e)

        return []


    def findByFullName(lastName, name, father):
        select_educator = select(Educator)
        
        # LASTNAME
        if isinstance(lastName, list) and len(lastName) == 1:
            select_educator = select_educator.where(
                (Educator.lastname.like(f"{lastName[0]}%"))
            )
        elif isinstance(lastName, list) and len(lastName) >= 2:
            select_educator = select_educator.where(
                (Educator.lastname.like(f"{lastName[0]}%")) |
                (Educator.lastname.like(f"{lastName[1]}%"))
            )
        else:
            logger.debug(lastName)
            select_educator = select_educator \
                .where(Educator.lastname.like(f"{lastName}%"))

        # NAME
        if isinstance(name, list) and len(name) == 1:
            select_educator = select_educator.where(
                (Educator.name.like(f"{name[0][0:4]}%"))
            )
        elif isinstance(name, list) and len(name) >= 2:
            select_educator = select_educator.where(
                (Educator.name.like(f"{name[0][0:4]}%")) |
                (Educator.name.like(f"{name[1][0:4]}%"))
            )
        else:
            select_educator = select_educator \
                .where(Educator.name.like(f"{name[0:3]}%"))


        # FATHER 
        if isinstance(father, list) and len(father) == 1:
            select_educator = select_educator.where(
                (Educator.father.like(f"{father[0][0:4]}%"))
            )
        elif isinstance(father, list) and len(father) >= 2:
            select_educator = select_educator.where(
                (Educator.father.like(f"{father[0][0:4]}%")) |
                (Educator.father.like(f"{father[1][0:4]}%"))
            )
        else:
            select_educator = select_educator \
                .where(Educator.father.like(f"{father[0:4]}%"))

        try:
            educators = session.scalars(select_educator).all()
            return educators
        except Exception as e:
            logger.error(e)

        return []

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
                (educator_cls.lastname.like(f"{lastName[0]}%")) |
                (educator_cls.lastname.like(f"{lastName[1]}%"))
            )
        else:
            select_join = select_join \
                .where(educator_cls.lastname.like(f"{lastName}%"))

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

        educators = session.execute(select_join).all()
        
        return educators

    def findByFullNameAndAdtAll(lastName, name, father, adt):
        educator_cls = aliased(Educator, name="e")

        select_join = select(educator_cls)
        select_join = select_join.where(educator_cls.lastname == " ".join(lastName))
        select_join = select_join.where(educator_cls.name == " ".join(name))
        select_join = select_join.where(educator_cls.father == " ".join(father))
        select_join = select_join.where(educator_cls.adt == adt)

        educators = session.scalars(select_join).all()

        logger.debug(len(educators))
        logger.debug(
            select_join.compile(
                dialect=engine.dialect,
                compile_kwargs={"literal_binds": True}
            )
        )

        return educators


    # def findByAm(am):
    #     select_educator = select(Educator).where(Educator.am == am)
    #     educators = session.scalars(select_educator).all()

    #     return educators


Base.metadata.create_all(engine)