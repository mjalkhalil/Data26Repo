"""
Read the fish market CSV data.
Write a version of it that is transformed back to
s3 - 'data-eng-resources/Data26/fish/your-name'Transformation: data averaged by fish species
create csv of all 3 files with averages of all fish species and add to new csv file.
"""

import boto3
import pandas as pd
import numpy as np

class Fish:
    """
    Takes data from a set of fish csvs to find the average values of each fish.
    """

    def __init__(self, bucket_name: str, filename: str):
        self.s3_client = boto3.client("s3")
        self.s3_resource = boto3.resource("s3")
        self.bucket_name = bucket_name
        self._load_bucket()
        self._create_dataframe(filename)
        self._to_csv()
        print(self.averages)
        self.s3_client.upload_file(Filename="Jad-fish-market.csv", Bucket=self.bucket_name,
                                   Key="Data26/fish/Jad.csv")

    def _load_bucket(self):
        self.bucket_contents = self.s3_client.list_objects_v2(Bucket=self.bucket_name)

    def _create_dataframe(self, filename: str):
        i = 0
        files = []
        data = []
        columns = []
        for each in self.bucket_contents["Contents"]:
            if each["Key"].startswith(filename) and each["Key"].endswith(".csv"):
                files.append(each["Key"])
        for file in files:
            s3_object = self.s3_client.get_object(Bucket=self.bucket_name, Key=file)
            arr = pd.read_csv(s3_object["Body"])
            if len(columns) == 0:
                for col in arr.columns:
                    columns.append(col)
            data.append(arr.to_numpy())
            i += 1
        data = [item for sublist in data for item in sublist]
        data = np.array(data)
        self.df = pd.DataFrame(data)
        self.df.columns = columns
        self.df = self.df.reset_index()
        self.df = self.df.drop("index", axis=1)

    def _to_csv(self):
        round(self.average(), 2).to_csv("Jad-fish-market.csv")
        self.averages = round(self.average(), 2)

    def average(self):
        return self.df.groupby("Species").mean()


    def print_data(self):
        print(self.df)
        return self.df

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

bucket_name = "data-eng-resources"
file_prefix = "python/fish-market"

Trial = Fish(bucket_name, file_prefix)
