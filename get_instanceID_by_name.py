import json
import boto3

s3 = boto3.resource('s3')

def lambda_handler(event, context):
    ec2 = boto3.resource('ec2')
    instance_iterator = ec2.instances.filter(Filters=[{'Name': 'tag-key', 'Values': ['Name']}])
    for instance in instance_iterator:
        for tag in instance.tags:
            if tag['Key'] == 'Name':
                if tag['Value'] == 'ansible-l':
                    ins_id = instance.id
                    print(ins_id)
