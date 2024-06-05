
from apscheduler.schedulers.background import BackgroundScheduler
from flask import jsonify
import requests
import time
import os
from dotenv import load_dotenv
from datetime import datetime
from pytz import timezone
import boto3
from urllib.parse import urlparse
from botocore.exceptions import NoCredentialsError
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256

load_dotenv()


def process_s3_url(s3_url,user_private_key):
  

    try:
        # Parse the bucket name and object key from the provided URL
        parsed_url = urlparse(s3_url)
        bucket_name = parsed_url.netloc.split('.')[0]
        object_key = parsed_url.path.lstrip('/')

        # Sign the URL with the user's private key
      #  private_key = RSA.import_key(user_private_key)
      #  h = SHA256.new(s3_url.encode('utf-8'))
       # signature = pkcs1_15.new(private_key).sign(h)

        is_valid = True  # Replace with your condition based on your application logic
    
        # Return tuple with boolean and hash
       # return is_valid,signature.hex()

        signature = "dummy_signature"
        return is_valid, signature

    except NoCredentialsError:
        return {'error': 'Credentials not available'}, 403
    except Exception as e:
        return {'error': str(e)}, 500

def process_url(s3_url):

    
    user_private_key = os.getenv('USER_PRIVATE_KEY')


    is_valid, signature = process_s3_url(s3_url, user_private_key)

    if is_valid:
        
        main_server = os.getenv('MAIN_SERVER')
        url = f"{main_server}/confirm"
        headers = {"Content-Type": "application/json"}
        payload = {'is_valid': is_valid}
        try:
        # Make POST request to Flask endpoint
            response = requests.post(url, json=payload, headers=headers)

        # Check if request was successful (status code 200)
            if response.status_code == 200:
                return response.json()  # Return JSON response from Flask endpoint
            else:
                return {'error': f'Request failed with status code {response.status_code}'}

        except requests.exceptions.RequestException as e:
            return {'error': f'Request failed: {str(e)}'}

    else:
        return jsonify({'error': 'Signature process failed'}), 500





def call_external_api():
    wallet = os.getenv('WALLET')
    main_server = os.getenv('MAIN_SERVER')
    api_url = f"{main_server}/task/{wallet}"
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.get(api_url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            s3_url = data.get('s3_url')
            data = response.json()
            s3_url = data.get('s3_url')  # Extract S3 URL from API response

            if not s3_url:
                print("S3 URL not found in API response.")
                return
            
            # Call process_url_endpoint function with retrieved S3 URL
            result = process_url(s3_url)
            print(f"Result from process_url_endpoint: {result}")

        else:
            print(f"Failed to fetch data from API. Status code: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"Request to API failed: {str(e)}")

if __name__ == '__main__':
    # Configure the scheduler with a timezone (using pytz)
    print("hi")
    scheduler = BackgroundScheduler(timezone='UTC')
    # Add a job that calls the external API every minute
    scheduler.add_job(call_external_api, 'interval', minutes=0.5)
    print('Scheduler started. Press Ctrl+C to exit.')
  
    scheduler.start()
  
    # Keep the script running
    try:
        while True:
            pass
    except (KeyboardInterrupt, SystemExit):
        print("Exiting...")