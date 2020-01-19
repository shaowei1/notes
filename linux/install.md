vim /etc/sysconfig/network-scripts/ifcfg-eth0

```
BOOTPROTO=dhcp
DEVICE=eth0
HWADDR=52:54:00:27:2d:09
NM_CONTROLLED=no
ONBOOT=yes
TYPE=Ethernet
USERCTL=no
PERSISTENT_DHCLIENT=yes
```

```
DEVICE=eth0
BOOTPROTO=dhcp
ONBOOT=yes
```

cp /etc/sysconfig/network-scripts/ifcfg-eth0 /etc/sysconfig/network-scripts/ifcfg-eth1

yum remove docker                   docker-client                   docker-client-latest                   docker-common                   docker-latest                   docker-latest-logrotate                   docker-logrotate                   docker-engine

yum install -y yum-utils   device-mapper-persistent-data   lvm2
yum-config-manager     --add-repo     https://download.docker.com/linux/centos/docker-ce.repo
yum install docker-ce docker-ce-cli containerd.io
systemctl start docker

docker pull registry.cn-beijing.aliyuncs.com/ecpro/ecpro-flask-docker:latest
sudo docker login --username=infimind极睿科技 registry.cn-beijing.aliyuncs.com
docker pull registry.cn-beijing.aliyuncs.com/ecpro/ecpro-flask-docker:latest


ssh-keygen

systemctl start nginx
yum install nginx

docker run -t -i --env-file environment_variables.txt   -p 800:80 --name old_merchant 101a5ac55eb8
docker pull registry.cn-hangzhou.aliyuncs.com/acs-sample/mysql:5.7
docker tag registry.cn-hangzhou.aliyuncs.com/acs-sample/mysql:5.7 mysql:5.7
   35  docker create -it mysql:5.7
   36  docker run --name mtmysql -e MYSQL_ROOT_PASSWORD=xinyue -d -i -p 3306:3306 mysql:5.7
   37  docker exec -it mtmysql mysql -uroot -pxinyue
   mysql -uroot -p -h 127.0.0.1
   docker build -t ecpro-storage -f Dockerfile .

nmap 47.91.147.52

  Starting Nmap 7.80 ( https://nmap.org ) at 2019-12-09 21:46 CST
  Nmap scan report for 47.91.147.52
  Host is up (0.046s latency).
  Not shown: 992 filtered ports
  PORT      STATE  SERVICE
  22/tcp    open   ssh
  25/tcp    open   smtp
  80/tcp    closed http
  110/tcp   open   pop3
  143/tcp   open   imap
  3389/tcp  closed ms-wbt-server
  9050/tcp  closed tor-socks
  12345/tcp closed netbus

  Nmap done: 1 IP address (1 host up) scanned in 18.18 seconds


  yum install git

  yum install python-setuptools && easy_install pip
pip install git+https://github.com/shadowsocks/shadowsocks.git@master

# https://github.com/shadowsocks/shadowsocks/blob/master/README.md

ssserver -p 443 -k password -m aes-256-cfb
sudo ssserver -d stop
sudo less /var/log/shadowsocks.log
or
ssserver -c /etc/shadowsocks.json

ssserver -p 8001 -k shaowei -m aes-256-cfb

git commit -a -m 'linux install docker network nginx initial'