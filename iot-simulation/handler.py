import os
from random import randint
import json
import boto3
import urllib.request
from urllib.parse import unquote

bucket = os.environ['BUCKET_NAME']

# Tạo một session với AWS
session = boto3.Session(
    aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'], 
    aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'], 
    aws_session_token=os.environ['AWS_SESSION_TOKEN'],
    region_name=os.environ['AWS_REGION'])
# Khởi tạo một client của AWS S3
s3 = session.client('s3')

bucket_name = bucket + '-' + os.environ['AWS_REGION']

def upload(event, context):
  list_objects_res = s3.list_objects_v2(Bucket=bucket_name, Prefix='uploads/', EncodingType='url')
  if 'Contents' not in list_objects_res:
      raise Exception('Invalid response format:', list_objects_res)
  
  file_keys = list(filter(lambda x: x['Key'][-1] != '/', list_objects_res['Contents']))
  
  if len(file_keys) == 0:
      raise Exception('Empty bucket')
  
  random_key = unquote(file_keys[randint(0, len(file_keys) - 1)]['Key'])
  print('Selected key: ' + random_key)

  baseURL = 'https://api.disaster-us-east-1.thienlinh.link' if os.environ['AWS_REGION'] == 'us-east-1'  else'https://api.disaster-ap-southeast-1.thienlinh.link'
  
  print('Uploaded to', baseURL)
  
  get_object_response = s3.get_object(Bucket=bucket_name, Key=random_key)
  image_data = get_object_response['Body'].read()
  
  print('ContentType', get_object_response['ContentType'])
  
  upload_service_res = urllib.request.urlopen(urllib.request.Request(
        url=baseURL + '/upload',
        data=json.dumps({ 'name': random_key, 'content_type': get_object_response['ContentType'] }).encode('utf-8'),
        headers={'Accept': 'application/json'},
        method='POST'),
    timeout=5)
  
  presigned_url = upload_service_res.read().decode('utf-8')
  print('Presigned url: ' + presigned_url)
  
  
  s3_put_object_req = urllib.request.Request(
        url=presigned_url,
        data=image_data,
        method='PUT')
  
  s3_put_object_req.add_header('Content-Length', str(len(image_data)))
  s3_put_object_req.add_header('Accept', '*/*')
  s3_put_object_req.add_header('Connection', 'keep-alive')
  s3_put_object_req.add_header('Content-Type', get_object_response['ContentType'])
  
  s3_put_object_res = urllib.request.urlopen(s3_put_object_req,
    timeout=60)

  return {
    'statusCode': 200,
    'body': s3_put_object_res
  }