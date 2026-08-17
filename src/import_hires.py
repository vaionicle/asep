#!python

import xlrd
import sys
import parsers._2023_hires as hire_tables_2023
import parsers._2025_hires as hire_tables_2025
import database as mydb
import logging
from database.Educator import Educator
from database.Qualifications import Qualifications
from database.Hire import Hire
from parsers import parse_int

HIRE_TABLES = {
    2023: hire_tables_2023,
    2025: hire_tables_2025,
}

logger = logging.getLogger('hires')
logger.setLevel(logging.INFO)
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
# ch.setLevel(logging.DEBUG)

# add ch to logger
logger.addHandler(ch)

# python /opt/asep/src/import_hires.py 2025 2026 "2025-26" "A" "anaplirotes/2025-26/a_fasi/Προσλήψεις_ΓΕΝΙΚΗ_ΠΕ_20250904_int.xls"

if __name__ == "__main__":
    try:
        year = parse_int(sys.argv[1])                  # hire file layout: 2023 or 2025
        qualifications_year = parse_int(sys.argv[2])    # qualifications cohort to match against: 2023 or 2026
        school_year = sys.argv[3]
        round = sys.argv[4]
        fileName = sys.argv[5]

        logger.info(f"{school_year:<8} {round:<2} quals={qualifications_year:<4} {fileName}")

        book = xlrd.open_workbook(filename=f"/opt/asep/tmp/{fileName}")

        sh = book.sheet_by_index(0)

        logger.debug(f"{sh.name} {sh.nrows} {sh.ncols}")
        logger.debug("The number of worksheets is {0}".format(book.nsheets))
        logger.debug("Worksheet name(s): {0}".format(book.sheet_names()))

        h = HIRE_TABLES.get(year)

        init_row = getattr(h, 'init_row', 0)
        end_row = sh.nrows - getattr(h, 'end_row', sh.nrows)

        for rx in range(init_row, end_row):
            msg = []
            row = sh.row(rx)

            row_hire = h.hire(row, school_year=school_year, round=round)

            logger.debug(row_hire)

            lastName = row_hire['lastname']
            name = row_hire['name']
            father = row_hire['father']
            spec = row_hire['specialization']
            aa_row = row_hire['aa_row']

            lastNameStr = " ".join(lastName) if isinstance(lastName, list) else lastName
            nameStr = " ".join(name) if isinstance(name, list) else name
            fatherStr = " ".join(father) if isinstance(father, list) else father

            msg.append(f"{spec:<10} {lastNameStr:<25} {nameStr:<25} {fatherStr:<25}")

            try:
                action = ""
                educator = None

                # 1. Primary match: the hire row's position in the hiring
                #    "flow" (aa_row) is the same position ("aa") the
                #    person had in that year's qualifications ranking
                #    table, for the same specialization.
                qualifications = Qualifications.findByYearSpecAndAa(
                    year_of_import = qualifications_year,
                    specialization = spec,
                    aa             = aa_row,
                )

                if len(qualifications) == 1:
                    action = "MATCHED (aa)"
                    educator = mydb.connect.session.get(Educator, qualifications[0].educator_id)

                # 2. Fallback: rankings can shift between the
                #    qualifications list and a later hiring phase, so if
                #    the aa position didn't resolve to exactly one
                #    qualification, fall back to a name + spec match.
                #    Never skip the row: if that's still ambiguous or
                #    empty, create a new educator rather than guessing.
                if educator is None:
                    educatorList = Educator.findByFullNameAndSpec(
                        lastName = lastName,
                        name     = name,
                        father   = father,
                        spec     = spec,
                    )

                    if len(educatorList) == 1:
                        action = "MATCHED (name+spec)"
                        educator = educatorList[0]
                    else:
                        if len(educatorList) > 1:
                            action = "CREATED [+] (ambiguous match)"
                            logger.warning(
                                f"Ambiguous educator match {lastNameStr}/{nameStr}/{fatherStr} "
                                f"spec={spec}: candidates={[e.id for e in educatorList]}"
                            )
                        else:
                            action = "CREATED [+]"

                        educator = Educator.createRow({
                            "lastName": lastName,
                            "name": name,
                            "father": father,
                            "adt": "",
                        })

                mydb.connect.session.add(educator)
                mydb.connect.session.commit()

            except Exception as e:
                logger.error(e)
                continue

            msg.append(f"EDU: {action:<24}")

            try:
                action = ""

                row_hire['educator_id'] = educator.id

                hires = Hire.findByEducatorIDYearAndRound(educator.id, school_year, round)

                if len(hires) == 0:
                    action = "CREATED [+]"
                    hire = Hire.createRow(row_hire)
                    mydb.connect.session.add(hire)
                else:
                    action = "UPDATED"
                    hires[0].updateRow(row_hire)
                    mydb.connect.session.add(hires[0])

            except Exception as e:
                logger.error(e)

            msg.append(f"HIRE: {action:<12}")

            msg = " ".join(msg)
            logger.info(f"{msg}")

            mydb.connect.session.commit()
    except KeyboardInterrupt:
        mydb.connect.session.commit()

        logger.info("STOPPED")
