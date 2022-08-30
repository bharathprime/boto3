import json
import boto3
import datetime
#from requests_toolbelt import MultipartEncoder
#import requests


def lambda_handler(event, context):
    
    regions = []
    client = boto3.client("ec2")
    response = client.describe_regions()

    for item in response["Regions"]:
        regions.append(item["RegionName"])
        
    date = datetime.date.today()
    today = date.today()
    year = today.year
    month = today.month
    day = today.day
    
    t = str(today)
    y = str(year)
    m = str(month)
    d = str(day)
    
    for rn in regions:
    
        client = boto3.client('resourcegroupstaggingapi',rn)
        res=client.get_resources()
        #encoded_string = res.encode("utf-8")
        fields = json.dumps(res)
        #m = MultipartEncoder(fields=fields)
        bucket_name = "test-list-all-res"
        file_name = rn + "aws_resources_consumed.json"
        s3_path = "aws_resources_consumed/" + y + "/" +  m + "/" +  d + "/" +  file_name
        s3 = boto3.resource("s3")
        s3.Bucket(bucket_name).put_object(Key=s3_path, Body=fields)
    
