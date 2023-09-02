#!python

import xlrd
import json
import parsers.tables2023 as tables2023
import database as mydb
from database.Educator import Educator
from database.Qualifications import Qualifications
from sqlalchemy import select

debug = False

if __name__ == "__main__":

    fileName = "2GE_2023_PROSORINOI_PINAKES_KATATAXIS_APORRIPTEON_1_ΚΑΤ_ΠΕ02 ΦΙΛΟΛΟΓΟΙ"
    book = xlrd.open_workbook(
        filename='/opt/asep/tmp/2GE_2023_PROSORINOI_PINAKES_KATATAXIS_APORRIPTEON/1_ΚΑΤ_ΠΕ02 ΦΙΛΟΛΟΓΟΙ.xls',
    )

    print("The number of worksheets is {0}".format(book.nsheets))
    print("Worksheet name(s): {0}".format(book.sheet_names()))

    sh = book.sheet_by_index(0)

    print("{0} {1} {2}".format(sh.name, sh.nrows, sh.ncols))

    init_row = 6
    end_row = 1000
    # end_row = sh.nrows-28

    for rx in range(init_row, end_row):
        row = sh.row(rx)

        row_ekpedeutikos = tables2023.ekpedeutikos(row)
        row_qualifications = tables2023.qualifications(row, fileName)
        
        am =  row_ekpedeutikos['am']
        if debug:
            parsed_row = {"ekpedeutikos": row_ekpedeutikos, "qualifications": row_qualifications}

            print(row)
            print(parsed_row)
            print(type(parsed_row))
            print(json.dumps(parsed_row, sort_keys=True, ensure_ascii=False, indent=4))

        print(f"{rx:<5} AM {am:<8}", end="")

        try:
            select_educator = select(Educator).where(Educator.am == am)    
            educators = mydb.connect.session.scalars(select_educator).all()

            if len(educators) == 0:
                raise Exception("NOT FOUND")
            else:
                print(f"EDUCATOR FOUND", end=" | ")
        except Exception as e:
            print(f"EDUCATOR NOT FOUND - {e}", end=" | ")
            educator = Educator.createRow(row_ekpedeutikos)
            mydb.connect.session.add(educator)

        try:
            select_qualification = select(Qualifications) \
                .where(Qualifications.am == am) \
                .where(Qualifications.year_of_import == "2023")
            qualifications = mydb.connect.session.scalars(select_qualification).all()

            if len(qualifications) == 0:
                raise Exception()
            else:
                qualifications[0].updateRow(row_qualifications)
                print(f"QUALIFICATION FOUND", end=" | ")
        except Exception as e:
            print(f"QUALIFICATION NOT FOUND - {e}", end=" | ")
            qualification = Qualifications.createRow(row_qualifications, "2023")
            mydb.connect.session.add(qualification)

        print(f"")
        mydb.connect.session.commit()


