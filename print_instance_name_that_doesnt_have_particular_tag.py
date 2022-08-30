import json
import boto3

def lambda_handler(event, context):


    instances = [i for i in boto3.resource('ec2', region_name='eu-central-1').instances.all()]

# Print instance_id of instances that do not have a Tag of Key='Backup' or replay tag name any
    for i in instances:
        if i.tags is not None and 'Backup' not in [t['Key'] for t in i.tags]:
          # print (i.instance_name)
            for tag in i.tags:
                if tag['Key'] == 'Name':
                    print (tag['Value'])
