# docker for mac
preference --> Daemon --> registry mirrors + https://v11ikicsy.mirror.aliyuncs.com
https://cr.console.aliyun.com/undefined/instances/mirrors

# paw
```
sudo spcl --master-disable
xclient.info
```
# pip
```
pip config list -v

[global]
index-url = https://pypi.tuna.tsinghua.edu.cn/simple

pip -i ...
```

# mysql-client
```
brew install mysql-client
echo 'export PATH="/usr/local/opt/mysql-client/bin:$PATH"' >> ~/.bash_profile
like /usr/local/opt/mysql-client/bin/mysqldump.

-- 导出表结构
mysqldump -udev -ppasswd -h host  --no-data --databases merchant storage > table-struct.sql

-- 导出表
mysqldump -uroot -proot --databases db1 --tables a1 a2  >/tmp/db1.sql

-- where
mysqldump -uroot -proot --databases db1 --tables a1 --where='id=1'  >/tmp/a1.sql
```

# redis

brew install redis
brew ls redis

brew services start redis

redis-server /usr/local/etc/redis.conf

redis-cli

```
exists kombu_demo
llen kombu_demo
lindex kombu_demo 0

keys *
 type _kombu.binding.kombu_demo

SMEMBERS _kombu.binding.kombu_demo << return all members of set
```


# rabbitmq
brew update
brew install rabbitmq

The RabbitMQ server scripts and CLI tools are installed in sbin directory under /usr/local/Cellar/rabbitmq, which is accessible via /usr/local/opt/rabbitmq/sbin. In case that directory is not in PATH it's recommend to append it:

export PATH=$PATH:/usr/local/opt/rabbitmq/sbin


rabbitmq-server
brew services start rabbitmq
browser watch 127.0.01:15672

docker run -d -p 5672:5672 -p 15672:15672 --name rabbitmq rabbitmq:management

# telnet
 brew install telnet

 telnet 127.0.0.1 6907
