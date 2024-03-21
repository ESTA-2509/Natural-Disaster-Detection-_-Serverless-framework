import os
import boto3
import json
import time
import uuid

bucket = os.environ['BUCKET_NAME']
region = os.environ['AWS_REGION']
table = os.environ['TABLE_NAME']

# Tạo một session với AWS
session = boto3.Session(
  aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'], 
  aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'], 
  aws_session_token=os.environ['AWS_SESSION_TOKEN'],
  region_name=region
)

# Khởi tạo một client của AWS S3
s3 = session.client('s3')
dynamodb = session.client('dynamodb')

def upload(event, context):
  bucket_name = bucket + '-' + region
  try:
    data = json.loads(event['body'])
    if not 'name' in data:
      raise Exception('required name')
  except:
    return {
      'statusCode': 400,
      'body': 'Invalid input data, must be json and have "name" attribute'
    }

  print('upload', data['name'], 'file to', region)

  response = s3.generate_presigned_url('put_object',
    Params={
      'Bucket': bucket_name,
      'Key': data['name']
    },
    ExpiresIn=3600
  )

  return {
    'statusCode': 200,
    'body': response
  }

def predict(event, context):
  print('The event:', event)
  if 's3-replication' in event['Records'][0]['userIdentity']['principalId']:
    print('ignore predict because of replication')
    return
  
  bucket_name = event['Records'][0]['s3']['bucket']['name']
  object_key = event['Records'][0]['s3']['object']['key']

  # todo ml prediction step

  timestamp = str(time.time())

  item = {
    'id': {
      'S': str(uuid.uuid1())
    },
    'bucket': {
      'S': bucket_name
    },
    'region': {
      'S': region
    },
    'object': {
      'S': object_key
    },
    'kind': {
      'S': 'Earthquake'
    },
    'created': {
      'S': timestamp
    },
    'updated': {
      'S': timestamp
    }
  }

  response = dynamodb.put_item(TableName=table, Item=item)

  print(response)

def list(event, context):
  response = dynamodb.scan(TableName=table)

  return {
    'statusCode': 200,
    'body': json.dumps(response['Items'])
  }

