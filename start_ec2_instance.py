import boto3
#specify the region and instance id
region = 'us-east-1'
instances = ['i-01e41db4c2af6d6b5']
ec2 = boto3.client('ec2', region_name=region)

def lambda_handler(event, context):
    ec2.start_instances(InstanceIds=instances)
    print('stopped your instances: ' + str(instances))
