import boto3
import requests
import uuid
from dotenv import load_dotenv
import os

load_dotenv()
s3_url = os.getenv("S3_URL")

def image_service(url):
    s3_client = boto3.client('s3', 
    endpoint_url=s3_url,
    config=boto3.session.Config(signature_version='s3v4'))

    bucket = "lookbook"
    image_uuid = uuid.uuid4()
    response = requests.get(url)

    s3_client.put_object(Bucket=bucket, Key=str(image_uuid), Body=response.content)
    return image_uuid
        

