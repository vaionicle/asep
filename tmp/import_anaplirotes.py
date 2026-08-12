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

logger = logging.getLogger('anaplirotes')
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
        phase = sys.argv[2]
        fileName = sys.argv[3]

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
            row_hire = hire_2023.hire(row, school_year=school_year, round=phase)

            try:
                e_index = 0
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

                msg.append(f"{row_hire['a/a']:<4} {row_hire['main_table_order']:<5} {phase:<1} {spec:<10} {lastname:<25} {name:<25} {father:<25}")

                msg.append("Educator")
                if len(educators) == 1:
                    msg.append("😁")
                elif len(educators) == 0:
                    msg.append("😡")
                elif len(educators) > 1:
                    msg.append("😱")
                    logger.info(" ".join(msg))
                    msg = []
                    idx = 0
                    for educator in educators:
                        e = educator[0]
                        q = educator[1]
                        if q.total_score == row_hire['main_table_score']:
                            e_index = idx
                            logger.info(f"|--> ADT: {e.adt:<10} AM: {e.am:<6} score: {q.total_score}=={row_hire['main_table_score']} <-- selected")
                        else:
                            logger.info(f"|--> ADT: {e.adt:<10} AM: {e.am:<6} score: {q.total_score}=={row_hire['main_table_score']}")
                        idx += 1

            except Exception as e:
                msg.append(f"💥 -> {e}")
            
            if len(educators) == 0 or len(educators) > 1:
                logger.info(" ".join(msg))
                continue

            msg.append("|")
            try:
                hires = Hire.findByAmYearRoundAndSpec(
                    am=educators[e_index][0].am,
                    spec=spec,
                    round=phase,
                    year=school_year
                )

                msg.append("Hire")
                if len(hires) == 1:
                    msg.append("💚")
                    hires[0].updateRow(row_hire, educators[e_index][0].am, fileName)

                elif len(hires) == 0:
                    msg.append("❤️")
                    hire = Hire.createRow(row_hire, educators[e_index][0].am, fileName)

                    mydb.connect.session.add(hire)

                elif len(hires) > 1:
                    raise Exception("MORE THAN ONE")

            except Exception as e:
                msg.append(f"💥 -> {e}")

            logger.info(" ".join(msg))
            mydb.connect.session.commit()

    except KeyboardInterrupt as e:
        logger.info(" ".join(msg))
        logger.info("STOPPED")
