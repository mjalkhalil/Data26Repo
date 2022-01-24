import pandas as pd

from assignment import *
import boto3

bucket_name = "data-eng-resources"
file_prefix = "python/fish"
s3_client = boto3.client("s3")

TestObject = Fish(bucket_name, file_prefix)

def test_load_bucket():
    assert TestObject.bucket_contents["Contents"] == s3_client.list_objects_v2(Bucket=bucket_name)["Contents"]

def test_create_dataframe():
    assert TestObject.df is not None
    assert isinstance(TestObject.df, pd.DataFrame)

def test_to_csv():
    s3_object = s3_client.get_object(Bucket=bucket_name, Key="Data26/Test/Jad-fish-market.csv")
    df = pd.read_csv(s3_object["Body"])
    df = df.groupby("Species").mean()
    assert len(TestObject.averages) == 7
    assert len(df) == 7
