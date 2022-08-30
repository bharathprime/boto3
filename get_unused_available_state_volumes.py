import json
import boto3

def lambda_handler(event, context):
    ec2 = boto3.resource('ec2', region_name='ap-south-1')
    #to get all volumes
    # volumes = ec2.volumes.all()
    #to get available state volume
    volumes = ec2.volumes.filter(Filters=[{'Name': 'status', 'Values': ['available']}])
    print("list of unattached volumes")
    for v in volumes:
        print (v.id)

    
