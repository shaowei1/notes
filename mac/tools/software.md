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
