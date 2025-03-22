import boto3
from io import BytesIO
from PIL import Image
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get Redis URL from .env
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")

s3_client = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION
)

def upload_to_s3(image_bytes, filename):
    s3_client.upload_fileobj(
        BytesIO(image_bytes),
        S3_BUCKET_NAME,
        filename,
        ExtraArgs={"ContentType": "image/jpeg"}
    )
    return f"https://{S3_BUCKET_NAME}.s3.amazonaws.com/{filename}"
