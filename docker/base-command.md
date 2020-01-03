## docker



```

# 重启Docker

docker ps
ps -aux | grep -v grep | grep docker-proxy
service docker stop
docker rm $(docker ps -aq)
rm /var/lib/docker/network/files/local-kv.db
service docker start

# 上传镜像到tencent

docker login --username=xxx ccr.ccs.tencentyun.com

docker tag [ImageId] ccr.ccs.tencentyun.com/[namespace]/[ImageName]:[镜像版本号]

docker push ccr.ccs.tencentyun.com/[namespace]/[ImageName]:[镜像版本号]

docker tag  ccr.ccs.tencentyun.com/ecpro/ecpro-billing:latest

docker push ccr.ccs.tencentyun.com/ecpro/ecpro-billing:latest


docker info

docker version



curl 'http://localhost:9200/?pretty'

docker run -d --name elasticsearch-ik -p 9200:9200 -p 9300:9300 -e "ES_JAVA_OPTS=-Xms256m -Xmx256m" -e "discovery.type=single-node" docker.io/bachue/elasticsearch-ik:6.2.4


~/flask-env/bin/pip uninstall -y uwsgi && ~/flask-env/bin/pip install --no-cache-dir uwsgi==2.0.17.1



docker run -t -i -e QLOUND_COS_SECRET_ID=1 -e QLOUND_COS_SECRET_KEY=2 -v /Users/shaowei/project:/app --name container_name ccr.ccs.tencentyun.com/[namespace]/storage



docker run -t -i --env-file ./env.txt -v /Users/user:/app -p 6000:80 --name user ccr.ccs.tencentyun.com/[namespace]/user

# 执行过后，会保存环境变量和映射信息



# Dockerfile

# Dockerfile

docker build -t myimage -f Dockerfile .
docker run -d --name mycontainer -p 80:5000 myimage   ==> 80/tcp, 443/tcp, 0.0.0.0:80->5000/tcp



# container operate

docker container start accefbc14cb6

docker exec -it f5d01e8c44cd /bin/ash

docker container list -a

docker rm b546bfb47902

docker stop $(docker ps -aq)

docker rm $(docker ps -aq)

docker container kill id

docker ps
docker port id
docker logs -f id

docker ps -a

docker rm xxx -f



## 查看容器内部运行的进程

docker top id

## 查看docker信息

docker inspect id





# image operate

docker rmi xxx

docker image list

docker rmi $(docker images -q)



# 复制文件

docker cp mycontainer:/opt/file.txt /opt/local/

docker cp /opt/local/file.txt mycontainer:/opt/



# 清除所有资源

docker system prune

docker container prune

docker image prune

docker image prune --force --all

docker container prune -f



# 格式化container inspect

docker inspect --format='{{json .Config}}' 6de489eff53a



# 查看container_id

docker port container_id

docker_netspace --> localhost

```
