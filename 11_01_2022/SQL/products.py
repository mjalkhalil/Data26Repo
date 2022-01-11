import decimal
from collections import Counter
import pandas as pd

import pyodbc

class Products:

    def __init__(self):
        self.server = 'localhost,1433'
        self.database = 'Northwind'
        self.username = 'SA'
        self.password = 'Passw0rd2018'
        self.northwind = pyodbc.connect(f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={self.server};'
                                        f'DATABASE={self.database};UID={self.username};PWD={self.password}')
        self.cursor = self.northwind.cursor()

    def _sql_query(self, sql_query):
        return self.cursor.execute(sql_query)

    def print_records(self, column):
        query = self._sql_query(f"SELECT * FROM {column}")
        while True:
            record = query.fetchone()
            if record is None:
                break
            print(record)

    def avg_unit_price(self):
        query = self._sql_query(f"SELECT * FROM PRODUCTS")
        count = 0
        total = 0
        while True:
            record = query.fetchone()
            if record is None:
                break
            count += 1
            total += record.UnitPrice
        avg = total / count
        return avg

    def employees_per_region(self):
        query = self._sql_query("""SELECT * FROM Employees e
                                INNER JOIN EmployeeTerritories et ON e.EmployeeID = et.EmployeeID
                                INNER JOIN Territories t ON t.TerritoryID = et.TerritoryID
                                INNER JOIN Region r ON r.RegionID = t.RegionID""")

        region = []
        employeeid = []
        while True:
            record = query.fetchone()
            if record is None:
                break
            region.append(record.RegionDescription)
            employeeid.append(record.EmployeeID)

        # columns = [columns[0] for columns in self.cursor.description]
        # print(columns)

        records = set(list(zip(region, employeeid)))

        return Counter([x[0] for x in records])

    def company_purchases_above_15k(self):
        query = self._sql_query("""SELECT * FROM Customers c
                                    INNER JOIN Orders o ON c.CustomerID = o.CustomerID
                                    INNER JOIN [Order Details Extended] od ON o.OrderID = od.OrderID""")
        companies = []
        prices = []
        order_date = []
        while True:
            record = query.fetchone()
            if record is None:
                break
            companies.append(record.CompanyName)
            prices.append(record.ExtendedPrice)
            order_date.append(record.OrderDate)

        columns = [columns[0] for columns in self.cursor.description]
        print(columns)

        prices = [float(x) for x in prices]
        records = list(zip(companies, prices, order_date))
        records = pd.DataFrame(records)
        records[1] = records[1].groupby(records[0]).transform('sum')
        records = records.drop_duplicates()
        records = records[records[1] > 15000]
        records = records[records[2] >= '1996-04-01']
        records = records.reset_index()
        records = records.drop('index', axis=1)
        records = pd.concat([records[0], records[1]], axis=1)
        records = records.drop_duplicates()
        records = records.sort_values(by=[1], ascending=False)
        records = records.reset_index()
        records = records.drop('index', axis=1)
        records.index += 1

        return records
