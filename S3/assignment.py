"""
Read the fish market CSV data.
Write a version of it that is transformed back to
s3 - 'data-eng-resources/Data26/fish/your-name'Transformation: data averaged by fish species
create csv of all 3 files with averages of all fish species and add to new csv file.
"""

import pymongo
import boto3
import pandas as pd
import numpy as np
from pprint import pprint as pp


class Fish:
    """
    Takes data from a set of fish csvs to find the average values of each fish.
    """

    def __init__(self, bucket_name: str, file_prefix: str, column_name: str):
        """
        Initialises the class and completes the required tasks to get the average values for each species of fish.
        The class has been made adaptive by giving the user the ability to specify which files to use and on which
        column to group the data on.
        :param bucket_name: The bucket name to be used. Must be a string.
        :param file_prefix: The starting characters in a file name. Must be a string.
        :param column_name: The column on which to group the data by. Must be a string.
        """
        self.column_name = column_name
        self.s3_client = boto3.client("s3")
        self.s3_resource = boto3.resource("s3")
        self.bucket_name = bucket_name
        self._load_bucket()
        self._create_dataframe(file_prefix)
        self._to_csv(column_name)
        self.s3_client.upload_file(Filename="Jad-fish-market.csv", Bucket=self.bucket_name,
                                   Key="Data26/fish/Jad.csv")

    def _load_bucket(self):
        """
        The bucket that we are using is added to a class variable, bucket_contents.
        :return:
        """
        self.bucket_contents = self.s3_client.list_objects_v2(Bucket=self.bucket_name)

    def _create_dataframe(self, file_prefix: str):
        """
        Creates a dataframe including all the specified files given by the prefix and suffix.
        All files must have the same columns.
        :param file_prefix: What the files should start with.
        :return:
        """
        # Create empty lists to store names from collected files.
        files = []
        data = []
        columns = []
        # Collects the files from the bucket with the specified prefixes and suffixes and adds the names of the files
        # to a list called files.
        for each in self.bucket_contents["Contents"]:
            if each["Key"].startswith(file_prefix) and each["Key"].endswith(".csv"):
                files.append(each["Key"])
        # This collects the data from the files with the names from the files list and appends them to a list after
        # transforming them to numpy arrays from dataframes.
        for file in files:
            s3_object = self.s3_client.get_object(Bucket=self.bucket_name, Key=file)
            arr = pd.read_csv(s3_object["Body"])
            # Collect the column names to apply back to the final dataframe.
            if len(columns) == 0:
                for col in arr.columns:
                    columns.append(col)
            data.append(arr.to_numpy())
        # Turn the list of lists into a single list with all the data.
        data = [item for sublist in data for item in sublist]
        data = np.array(data)
        # Create the final dataframe and fix the columns and index.
        self.df = pd.DataFrame(data)
        self.df.columns = columns
        self.df = self.df.reset_index()
        self.df = self.df.drop("index", axis=1)

    def _to_csv(self, column_name):
        """
        Creates a csv and a new dataframe of the averaged data grouped by column_name.
        :param column_name: Must be a string.
        :return:
        """
        round(self.average(column_name), 2).to_csv("Jad-fish-market.csv")
        self.averages = round(self.average(column_name), 2)

    def average(self, column_name):
        """
        Gets the averages for each column grouped by the column_name.
        :param column_name: Must be a string.
        :return:
        """
        return self.df.groupby(column_name).mean()


    def print_data(self, avg : bool=False):
        """
        Prints the final dataset.
        :param avg: If True, prints the mean of the data grouped by the given column. If False, prints the dataframe.
                    Must be Boolean value.
        """
        if avg:
            print(self.averages)
        else:
            print(self.df)

    def turn_dict(self, averages):
        """
        Turn my dataframe into a list of dictionaries.
        :return: list of dictionaries
        """
        df_with_index = averages
        if self.column_name not in df_with_index:
            df_with_index[self.column_name] = df_with_index.index
        cols = df_with_index.columns.tolist()
        cols = cols[-1:] + cols[:-1]
        df_with_index = df_with_index[cols]
        dict_df = df_with_index.to_dict(orient="records")
        return dict_df

    def to_mongo(self, client_id: str, collection_name: str, df):
        """
        Upload the list of dictionaries to the mongoDB collection
        :param client_id: the MongoDB client ID
        :param collection_name: The name of the collection to be created and used
        :return:
        """
        client = pymongo.MongoClient(client_id)
        db = client.Sparta
        db[collection_name].drop()
        db[collection_name].insert_many(self.turn_dict(df))
        return db["fishMarket"].find()

if __name__ == "__main__":

    pd.set_option('display.max_rows', 500)
    pd.set_option('display.max_columns', 500)
    pd.set_option('display.width', 1000)
    bucket_name = "data-eng-resources"
    file_prefix = "python/fish-market"
    mongo_client = "mongodb://35.156.9.121:27017/Sparta"
    collection = "fishMarket"

    Trial = Fish(bucket_name, file_prefix, column_name="Species")

    dicts = Trial.to_mongo(mongo_client, collection, Trial.averages)

    for each in dicts:
        pp(each)
