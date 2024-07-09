
from urllib.parse import urlparse
from dotenv import load_dotenv
from eth_account import Account
from eth_account.messages import defunct_hash_message
import logging



load_dotenv()


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),  # Log to a file
        logging.StreamHandler()          # Log to the console
    ]
)


def sign_s3_url(task_id,s3_url,user_private_key,wallet):
    try:
        msghash = defunct_hash_message(text="\x19Ethereum Signed Message:\n32" + s3_url)
        signedMesaage=Account.signHash(msghash,user_private_key)
        msghash=signedMesaage['messageHash'].hex()
        signature=signedMesaage['signature'].hex()
        v = signedMesaage['v']
        r = signedMesaage['r']
        s = signedMesaage['s']
        is_valid = True 
        params = {
        'taskId':task_id,
        'operatorId':wallet,
        'messageHash':msghash,
        'signature':signature,
        'v':hex(v),
        'r':hex(r),
        's':hex(s),
        's3Url':s3_url
    }
        return is_valid, params
    except Exception as e:
        return {'error': str(e)}, 500