#!python

import pandas as pd
 
# read by default 1st sheet of an excel file
dataframe1 = pd.read_excel('./tmp/2GE_2023_PROSORINOI_PINAKES_KATATAXIS_APORRIPTEON/1_ΚΑΤ_ΠΕ02 ΦΙΛΟΛΟΓΟΙ.xls')
 
# print(dataframe1)

# dataframe1 = dataframe1.active

# Iterate the loop to read the cell values
for row in range(5, dataframe1.max_row):
    for col in dataframe1.iter_cols(1, dataframe1.max_column):
        print(col[row].value)