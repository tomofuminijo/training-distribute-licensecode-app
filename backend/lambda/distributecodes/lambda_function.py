import json
import urllib
import boto3
import botocore.exceptions
import os
import traceback
from datetime import datetime

dynamodb = boto3.resource('dynamodb')

DDB_TABLE_NAME = os.environ['DDB_TABLE_NAME']
# DDB_TABLE_NAME = 'LicenseCodesAssignment'

def lambda_handler(event, context):
    #print("Received Original event: %s" % event)

    body = json.loads(event['body']);
    print("Received Original event.body: %s" % body)
    
    email = body['email'].strip()
    
    licenseCode = ''
    course = ''

    print("Received event. email: [%s]" % (email))

    table = dynamodb.Table(DDB_TABLE_NAME)
    try:
        response = table.get_item(
            Key={
                'email': email
            }
        )
        
        print(response)
        if 'Item' not in response:
            return {
                "statusCode": 200,
                'headers': {
                    "Access-Control-Allow-Origin": "*"
                },
                "body": json.dumps({
                    'message': 'このメールアドレスは登録されていません。メールアドレスを確認してください。'
                })
            }

        licenseCode = response['Item']['licenseCode']
        course = response['Item']['course']

    except botocore.exceptions.ClientError as e:
        raise

    #
    # Update License Code has distributed
    #
    try: 
        response = table.update_item(
                Key={
                    'email': email
                },
                UpdateExpression='SET updatetime = :val1, distributed = :val2',
                ExpressionAttributeValues={
                    ':val1': datetime.now().strftime('%Y%m%d%H%M%S'),
                    ':val2': 'true'
                }
            )
    except botocore.exceptions.ClientError as e:
        raise


    return {
        "statusCode": 200,
        'headers': {
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps({
            'licenseCode': licenseCode,
            'course': course
        })
    }