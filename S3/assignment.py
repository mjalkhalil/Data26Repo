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

    def __init__(self, bucket_name: str, file_prefix: str, file_suffix: str, column_name: str):
        """
        Initialises the class and completes the required tasks to get the average values for each species of fish.
        The class has been made adaptive by giving the user the ability to specify which files to use and on which
        column to group the data on.
        :param bucket_name: The bucket name to be used. Must be a string.
        :param file_prefix: The starting characters in a file name. Must be a string.
        :param file_suffix: The ending characters in a file name. Must be a string.
        :param column_name: The column on which to group the data by. Must be a string.
        """
        self.s3_client = boto3.client("s3")
        self.s3_resource = boto3.resource("s3")
        self.bucket_name = bucket_name
        self._load_bucket()
        self._create_dataframe(file_prefix, file_suffix)
        self._to_csv(column_name)
        self.s3_client.upload_file(Filename="Jad-fish-market.csv", Bucket=self.bucket_name,
                                   Key="Data26/fish/Jad.csv")

    def _load_bucket(self):
        """
        The bucket that we are using is added to a class variable, bucket_contents.
        :return:
        """
        self.bucket_contents = self.s3_client.list_objects_v2(Bucket=self.bucket_name)

    def _create_dataframe(self, file_prefix: str, file_suffix: str):
        """
        Creates a dataframe including all the specified files given by the prefix and suffix.
        All files must have the same columns.
        :param file_prefix: What the files should start with.
        :param file_suffix: What the files should end with.
        :return:
        """
        files = []
        data = []
        columns = []
        for each in self.bucket_contents["Contents"]:
            if each["Key"].startswith(file_prefix) and each["Key"].endswith(file_suffix):
                files.append(each["Key"])
        for file in files:
            s3_object = self.s3_client.get_object(Bucket=self.bucket_name, Key=file)
            arr = pd.read_csv(s3_object["Body"])
            if len(columns) == 0:
                for col in arr.columns:
                    columns.append(col)
            data.append(arr.to_numpy())
        data = [item for sublist in data for item in sublist]
        data = np.array(data)
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

if __name__ == "__main__":

    pd.set_option('display.max_rows', 500)
    pd.set_option('display.max_columns', 500)
    pd.set_option('display.width', 1000)

    bucket_name = "data-eng-resources"
    file_prefix = "python/fish-market"
    file_suffix = ".csv"

    Trial = Fish(bucket_name, file_prefix, file_suffix, column_name="Species")
