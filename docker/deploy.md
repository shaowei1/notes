#!/bin/bash
# 自动创建app包

app_name=$1
if [[ -z ${app_name} ]]
then
    error_hint="错误: 请在命令后输入目录"
    echo -e "\033[31m${error_hint}\033[0m"
    exit 2
fi

cd ${app_name}
docker build -t ${app_name} -f Dockerfile .

image_id=$(docker image ls -a | grep ${app_name} | grep latest | awk '{print $3}')

echo ${image_id}
if [[ -z ${image_id} ]]
then
    error_hint="image_id not found"
    echo -e "\033[31m${error_hint}\033[0m"
    exit 2
fi

container_id=$(docker ps -a | grep ecpro-storage | awk '{print $1}')
docker rm ${container_id}

docker run -t -i --env-file /root/${app_name}/.env.example  -p 80:80 --name ecpro-storage ${image_id}
##docker push ccr.ccs.tencentyun.com/ecpro/${app_name}:latest
