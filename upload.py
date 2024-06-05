import os
import boto3
from botocore.exceptions import NoCredentialsError, ClientError

def upload_file_to_s3(file_name, bucket_name, object_name=None, s3_endpoint=None):
    """
    Upload a file to a custom S3-compatible endpoint and return the URL of the uploaded file.

    :param file_name: File to upload
    :param bucket_name: Bucket to upload to
    :param object_name: S3 object name. If not specified, file_name is used
    :param s3_endpoint: Custom S3 endpoint URL
    :return: URL string of the uploaded file, or None if upload fails
    """
    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Get AWS credentials from environment variables
    aws_access_key_id = "997845e6a4f7f62ee22d399e8aebc676"
    aws_secret_access_key = "1b4c3e04dfc749f19a965d84c4e5ca4a4513bfc4a9c9740de039e534a1b0a2fc"

    if not aws_access_key_id or not aws_secret_access_key:
        print("AWS credentials not found. Set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables.")
        return None

    # Create an S3 client with custom endpoint and credentials
    s3_client = boto3.client('s3', 
                             aws_access_key_id=aws_access_key_id,
                             aws_secret_access_key=aws_secret_access_key,
                             endpoint_url=s3_endpoint)

    try:
        # Upload the file
        s3_client.upload_file(file_name, bucket_name, object_name)

        # Generate URL to get the uploaded file
        file_url = f"{s3_endpoint}/{bucket_name}/{object_name}"

        print(f"File uploaded successfully. URL: {file_url}")
        return file_url

    except FileNotFoundError:
        print(f"The file {file_name} was not found")
        return None
    except NoCredentialsError:
        print("Credentials not available")
        return None
    except ClientError as e:
        print(f"Failed to upload file {file_name}. Error: {e}")
        return None

if __name__ == "__main__":
    # Example usage
    file_to_upload = os.path.join(os.path.dirname(__file__), 'test.mp4')
    bucket_name = "playai"
    custom_s3_endpoint = "https://87e044e966512f7b11387ff032db8cf3.r2.cloudflarestorage.com"

    uploaded_file_url = upload_file_to_s3(file_to_upload, bucket_name, s3_endpoint=custom_s3_endpoint)

    if uploaded_file_url:
        print(f"Uploaded file URL: {uploaded_file_url}")
    else:
        print("File upload failed. Check logs for details.")
