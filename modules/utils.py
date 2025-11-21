import os
import json
from dotenv import load_dotenv
from datetime import datetime
from botocore.exceptions import ClientError
import boto3

load_dotenv()

# R2 Configuration (using S3-compatible Boto3 structure)
R2_ENDPOINT_URL = os.getenv("R2_ENDPOINT_URL")
R2_ACCESS_KEY_ID = os.getenv("R2_ACCESS_KEY_ID")
R2_SECRET_ACCESS_KEY = os.getenv("R2_SECRET_ACCESS_KEY")
R2_BUCKET_NAME = os.getenv("R2_BUCKET_NAME")

GALLERY_METADATA_KEY = "gallery_data.json" # Central file for all metadata

def get_s3_client():
    """Returns a configured Boto3 S3 client for R2."""
    if not all([R2_ENDPOINT_URL, R2_ACCESS_KEY_ID, R2_SECRET_ACCESS_KEY]):
        print("❌ R2 credentials not fully configured.")
        return None
    
    return boto3.client(
        's3',
        endpoint_url=R2_ENDPOINT_URL,
        aws_access_key_id=R2_ACCESS_KEY_ID,
        aws_secret_access_key=R2_SECRET_ACCESS_KEY,
        region_name='auto' # Required for Cloudflare R2
    )

def generate_unique_filename(base_name="news_art", extension=".png"):
    """
    Generates a unique file key (path) for R2 storage using date and timestamp.
    
    Returns:
        str: The unique R2 key (e.g., news_art_YYYYMMDD_HHMMSS.png).
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{base_name}_{timestamp}{extension}"

def save_gallery_metadata(new_entry):
    """
    Fetches the existing gallery metadata JSON from R2, adds the new entry, 
    and saves the updated list back to R2.
    """
    s3_client = get_s3_client()
    if not s3_client:
        print("❌ Cannot save metadata: R2 client not initialized.")
        return False
    
    gallery_data = []
    
    try:
        # 1. Fetch existing data
        response = s3_client.get_object(Bucket=R2_BUCKET_NAME, Key=GALLERY_METADATA_KEY)
        content = response['Body'].read().decode('utf-8')
        gallery_data = json.loads(content)
        print(f"Loaded {len(gallery_data)} existing entries from R2.")
    except ClientError as e:
        # 2. Handle file not found (first run)
        if e.response['Error']['Code'] == 'NoSuchKey':
            print("Metadata file not found on R2. Creating a new one.")
        else:
            print(f"❌ Error fetching metadata from R2: {e}")
            return False
    except Exception as e:
        print(f"❌ General error reading R2 metadata: {e}")
        return False

    # 3. Add the new entry (at the beginning for easier display)
    gallery_data.insert(0, new_entry)
    
    # 4. Save updated data back to R2
    updated_content = json.dumps(gallery_data, indent=2, ensure_ascii=False).encode('utf-8')
    try:
        s3_client.put_object(
            Bucket=R2_BUCKET_NAME, 
            Key=GALLERY_METADATA_KEY, 
            Body=updated_content, 
            ContentType='application/json'
        )
        print(f"✅ Metadata saved to R2 key: {GALLERY_METADATA_KEY}")
        return True
    except Exception as e:
        print(f"❌ Error saving metadata to R2: {e}")
        return False

def load_gallery_metadata():
    """Fetches and returns the gallery metadata list from R2."""
    s3_client = get_s3_client()
    if not s3_client:
        return []

    try:
        response = s3_client.get_object(Bucket=R2_BUCKET_NAME, Key=GALLERY_METADATA_KEY)
        content = response['Body'].read().decode('utf-8')
        return json.loads(content)
    except ClientError as e:
        if e.response['Error']['Code'] == 'NoSuchKey':
            return []
        print(f"❌ Error loading metadata from R2: {e}")
        return []
    except Exception as e:
        print(f"❌ General error loading R2 metadata: {e}")
        return []