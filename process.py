
from urllib.parse import urlparse
from dotenv import load_dotenv
from eth_account import Account
from eth_account.messages import defunct_hash_message



load_dotenv()

def sign_s3_url(task_id,s3_url,user_private_key,wallet):
    try:
        msghash = defunct_hash_message(text="\x19Ethereum Signed Message:\n32" + s3_url)
        signedMesaage=Account.signHash(msghash,user_private_key)
        msghash=signedMesaage['messageHash'].hex()
        signature=signedMesaage['signature'].hex()
        v = signedMesaage['v']
        r = signedMesaage['r']
        s = signedMesaage['s']
        print(signedMesaage)
        print(hex(v))
        print(hex(r))
        print(hex(s))
        is_valid = True 
        params = {
        'is_valid':True,
        'taskId':task_id,
        'operatorId':wallet,
        'messageHash':msghash,
        'signature':signature,
        'v':v,
        'r':r,
        's':s
    }
        return is_valid, params
    except Exception as e:
        return {'error': str(e)}, 500