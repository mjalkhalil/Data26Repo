import products
from pprint import pprint as pp
import pyodbc


query = products.Products()

#query.print_records("Products")

#pp(query.employees_per_region())

# pp(query.company_purchases_above_15k())

for driver in pyodbc.drivers():
    print(driver)