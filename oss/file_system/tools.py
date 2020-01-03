import oss2
import hashlib
import base64
from flask import request
import logging
import base64
import urllib.parse

from M2Crypto import BIO
from M2Crypto import RSA

def verify_oss_call_back():
    """
    apt-get install build-essential python3-dev python-dev libssl-dev swig
    pip install M2Crypto==0.35.2
    """
    pub_key_url = ''
    try:
        pub_key_url_base64 = request.headers['x-oss-pub-key-url']
        pub_key_url = base64.b64decode(pub_key_url_base64).decode()
        if not pub_key_url.startswith("http://gosspublic.alicdn.com/") and not pub_key_url.startswith("https://gosspublic.alicdn.com/"):
            raise ValidationError()
        url_reader = requests.get(pub_key_url)
        # you can cache it
        pub_key = url_reader.content
        logging.info(f'pub_key: {pub_key}')
    except:
        logging.info(f'pub_key_url : {pub_key_url}')
        logging.info('Get pub key failed!')
        raise ValidationError()

    # get authorization
    authorization_base64 = request.headers['authorization']
    authorization = base64.b64decode(authorization_base64)
    logging.info(f'authorization : {authorization}')

    # get callback body
    content_length = request.headers['content-length']
    callback_body = request.data.decode()
    # compose authorization string
    auth_str = ''
    pos = request.path.find('?')
    if -1 == pos:
        auth_str = urllib.parse.unquote(request.path) + '\n' + callback_body
    else:
        auth_str = urllib.parse.unquote(request.path[0:pos]) + request.path[pos:] + '\n' + callback_body

    logging.info(f'auth_str: {auth_str}')
    # verify authorization
    auth_md5 = hashlib.md5(auth_str.encode()).digest()  # hexdigest
    bio = BIO.MemoryBuffer(pub_key)
    rsa_pub = RSA.load_pub_key_bio(bio)
    try:
        result = rsa_pub.verify(auth_md5, authorization, 'md5')
    except:
        result = False
    if not result:
        logging.info('Authorization verify failed!')

        logging.info(f'Public key : {pub_key}')
        logging.info(f'Auth string : {auth_str}')
        raise ValidationError()
    return callback_body
