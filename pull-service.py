
from apscheduler.schedulers.background import BackgroundScheduler
from flask import jsonify
import requests
import time
import os
import logging
from dotenv import load_dotenv
from datetime import datetime
from pytz import timezone
from process import sign_s3_url
from eth_account import Account
from eth_account.messages import defunct_hash_message
import platform,socket,json,psutil,logging,re,uuid



load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),  # Log to a file
        logging.StreamHandler()          # Log to the console
    ]
)
class ExcludeJobLogFilter(logging.Filter):
    def filter(self, record):
        msg = record.getMessage()
        return not ("Added job" in msg or "Job " in msg or "Running job" in msg)


# Apply the filter to all handlers
for handler in logging.root.handlers:
    handler.addFilter(ExcludeJobLogFilter())

def process_url(task_id):
    user_private_key = os.getenv('USER_PRIVATE_KEY')
    main_server = os.getenv('MAIN_SERVER')
    wallet = os.getenv('WALLET')
    api_url = f"{main_server}/taskInfo/{task_id}"
    headers = {"Content-Type": "application/json"}
    # Call taskInfo_endpoint function with retrieved taskId to get the s3 url
    try:
        logging.info("Getting additional task info")
        response = requests.get(api_url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            s3_url = data.get('s3_url')
            if not s3_url:
                logging.error("s3_url not found in API response.")
                return {'error':'s3_url not found in API response.'}
        else:
            logging.error(f"Failed to fetch data from API. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Request to API failed: {str(e)}")
    
    #passing the s3 url for signing to sign_s3_url
    is_valid, params = sign_s3_url(task_id,s3_url,user_private_key,wallet)

    # if the process was completed, calling the /confrim endpoint in the main function to confrim the task
    if is_valid:
        logging.info("Sending verified task to backend")
        url = f"{main_server}/confirm"
        headers = {"Content-Type": "application/json"}
        try:
            # Make POST request to /confrim endpoint
            response = requests.post(url, json=params, headers=headers)
            # Check if request was successful (status code 200)
            if response.status_code == 200:
                return response.json()  
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
    #calling the task endpoint and getting taskId 
    try:
        logging.info("Calling the backend for active tasks")
        response = requests.get(api_url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            task_id = data.get('task_id')
            if not task_id:
                logging.info("No task assigned at the moment")
                return
            # Taskid passed to process_url() fucntion
            result = process_url(task_id)
            logging.info(f"Result of the task: {result}")
        else:
            logging.error(f"Failed to fetch data from API. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Request to API failed: {str(e)}")




def getSystemInfo():
    try:
        info={}
        info['platform']=platform.system()
        info['platform-release']=platform.release()
        info['platform-version']=platform.version()
        info['architecture']=platform.machine()
        info['hostname']=socket.gethostname()
        info['ip-address']=socket.gethostbyname(socket.gethostname())
        info['mac-address']=':'.join(re.findall('..', '%012x' % uuid.getnode()))
        info['processor']=platform.processor()
        info['ram']=str(round(psutil.virtual_memory().total / (1024.0 **3)))+" GB"
        info['physical_cores'] = psutil.cpu_count(logical=False)
        info['logical_cores'] = psutil.cpu_count(logical=True)
        info['cpu_usage'] = psutil.cpu_percent(interval=1)
        return info
    except Exception as e:
        logging.exception(e)


def register_node():
    user_private_key = os.getenv('USER_PRIVATE_KEY')
    main_server = os.getenv('MAIN_SERVER')
    api_url = f"{main_server}/register"
    headers = {"Content-Type": "application/json"}
    token_id = os.getenv('NFT_TOKEN_ID')
    ip= os.getenv('IP')
    port = os.getenv('PORT')
    msghash = defunct_hash_message(text="\x19Ethereum Signed Message:\n32" + token_id)
    signedMesaage=Account.signHash(msghash,user_private_key)
    msghash=signedMesaage['messageHash'].hex()
    signature=signedMesaage['signature'].hex()
    v = signedMesaage['v']
    r = signedMesaage['r']
    s = signedMesaage['s']
    params = {
        'keyId':token_id,
        'messageHash':msghash,
        'v':hex(v),
        'r':hex(r),
        's':hex(s),
        'ip':ip,
        'port':port
    }
    info=getSystemInfo()
    #logging.info(info)
    try:
            # Make POST request to /confrim endpoint
            response = requests.post(api_url, json=params, headers=headers)
            # Check if request was successful (status code 200)
            if response.status_code == 200:
                 data = response.json()
                 id = data.get('id')
                 logging.info('Node regsitration successful')
                 logging.info(f"Your unique id is : {id}")
                 return True
            else:
                logging.info('Node registration unsuccesful')
                return False
    except requests.exceptions.RequestException as e:
            return {'error': f'Request failed: {str(e)}'}



if __name__ == '__main__':
    # Configure the scheduler with a timezone
    if register_node():
        logging.info(" ")
    else:
        exit()
    scheduler = BackgroundScheduler(timezone='UTC')
    # Add a job that calls the external API every minute to get the task
    scheduler.add_job(call_external_api, 'interval', minutes=0.5)
   # logging.info('Scheduler started. Press Ctrl+C to exit.')
    scheduler.start()
    # Keep the script running
    try:
        while True:
            pass
    except (KeyboardInterrupt, SystemExit):
        logging.info("Exiting...")