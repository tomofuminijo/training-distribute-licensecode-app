import json
import boto3
import csv
import urllib
import os


s3 = boto3.resource('s3')
dynamodb = boto3.resource('dynamodb')

DDB_TABLE_NAME = os.environ['DDB_TABLE_NAME']
# DDB_TABLE_NAME = 'LicenseCodesAssignment'
table = dynamodb.Table(DDB_TABLE_NAME)


def lambda_handler(event, context):
    bucket = event['Records'][0]["s3"]["bucket"]["name"]
    key = event['Records'][0]["s3"]["object"]["key"]
    key = urllib.parse.unquote_plus(key);

    print("Received event. Bucket: [%s], Key: [%s]" % (bucket, key))
    
    file_path = f'/tmp/{key}'
    
    print("file path:[%s]" % (file_path))
    
    bucket = s3.Bucket(bucket).download_file(key, file_path)

    with open(file_path) as f:
        reader = csv.reader(f)
        for row in reader:
            course = row[0]
            licenseCode = row[1]
            email = row[2]
            putLicenseCodesToDynamoDB(email, licenseCode, course)
            

    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

def putLicenseCodesToDynamoDB(email, licenseCode, course):
    print('PutItem to DDB: email: %s, licenseCode: %s' % (email, licenseCode))
    response = table.put_item(
        Item={
            'email': email,
            'licenseCode': licenseCode,
            'course': course
        }
    )
