# install

```shell
   33  docker pull registry.cn-hangzhou.aliyuncs.com/acs-sample/mysql:5.7
   34  docker tag registry.cn-hangzhou.aliyuncs.com/acs-sample/mysql:5.7 mysql:5.7
   35  docker create -it mysql:5.7
   36  docker run --name mtmysql -e MYSQL_ROOT_PASSWORD=xinyue -d -i -p 3306:3306 mysql:5.7
   37  docker exec -it mtmysql mysql -uroot -pxinyue
   38  docker ps
   41  yum install mysql
   42  mysql -uroot -p -h 127.0.0.1
```

```shell
docker pull mysql:8.0
docker run -p 3306:3306 --name mtmysql -e MYSQL_ROOT_PASSWORD=xinyue -d -i mysql:8.0 --default-authentication-plugin=mysql_native_password
# 如果不设置 authentication 将会产生ERROR 2059 (HY000): Authentication plugin 'caching_sha2_password' cannot be loaded: /usr/lib64/mysql/plugin/caching_sha2_password.so: cannot open shared object file: No such file or directory

```



# query all foreign keys

```

select * from INFORMATION_SCHEMA.KEY_COLUMN_USAGE where table_schema = 'merchant'



```

sqlacodegen mysql+pymysql://root:xinyue@192.168.15.179/merchant > model.py
