#!python

import xlrd
import sys
import parsers._2023_tables_2GE as qualification_tables_2023
import parsers._2026_tables_2GE as qualification_tables_2026
import database as mydb
import logging
from database.Educator import Educator
from database.Qualifications import Qualifications
from parsers import parse_int

from sqlalchemy import select

QUALIFICATION_TABLES = {
    2023: qualification_tables_2023,
    2026: qualification_tables_2026,
}

logger = logging.getLogger('qualifications')
logger.setLevel(logging.INFO)
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
# ch.setLevel(logging.DEBUG)

# add ch to logger
logger.addHandler(ch)

if __name__ == "__main__":
    try:
        n = len(sys.argv)

        spec = sys.argv[1]
        fileName = sys.argv[2]
        year = parse_int(sys.argv[3])

        logger.info(f"{year:<4} {spec:<7} {fileName}")

        book = xlrd.open_workbook(filename=f"/opt/asep/tmp/{fileName}")

        sh = book.sheet_by_index(0)

        logger.debug(f"{sh.name} {sh.nrows} {sh.ncols}")
        logger.debug("The number of worksheets is {0}".format(book.nsheets))
        logger.debug("Worksheet name(s): {0}".format(book.sheet_names()))

        q = QUALIFICATION_TABLES.get(year)

        init_row = getattr(q, 'init_row', 0)
        end_row = sh.nrows - getattr(q, 'end_row', sh.nrows)

        for rx in range(init_row, end_row):
            msg = []
            row = sh.row(rx)
            
            row_ekpedeutikos = q.ekpedeutikos(row)
            row_qualifications = q.qualifications(row, fileName, spec)

            logger.debug(row_ekpedeutikos)

            aa = row_qualifications['aa']
            am = row_qualifications['am']
            adt = row_ekpedeutikos['adt']
            
            lastName = " ".join(row_ekpedeutikos['lastName'])
            name = " ".join(row_ekpedeutikos['name'])
            father = " ".join(row_ekpedeutikos['father'])

            msg.append(f"{year:<4}-{spec:<5} {aa:<6} {am:<10} {adt:<15} {lastName:<30} {name:<30} {father:<25}")

            try:
                action = ""
                educator = None

                # ADT (govID) is unique per educator and is normally
                # authoritative. Spec must NOT be part of this match: an
                # educator can hold several specializations, so filtering
                # by spec would miss them the first time we import a spec
                # they don't have a Qualifications row for yet, creating
                # a duplicate Educator instead of reusing the existing
                # one.
                if adt not in ("", "0"):
                    educatorList = Educator.findByAnyAdt(adt)

                    if len(educatorList) == 0:
                        # Not found under the current or a previously-seen
                        # adt. Could be a genuinely new educator, or an
                        # existing one whose adt format just changed (eg.
                        # ΑΙ519314 -> Α00576786) and we haven't recorded it
                        # for them yet - fall back to a name match so we
                        # update the existing person (and record both
                        # adts via updateRow) instead of duplicating them.
                        educatorList = Educator.findByFullName(
                            lastName = row_ekpedeutikos['lastName'],
                            name     = row_ekpedeutikos['name'],
                            father   = row_ekpedeutikos['father'],
                        )
                else:
                    educatorList = Educator.findByFullName(
                        lastName = row_ekpedeutikos['lastName'],
                        name     = row_ekpedeutikos['name'],
                        father   = row_ekpedeutikos['father'],
                    )

                if len(educatorList) == 1:
                    action = "UPDATED"
                    educatorList[0].updateRow(row_ekpedeutikos)
                    educator = educatorList[0]
                else:
                    # 0 matches -> genuinely new educator.
                    # >1 matches -> can't tell which one is "the" match;
                    # never guess and overwrite an unrelated existing
                    # record, so create a new row and flag it for a human
                    # to reconcile instead of silently merging or dropping
                    # the incoming data.
                    if len(educatorList) > 1:
                        action = "CREATED [+] (ambiguous match)"
                        logger.warning(
                            f"Ambiguous educator match adt={adt!r} "
                            f"{lastName}/{name}/{father} spec={spec}: "
                            f"candidates={[e.id for e in educatorList]}"
                        )
                    else:
                        action = "CREATED [+]"

                    educator = Educator.createRow(row_ekpedeutikos)

                mydb.connect.session.add(educator)
                mydb.connect.session.commit()

            except Exception as e:
                logger.error(e)
                continue

            msg.append(f"EDU: {action:<11}")

            try:
                action = ""

                qualifications = Qualifications.findBy(spec, educator.id, am)

                row_qualifications['educator_id'] = educator.id
                row_qualifications['year_of_import'] = year
                row_qualifications['file'] = fileName
                row_qualifications['specialization'] = spec

                if len(qualifications) == 0:
                    action = "CREATED [+]"
                    qualification = Qualifications.createRow(row_qualifications)
                    mydb.connect.session.add(qualification)
                else:
                    action = "UPDATED"
                    qualifications[0].updateRow(row_qualifications)
                    mydb.connect.session.add(qualifications[0])

            except Exception as e:
                logger.error(e)

            msg.append(f"QUAL: {action:<20}")

            msg = " ".join(msg)
            logger.info(f"{msg}")

            mydb.connect.session.commit()
    except KeyboardInterrupt:
        mydb.connect.session.commit()

        logger.info("STOPPED") 


