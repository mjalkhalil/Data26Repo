import pyodbc
from pprint import pprint as pp
import pandas as pd
import numpy as np


def pandas_options():
    pd.set_option('display.max_rows', 1000)
    pd.set_option('display.max_columns', 500)
    pd.set_option('display.width', 1000)


def connect_to_database(server, database, username, password):
    northwind = pyodbc.connect(f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};'
                               f'DATABASE={database};UID={username};PWD={password}')
    return northwind.cursor()


pandas_options()
cursor = connect_to_database('localhost,1433', 'Northwind', 'SA', 'Passw0rd2018')

rows = cursor.execute("SELECT * FROM products")
columns = [columns[0] for columns in cursor.description]
# pp(row)
# print("\n\n")
# np_array = np.array(row)
# df = pd.DataFrame(np_array, columns=columns)
# df = df.drop(0, axis=1)
# pp(df)

count = 0
total = 0

while True:
    record = rows.fetchone()
    if record is None:
        break
    count += 1
    total += record.UnitPrice

avg = total/count
print(round(avg, 4))
