import json
import boto3
from datetime import datetime

def lambda_handler(event, context):
    # TODO implement
    def image_sort(elem):
        return elem.get('CreationDate')
# give image name that has to be delete        
    ec2 = boto3.client('ec2','us-east-1')
    response = ec2.describe_images(Filters=[
            {
                'Name': 'tag:Name',
                'Values': ['ami-name-' + '*']
            }
    ])
    images = response
#sorting filtered images as creation date 
    print("------------------")
    response1 = {image['CreationDate']: image['ImageId'] for image in sorted(images['Images'], key=lambda image: datetime.strptime(image['CreationDate'], '%Y-%m-%dT%H:%M:%S.%f%z'))}
    print(response1)
    print("------------------")
    #print(response)
# creating a associative array
    my_list = []
    for image in sorted(images['Images'], key=lambda image: datetime.strptime(image['CreationDate'], '%Y-%m-%dT%H:%M:%S.%f%z')):
        #print(image['CreationDate'], image['ImageId'])
        name = [tag['Value'] for tag in image['Tags'] if tag['Key'] == 'Name'][0]
        #print(name)
        my_list.append( {'ami_id': image['ImageId'], 'ami_date': image['CreationDate'], 'ami_name' : name} )

#this for loop will execute the array in descending  
#deleting the the image other than latest 3 ami
    z = 0
    for ami2 in reversed(my_list):
        z= z+1
        #print(z)
        print(ami2['ami_id'],ami2['ami_date'],ami2['ami_name'])
        if(z>=4):
            ec2.deregister_image(ImageId=ami2['ami_id'])
            print(ami2['ami_id'],ami2['ami_name'],"is deleted")
