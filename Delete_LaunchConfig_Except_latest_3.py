from __future__ import print_function

import json
import datetime
import time
import boto3
import os

def lambda_handler(event, context):
    region = os.getenv("region")
    client = boto3.client('autoscaling',region)
    response = client.describe_launch_configurations()
    ls_list=[]
    for LC in response['LaunchConfigurations']:
        msg = LC['LaunchConfigurationName']
        #print(msg)
        
#Give LC name to be deleted eg: LC-test-ASG
        if(msg.startswith("LC-test-ASG")):
            (ls_list.append(LC['LaunchConfigurationName']))
    #print(np.sort(ls_list))
    ls_list.sort(reverse=True)
    print("LC list")
    print (ls_list)
    #LCcount = len(ls_list)
    #print(LCcount)
    i=0
    j=0
#deleting the LC except latest 3
    for lcn in ls_list:
        j=j+1
        if(i<=3):
            i=i+1
        if(i==4):
            client.delete_launch_configuration(LaunchConfigurationName=lcn)
            print(lcn, "is deleted")
