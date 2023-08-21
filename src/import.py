#!python

import xlrd
import json
import tables2023
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
    end_row = 28
    # end_row = sh.nrows-28

    for rx in range(init_row, end_row):
        row = sh.row(rx)

        ekpedeutikos = tables2023.ekpedeutikos(row, fileName)
        qualifications = tables2023.qualifications(row, fileName)
        output = {
            "ekpedeutikos": ekpedeutikos,
            "qualifications": qualifications
        }

        if debug:
            print(row)
            print(output)
            print(type(output))
            print(json.dumps(output, sort_keys=True, ensure_ascii=False, indent=4))

        educator = Educator.createRow(ekpedeutikos)
        qualifications = Qualifications.createRow(qualifications)

        # educatorSQL = select(Educator).where(Educator.am == ekpedeutikos['am'])

        # session.execute(select(User.name, User.fullname)).first()

        # exists = mydb.connect.session.query(Educator).filter_by(am = ekpedeutikos['am'])
        
        Educator.select().where(Educator.columns.am == ekpedeutikos['am'])
        
# query = Student.select().where(Student.columns.Major == 'English')
# output = conn.execute(query)
# print(output.fetchall())


        print(exists)
        # print(type(exists))
        # if exists is None:
        #     mydb.connect.session.add(educator)


        # exists = mydb.connect.session.query(Qualifications).filter_by(
        #     am = ekpedeutikos['am'],
        #     file = fileName
        # )
        # if exists is None:
        #     mydb.connect.session.add(qualifications)

    mydb.connect.session.commit()
