import csv
import pandas as pd

with open("user_details.csv", newline='') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',')

    print(csvreader)

csv_read = pd.read_csv("user_details.csv")

print(csv_read)