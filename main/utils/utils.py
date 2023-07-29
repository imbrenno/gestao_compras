import bcrypt
import base64
from json import dumps

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')


def encode_str(data: str) -> str:
    data_encode = base64.b64encode(data.encode('utf-8')).decode('utf-8')
    return data_encode


def encode_addrees(data: dict) -> str:
    addrees = dict()
    if data['street'] is not '':
        addrees['street'] = data['street']

    if data['number'] is not '':
        addrees['number'] = data['number']

    if data['complement'] is not '':
        addrees['complement'] = data['complement']

    if data['neighborhood'] is not '':
        addrees['neighborhood'] = data['neighborhood']

    if data['city'] is not '':
        addrees['city'] = data['city']

    if data['state'] is not '':
        addrees['state'] = data['state']


    if data['zipCode'] is not '':
        addrees['zipCode'] = data['zipCode']

    if len(addrees) == 0:
        addrees = None
    
    else:
        addrees = dumps(addrees)
        addrees = encode_str(addrees)
 
    return addrees