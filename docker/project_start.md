## Docker 启动项目

```shell script

docker build -t ${project_name} -f Dockerfile ${project_path}

docker run  -t -i --env-file .environment.txt -v ${project_path}/app/:/app -p 80:80 --name ${project_name} --network ${network_name} ${project_name}:latest

```
### Docker 运行 Celery

Known issues: https://github.com/celery/billiard/issues/273#issuecomment-473204170

需要安装 eventlet，并在启动 Celery 时候指定 -P eventlet
```shell script
docker run  -t -i --env-file .environment.txt -v ${project_path}/app/:/app --name ${celery_name} --network ${network_name} ${project_name}:latest celery -A engine.runserver.celery worker -l debug -Q ${queue_name1},${queue_name2}
```
