import requests

data = requests.post(
    'http://127.0.0.1:5000/foo',
    json={'inputVar': 'yang'},
    headers={'Origin': 'https://mc-dev.ecpro.com'}
)
print(data.content)
"""
Access-Control-Allow-Origin: http://svdXXfL0.com
Access-Control-Allow-Credentials: true
"""
# b'<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">\n<title>405 Method Not Allowed</title>\n<h1>Method Not Allowed</h1>\n<p>The method is not allowed for the requested URL.</p>\n'
