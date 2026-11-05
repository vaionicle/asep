#!python

import xlrd
import sys
import parsers._2023_tables_2GE as qualification_tables_2023
import parsers._2026_tables_2GE as qualification_tables_2026
import store
import logging
from parsers import parse_int

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
        teachers = store.get_teachers()

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

            row_qualifications['year_of_import'] = year
            row_qualifications['file'] = fileName
            row_qualifications['specialization'] = spec

            try:
                _, action = store.save_ranking(teachers, {
                    "lastname": row_ekpedeutikos['lastName'],
                    "name":     row_ekpedeutikos['name'],
                    "father":   row_ekpedeutikos['father'],
                    "adt":      adt,
                }, row_qualifications)
            except Exception as e:
                logger.error(e)
                continue

            msg.append(f"TEACHER: {action:<20}")

            msg = " ".join(msg)
            logger.info(f"{msg}")

    except KeyboardInterrupt:
        logger.info("STOPPED") 


