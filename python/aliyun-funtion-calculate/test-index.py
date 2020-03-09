import json
from pprint import pprint

import requests


# curl -XPOST http://57e8f118477148a19d0e74360d86ebd2-cn-beijing.alicloudapi.com/test -d '{}'

def test_index():
    key = 'tmp/1/2d9cd430-43eb-4306-b7d6-1bbfe6e20605.zip'
    key = 'tmp/14e8fa0c-0f7e-11ea-a8b0-acde48001122.jpg'

    key = 'tmp/acde48001122.zip'

    zip_name = 'shaowei.zip'
    url = 'http://57e8f118477148a19d0e74360d86ebd2-cn-beijing.alicloudapi.com/test'

    resp = requests.post(
        url=url,
        json={
            "key": key,
            "upload_task_id": 1,
            "account_id": 1,
            "decompression_expire_time": 60,
            "zip_name": zip_name
        }
    )
    {
        "key": 'tmp/1/2d9cd430-43eb-4306-b7d6-1bbfe6e20605.zip',
        "upload_task_id": 1,
        "account_id": 1,
        "decompression_expire_time": 60,
        "zip_name": 'shaowei.zip'
    }
    print(resp.content)
    pprint(json.loads(resp.content.decode()))
    # return response({}, {"access_key_id": {creds.access_key_id: creds.access_key_secret}})
    {'request_callback': {},
     'result': {'access_key_id': {'STS.NTwJffTYZ2B5N18psWs2PUZPX': '8XZRawKrb9MeWW47uMVMZhTug1kjK6bFrZkdFa4yeM1Y'}}}

if __name__ == '__main__':
    test_index()
