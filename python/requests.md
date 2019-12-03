# request post multi/form-data with file
```python
import requests, json
path = '/Users/root1/Github/ecpro-storage/snippets/oss-notes/girl.jpg'
oss_host = 'https://ecpro-uploads.oss-cn-beijing.aliyuncs.com'

data = {
    "success_action_status": 200,
    "name": "shaowei.jpg",
    "Filename": "shaowei",
    "key": "key",
    "policy": "policy",
    "OSSAccessKeyId": "OSSAccessKeyId",
    "signature": "Signature",
    "callback": "callback",
    "x:customize": "x:customize",
    # "file": 'file': ('custom_file_name.zip', open('myfile.zip', 'rb')),,
}
resp = requests.post(
    url=oss_host,
    data=data,
    files={'file': open(path, 'rb')}
)
json.loads(resp.content.decode())
```