from __future__ import print_function

import json
import datetime
import time
import boto3
import os


print('Loading function')


def lambda_handler(event, context):
    print("Received event: " + json.dumps(event, indent=2))

    start_date = str(datetime.datetime.now().strftime("%Y%m%d-%H%M"))
    region = os.getenv("region")
    client = boto3.client('ec2',region)
    
    ec2 = boto3.resource('ec2')
    ins_id = ""
    instance_iterator = ec2.instances.filter(Filters=[{'Name': 'tag-key', 'Values': ['Name']}])
    for instance in instance_iterator:
        for tag in instance.tags:
            if tag['Key'] == 'Name':
    #give below the instance name to take ami
                if tag['Value'] == 'ansible-l':
                    ins_id = instance.id
                    break
    #print(ins_id)

    instanceid = ins_id
    
    name= "AMI "+instanceid+" "+start_date
    description= "AMI for "+instanceid+" created by lambda at "+start_date
    image = client.create_image(Description=description,DryRun=False, InstanceId=instanceid, Name=name, NoReboot=True)
    newAmiID = image['ImageId']
    
    tag = client.create_tags(
        DryRun=False,
        Resources=[
            newAmiID,
        ],
        Tags=[
            {
                'Key': 'Name',
                'Value': 'ami-name-Latest-prod-orbit-fe-asg'
            },
        ]
      )
    # get autoscaling client
    client = boto3.client('autoscaling')

    # get object for the ASG we're going to update, filter by name of target ASG
    response = client.describe_auto_scaling_groups(AutoScalingGroupNames=[event['targetASG']])

    if not response['AutoScalingGroups']:
        return 'No such ASG'

    # get name of InstanceID in current ASG that we'll use to model new Launch Configuration after
    sourceInstanceId = response.get('AutoScalingGroups')[0]['Instances'][0]['InstanceId']

    # create LC using instance from target ASG as a template, only diff is the name of the new LC and new AMI
    timeStamp = time.time()
    timeStampString = datetime.datetime.fromtimestamp(timeStamp).strftime('%Y%m%d-%H%M')
    newLaunchConfigName = 'LC-prod-fe-orbit-arzooo-ASG '+ timeStampString + ' ' + newAmiID
    client.create_launch_configuration(
        InstanceId = instanceid,
        LaunchConfigurationName=newLaunchConfigName,
        ImageId= newAmiID )
    # update ASG to use new LC
    response = client.update_auto_scaling_group(AutoScalingGroupName = event['targetASG'],LaunchConfigurationName = newLaunchConfigName)
    
    print( event['targetASG'], newLaunchConfigName, newAmiID)
    client = boto3.client('autoscaling',region)
    response = client.describe_launch_configurations()
    ls_list=[]
    for LC in response['LaunchConfigurations']:
        msg = LC['LaunchConfigurationName']
        #print(msg)
        
        #replace the below string of startswith value
        if(msg.startswith("LC-prod-fe-orbit-arzooo-ASG")):
            (ls_list.append(LC['LaunchConfigurationName']))
    #print(np.sort(ls_list))
    ls_list.sort(reverse=True)
    print("LC list")
    print (ls_list)
    #LCcount = len(ls_list)
    #print(LCcount)
    i=0
    j=0
    for lcn in ls_list:
        j=j+1
        if(i<=3):
            i=i+1
        if(i==4):
            client.delete_launch_configuration(LaunchConfigurationName=lcn)
            print(lcn, "is deleted")
    
