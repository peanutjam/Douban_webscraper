import xlrd
import pandas as pd

df = pd.DataFrame()
df = pd.read_excel("Farewell my Concubine total.xlsx")
df['Username'] = df['Username'].astype(str)

df = df.sort_values(by=["Username"])

# for i in range(len(df) - 1):
#     print(df.loc[i,"Username"])

print(df.drop_duplicates(subset=["Username"]))

df = df.drop_duplicates(subset=["Username"])

        
with pd.ExcelWriter("Farewell my Concubine total (edited).xlsx") as writer:
    df.to_excel(writer, index = False)