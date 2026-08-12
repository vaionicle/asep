#!python

import sys
import xlrd
import json
import logging
import parsers._2023_hires as hire_2023

import database as mydb

from database.Educator import Educator
from database.Hire import Hire
# from database.Qualifications import Qualifications
# from sqlalchemy import select

logger = logging.getLogger('hires')
logger.setLevel(logging.INFO)
# logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
ch.setLevel(logging.DEBUG)

# add ch to logger
logger.addHandler(ch)

if __name__ == "__main__":
    try:
        # Code that may raise KeyboardInterrupt

        school_year = sys.argv[1]
        fileName = sys.argv[2]

        book = xlrd.open_workbook(filename=f'/opt/asep/tmp/{fileName}')
        sh = book.sheet_by_index(0)

        logger.debug(f"{sh.name} {sh.nrows} {sh.ncols}")
        logger.debug("The number of worksheets is {0}".format(book.nsheets))
        logger.debug("Worksheet name(s): {0}".format(book.sheet_names()))

        init_row = 1
        end_row = sh.nrows
        
        # exit()

        for rx in range(init_row, end_row):
            msg = []
            row = sh.row(rx)
            row_hire = hire_2023.hire(row, school_year=school_year)

            try:
                educators = Educator.findByNameAndSpecAll(
                    father   = row_hire['father'],
                    name     = row_hire['name'],
                    lastName = row_hire['lastname'],
                    spec     = row_hire['spec']
                )

                lastname    = row_hire['lastname']      if not isinstance(row_hire['lastname'], list)   else "-".join(row_hire['lastname'])
                name        = row_hire['name']          if not isinstance(row_hire['name'], list)       else "-".join(row_hire['name'])
                father      = row_hire['father']        if not isinstance(row_hire['father'], list)     else "-".join(row_hire['father'])
                spec        = row_hire['spec']

                msg.append(f"{row_hire['main_table_order']:<5} {spec:<10} {lastname:<25} {name:<25} {father:<25}")

                msg.append("Educator")
                if len(educators) == 1:
                    msg.append("FOUND")
                elif len(educators) == 0:
                    msg.append("NOT FOUND")
                elif len(educators) > 1:
                    raise Exception("MORE THAN ONE")
            except Exception as e:
                msg.append(f"EXCEPTION {e}")
            
            if len(educators) == 0 or len(educators) > 1:
                continue

            msg.append("|")
            try:
                hires = Hire.findByAmYearRoundAndSpec(
                    am=educators[0].am,
                    spec=spec,
                    round=phase,
                    year=school_year
                )

                msg.append("Hire: ")
                if len(hires) == 1:
                    msg.append("UPDATED")
                    hires[0].updateRow(row_hire, educators[0].am, fileName)

                elif len(hires) == 0:
                    msg.append("CREATED")
                    hire = Hire.createRow(row_hire, educators[0].am, fileName)

                    mydb.connect.session.add(hire)

                elif len(hires) > 1:
                    raise Exception("MORE THAN ONE")

            except Exception as e:
                msg.append(f"EXCEPTION {e}")
            
            logger.info(" ".join(msg))
            mydb.connect.session.commit()

    except KeyboardInterrupt as e:
        logger.info(" ".join(msg))
        logger.info("STOPPED")
