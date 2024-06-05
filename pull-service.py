
from apscheduler.schedulers.blocking import BlockingScheduler
import requests
import time
import os
from dotenv import load_dotenv
from datetime import datetime
from pytz import timezone

load_dotenv()


def call_process_url_endpoint(s3_url):
    url = 'http://localhost:5000/process-url'  # Adjust URL if Flask app runs on a different port or host

    # Create JSON payload with 's3_url' key
    payload = {'s3_url': s3_url}

    headers = {'Content-Type': 'application/json'}

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
            result = call_process_url_endpoint(s3_url)
            print(f"Result from process_url_endpoint: {result}")

        else:
            print(f"Failed to fetch data from API. Status code: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"Request to API failed: {str(e)}")

if __name__ == '__main__':
    # Configure the scheduler with a timezone (using pytz)
    scheduler = BlockingScheduler(timezone=timezone('UTC'))
    # Add a job that calls the external API every minute
    scheduler.add_job(call_external_api, 'interval', minutes=0.5)
    print('Scheduler started. Press Ctrl+C to exit.')
    try:
        scheduler.start()
    except KeyboardInterrupt:
        print('Scheduler stopped manually.')