import json
import boto3   

def lambda_handler(event, context):
    # TODO implement
    client = boto3.client('ec2')
    addresses_dict = client.describe_addresses()
    totno = 0
    allvol = ""
    for eip_dict in addresses_dict['Addresses']:
        #print(eip_dict['PublicIp'])
        if "InstanceId" not in eip_dict:
            #print (eip_dict['PublicIp'] + " doesn't have any instances associated")
            allvol += " \n "
            allvol += eip_dict['PublicIp'] + " doesn't have any instances associated"
            totno += 1
            #print(allvol)
            
    tn=str(totno)
    html = """They are $(num) EIP doesn't have attached with any instances
    $(vol)
    """
    html = html.replace("$(num)", tn)
    html = html.replace("$(vol)", allvol)
    message = {"Anker-account": "EIP"}
    client = boto3.client('sns')
    response = client.publish(
        #update the target arn of sns
        TargetArn='arn:aws:sns:ap-south-1:123456789:test_tagging',
        Message=json.dumps({'default': json.dumps(html)}),
        MessageStructure='json'
    )

 
    
