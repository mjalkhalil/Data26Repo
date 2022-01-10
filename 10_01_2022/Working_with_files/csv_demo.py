import csv
import pandas as pd
import numpy as np

def transform_user_details(file):
    csv_df = pd.read_csv(file)
    csv_array = csv_df.to_numpy()
    new_csv = []
    for row in csv_array:
        transformation = [row[1], row[2], row[-1]]
        new_csv.append(transformation)

    return pd.DataFrame(np.array(new_csv), columns=["First Name", "Last Name", "email"])

def create_new_Data(old_file, new_file):
    new_data = transform_user_details(old_file)
    new_data.to_csv(new_file,mode='w', index=False)

create_new_Data("user_details.csv", "new_user_details.csv")