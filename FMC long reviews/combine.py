import xlrd
import pandas as pd
import os


total = pd.DataFrame()

dir_list = os.listdir(os.getcwd())
for i in dir_list:
    if i.endswith(".xlsx"):
        df = pd.read_excel(i)
        total = total.append(df, ignore_index=True)
        print(total)
        
with pd.ExcelWriter("Farewell my Concubine total.xlsx") as writer:
    total.to_excel(writer, index = False)