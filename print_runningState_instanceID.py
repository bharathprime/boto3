import json
import boto3 

def lambda_handler(event,context):
    regions= ['ap-south-1','us-east-2']
    for region_name in regions:
        print('region_name: {region_name}')
        ec2= boto3.resource('ec2', region_name=region_name)
        if instance['State']['Name'] == 'running':
                    print(instance["InstanceId"])
