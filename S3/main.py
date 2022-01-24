import boto3
from pprint import pprint as pp
import json
import pandas as pd

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

s3_client = boto3.client("s3")
s3_resource = boto3.resource("s3")
bucket_name = "data-eng-resources"

# bucket_list = s3_client.list_buckets()
# bucket = s3_resource.Bucket(bucket_name)

# for bucket in bucket_list["Buckets"]:
#     print(bucket["Name"])

# bucket_contents = s3_client.list_objects_v2(Bucket = bucket_name, Prefix = "python")

# for object in bucket_contents["Contents"]:
#     print(object["Key"])
#
# for content in bucket.objects.all():
#     print(content.key)


# Reading JSON from Bucket
# s3_object = s3_client.get_object(Bucket = bucket_name, Key="python/chatbot-intent.json")
# strbody = s3_object["Body"].read()
#
# pp(json.loads(strbody))

# Reading CSV file from Bucket
# s3_object = s3_client.get_object(Bucket = bucket_name, Key="Data26/Test/Jad-fish-market.csv")
# df = pd.read_csv(s3_object["Body"])
# print(df)

# Create a json file and upload it to S3
# dict_to_upload = {"name": "data", "status": 2}
#
# with open("Jad.json", "w") as jsonfile:
#     json.dump(dict_to_upload, jsonfile)
#
# s3_client.upload_file(Filename="Jad.json", Bucket=bucket_name, Key="Data26/Test/Jad.json")
