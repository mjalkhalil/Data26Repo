import pandas as pd

from assignment import *
import boto3

bucket_name = "data-eng-resources"
file_prefix = "python/fish-market"
file_suffix = ".csv"
s3_client = boto3.client("s3")

TestObject = Fish(bucket_name, file_prefix, file_suffix, column_name="Species")

def test_load_bucket():
    bucket_contents_a = s3_client.list_objects_v2(Bucket=bucket_name)["Contents"]
    bucket_contents_b = TestObject.bucket_contents["Contents"]
    for a, b in zip(bucket_contents_a, bucket_contents_b):
        assert a["Key"] == b["Key"]

def test_create_dataframe():
    assert TestObject.df is not None
    assert isinstance(TestObject.df, pd.DataFrame)

def test_to_csv():
    s3_object = s3_client.get_object(Bucket=bucket_name, Key="Data26/fish/Jad.csv")
    df = pd.read_csv(s3_object["Body"])
    df = df.groupby("Species").mean()
    assert len(TestObject.averages) == 7
    assert len(df) == 7
