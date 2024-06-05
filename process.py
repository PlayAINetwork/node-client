from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
import boto3
from urllib.parse import urlparse
from botocore.exceptions import NoCredentialsError
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
import requests

# Load environment variables from .env file
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

app = Flask(__name__)

@app.route('/process-url', methods=['POST'])
def process_url():

    data = request.get_json()

    # Check if 's3_url' is present in the JSON data
    if 's3_url' not in data:
        return jsonify({'error': 'Missing s3_url in JSON data'}), 400

    s3_url = data['s3_url']
   
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

if __name__ == '__main__':
   port = int(os.getenv('PORT', 5000))
   app.run(host='0.0.0.0', port=port)