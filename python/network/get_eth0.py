pip install netifaces
>>> import netifaces as ni
>>> ni.ifaddresses('eth0')
{17: [{'addr': '02:42:ac:13:00:02', 'broadcast': 'ff:ff:ff:ff:ff:ff'}], 2: [{'addr': '172.19.0.2', 'netmask': '255.255.0.0', 'broadcast': '172.19.255.255'}]}
>>> ip = ni.ifaddresses('eth0')[ni.AF_INET][0]['addr']
>>> ip
'172.19.0.2'
