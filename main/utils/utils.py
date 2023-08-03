from typing import Dict
import bcrypt
import base64
from json import dumps, loads


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')


def encode_str(data: str) -> str:
    data_encode = base64.b64encode(data.encode('utf-8')).decode('utf-8')
    return data_encode

def decode_str(data: str) -> Dict:
    data_decode = base64.b64decode(data).decode('utf-8')
    return loads(data_decode)




def encode_addrees(data: dict) -> str:
    try:
        print('passou no encode addrees')
        addrees = dict()

        if data['publicPlace'] is not '':
            addrees['publicPlace'] = data['publicPlace']

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
            return addrees
        
        addrees = dumps(addrees)
        addrees = encode_str(addrees)
        print(f'print addrees2: {addrees}')
        return addrees
        
    except Exception as e:
        print(e)
        return e
    

def validate_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


def encode_contact(data: dict) -> str:
    try:
        contact = dict()
        print('passou no encode contact')

        if data['telephone'] is not '':
            contact['telephone'] = data['telephone']

        if data['cell'] is not '':
            contact['cell'] = data['cell']

        if data['email'] is not '':
            contact['email'] = data['email']

        if len(contact) == 0:
            contact = None
            return contact
        
    
        contact = dumps(contact)
        contact = encode_str(contact)
    
        return contact

    except Exception as e:
        print(e)
        return e