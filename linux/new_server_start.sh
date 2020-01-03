yum install -y htop

yum remove docker                   docker-client                   docker-client-latest                   docker-common                   docker-latest                   docker-latest-logrotate                   docker-logrotate                   docker-engine
yum install -y yum-utils   device-mapper-persistent-data   lvm2
yum-config-manager     --add-repo     https://download.docker.com/linux/centos/docker-ce.repo
yum install -y docker-ce docker-ce-cli containerd.io
yum install -y git

# jupyter notebook
# yum install -y python3
# python3 -m pip install --upgrade pip
# python3 -m pip install jupyter
# jupyter notebook --generate-config
# cat /root/.jupyter/jupyter_notebook_config.json
# jupyter notebook --port 8888 --no-browser --ip 0.0.0.0 --allow-root
docker pull jupyter/base-notebook
# docker Dockerfile-jupyter1
# https://jupyter-docker-stacks.readthedocs.io/en/latest/index.html



systemctl start docker

docker pull registry.cn-beijing.aliyuncs.com/ecpro/ecpro-flask-docker:latest

docker network create some-network

docker pull mysql:8.0
docker run -p 3306:3306 --name mtmysql --network some-network -e MYSQL_ROOT_PASSWORD=xinyue -d -i mysql:8.0 --default-authentication-plugin=mysql_native_password

docker pull redis
docker run -p 6379:6379 --name some-redis --network some-network -d redis

source .bashrc

ssh-keygen
git clone git@git.xx.com:ecpro/ecpro-merchant.git
git clone git@git.xx.com:ecpro/ecpro-storage.git

yum install -y mysql
mysql -uroot -p -h 127.0.0.1

CREATE DATABASE merchant;
CREATE DATABASE storage;
# DROP DATABASE nba; // 删除一个名为nba的数据库

exit;

# docker network connect some-network some-redis
# docker network connect some-network mtmysql

docker build -t ecpro-merchant -f /root/ecpro-merchant/Dockerfile-debug /root/ecpro-merchant
docker build -t ecpro-storage -f /root/ecpro-storage/Dockerfile-debug /root/ecpro-storage

docker run  -t -i --env-file /root/ecpro-merchant/.env.example -v /root/ecpro-merchant/app/:/app -p 8000:80 --name ecpro-merchant --network some-network ecpro-merchant:latest
docker run  -t -i --env-file /root/ecpro-storage/.env.example -v /root/ecpro-storage/app/:/app -p 80:80 --name ecpro-storage --network some-network ecpro-storage:latest

docker run  -t -i --env-file ecpro-merchant/.env.example -v /root/ecpro-merchant/app/:/app  --name publish-celery --network some-network ecpro-merchant:latest celery -A engine.runserver.celery worker -l debug -Q queue_name0,queue_name1

docker network inspect some-network

docker rm ecpro-merchant -f
apt-get install -y net-tools

apt-cache search mysql-server
