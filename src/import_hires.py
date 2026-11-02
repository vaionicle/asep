#!python

import xlrd
import sys
import parsers._2023_hires as hire_tables_2023
import parsers._2025_hires as hire_tables_2025
import store
import logging
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

# python /opt/asep/src/import_hires.py 2025 "2025-26" "A" "anaplirotes/2025-26/a_fasi/Προσλήψεις_ΓΕΝΙΚΗ_ΠΕ_20250904_int.xls"

if __name__ == "__main__":
    try:
        year = parse_int(sys.argv[1])                  # hire file layout: 2023 or 2025
        school_year = sys.argv[2]
        round = sys.argv[3]
        fileName = sys.argv[4]

        logger.info(f"{school_year:<8} {round:<2} {fileName}")

        book = xlrd.open_workbook(filename=f"/opt/asep/tmp/{fileName}")

        sh = book.sheet_by_index(0)

        logger.debug(f"{sh.name} {sh.nrows} {sh.ncols}")
        logger.debug("The number of worksheets is {0}".format(book.nsheets))
        logger.debug("Worksheet name(s): {0}".format(book.sheet_names()))

        h = HIRE_TABLES.get(year)
        teachers = store.get_teachers()

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
                _, action = store.save_hire(teachers, row_hire)
            except Exception as e:
                logger.error(e)
                continue

            msg.append(f"TEACHER: {action:<20}")

            msg = " ".join(msg)
            logger.info(f"{msg}")

    except KeyboardInterrupt:
        logger.info("STOPPED")
