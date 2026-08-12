#!python

import xlrd
import sys
import parsers._2023_tables_2GE as qualification_tables_2023
import parsers._2026_tables_2GE as qualification_tables_2026
import database as mydb
import logging
from database.Educator import Educator
from database.Qualifications import Qualifications
from sqlalchemy import select

logger = logging.getLogger('qualifications')
logger.setLevel(logging.INFO)
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
# ch.setLevel(logging.DEBUG)

# add ch to logger
logger.addHandler(ch)

# python /opt/asep/src/import_qualifications.py "ΠΕ02" "anaplirotes/2GE_2026_PROSORINOI/1_ΚΑΤ_ΠΕ02 ΦΙΛΟΛΟΓΟΙ_ΓΕΝ (ΜΕ ΕΜΠ.)_ΒΠ.xls"

if __name__ == "__main__":
    try:
        n = len(sys.argv)

        spec = sys.argv[1]
        fileName = sys.argv[2]
        year = "2026"

        logger.debug(f"{year:<4} {spec:<7} {fileName}")
        
        book = xlrd.open_workbook(filename=f"/opt/asep/tmp/{fileName}")

        sh = book.sheet_by_index(0)

        logger.debug(f"{sh.name} {sh.nrows} {sh.ncols}")
        logger.debug("The number of worksheets is {0}".format(book.nsheets))
        logger.debug("Worksheet name(s): {0}".format(book.sheet_names()))

        init_row = 7
        # init_row = sh.nrows - 100
        end_row = sh.nrows-36
        # end_row = 205

        for rx in range(init_row, end_row):
            msg = []
            row = sh.row(rx)
            
            row_ekpedeutikos = qualification_tables_2026.ekpedeutikos(row)
            row_qualifications = qualification_tables_2026.qualifications(row, fileName, spec)

            # logger.debug(row_ekpedeutikos)

            adt = row_ekpedeutikos['adt']
            
            lastName = " ".join(row_ekpedeutikos['lastName'])
            name = " ".join(row_ekpedeutikos['name'])
            father = " ".join(row_ekpedeutikos['father'])

            msg.append(f"{adt:<15} {lastName:<25} {name:<25} {father:<25}")

            try:
                action = ""
                
                if adt == "" or adt == "0":
                    raise "NO ADT"

                educatorList = Educator.findByFullNameAndAdtAll(
                    lastName = row_ekpedeutikos['lastName'],
                    name     = row_ekpedeutikos['name'],
                    father   = row_ekpedeutikos['father'],
                    adt      = adt
                )

                if len(educatorList) == 0:                    
                    action = "CREATED [+]"
                    educator = Educator.createRow(row_ekpedeutikos)

                elif len(educatorList) == 1:
                    action = "UPDATED"
                    educatorList[0].updateRow(row_ekpedeutikos)
                    educator = educatorList[0]
                
                else:
                    logger.debug(len(educatorList))
                    action = "WTF"
                    
                    raise "WTF"

                mydb.connect.session.add(educator)
                mydb.connect.session.commit()
    
            except Exception as e:
                logger.error(e)

            msg.append(f"EDU: {action:<12}")

            try:
                action = ""

                qualifications = Qualifications.findBy(spec, educator.id)

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

            msg.append(f"QUAL: {action:<12}")

            msg = " ".join(msg)
            logger.info(f"{msg}")

            mydb.connect.session.commit()
    except KeyboardInterrupt:
        mydb.connect.session.commit()

        logger.info("STOPPED") 


