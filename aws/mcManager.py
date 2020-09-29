#Description: Lambda manages EC2 instance, provides response message to discord users
#Trigger: AWS cloudwatch events via eventbridge, or direct calls via discord bot
#Output: 
#Last update: Seth Alexander. ?/?/2020

import os 
import boto3
from botocore.exceptions import ClientError

instanceId = os.environ['INSTANCE_ID']
ec2 = boto3.resource('ec2')
instance = ec2.Instance(instanceId)


def lambda_handler(event, context):
    op = event["op"]
    
    success = False
    body = {}
    message = "" 
    
    print(f"Operation: {op}")
    if op == "start":
        success, message = startInstance()
        return buildResponse(success, message, body)
    elif op == "stop":
        success, message = stopInstance()
        return buildResponse(success, message, body)
    elif op == "ip":
        success, message = getPublicIp()
        return buildResponse(True, message, {"public_ipv4": message})
    elif op == "getState":
        state = instance.state['Name']
        return buildResponse(True, f"state: {state}", {"state": state})
    
    return buildResponse(success, message, body)


def startInstance():
    success = False
    message = ""
    
    try:
        response = instance.start()
        state = response['StartingInstances'][0]['CurrentState']['Name']
        if state == 'pending':
            success = True
            message = "Server is starting up."
        elif state == 'running':
            success = True
            message = "Server is running"
        else:
            message = f"Failed to start server. Unexpected server state: {state}"
            
    except ClientError as e:
        print(e)
        message = f"Failed to start instance. Error: {e['Error']['Code']}"
    
    return success, message
    
    
def stopInstance():
    success = False
    message = ""
    
    try:
        response = instance.stop()
        state = response['StoppingInstances'][0]['CurrentState']['Name']
        message = f"Server is {state}"
        success = True
    except ClientError as e:
        print(e)
        message = f"Failed to start instance. Error: {e['Error']['Code']}"
    
    return success, message
    

def buildResponse(success, message, body):
    return {
        "body": body,
        "success": success,
        "message": message
    }
    
    
def getPublicIp():
    ip = instance.public_ip_address
    if ip != None:
        return True, ip
    else:
        return False, "Failed to retrieve Ip"
        