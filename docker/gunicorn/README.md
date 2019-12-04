# 微服务脚手架
## token
jwt payload格式。perms是permission，内容为权限标示。权限标示以a-z A-Z 0-9的62进制组成，最多5位

## API endpoints

对外提供的 API 接口列在这里并提供文档。

## 使用说明

API 接口的试用方法。

### 注意事项

注意事项列表。

## 部署方法

### 本地调试 connexion

docker build -t ecpro-storage -f Dockerfile .
docker run -t -i --env-file ./.env.example -v /Users/root1/Github/ecpro-storage/:/home -p 80:80 --name ecpro_storage ecpro-storage:latest
docker exec -it 7d3056b624d6 /bin/ash
docker logs -f 7d3056b624d6

### uWSGI 联调
```shell
cd app && uwsgi --http :5000 -w app.main
```

如果想在 Python 代码更改时进行 autoreload，使用

```shell
cd app && uwsgi --http :5000 -w app.main --py-autoreload=1
```

### Docker 构建镜像

```shell
docker build -t ecpro-microservice-scaffold -f Dockerfile .
```

### Docker 运行镜像

```shell
cp .env.example .env && vim .env
docker run -d --env-file .env --name ecpro-microservice-scaffold ecpro-microservice-scaffold:lastest
```

### Docker 运行 Celery

Known issues: https://github.com/celery/billiard/issues/273#issuecomment-473204170

需要安装 eventlet，并在启动 Celery 时候指定 -P eventlet

```shell
cp .env.example .env && vim .env
docker run -d --env-file .env -name ecpro-microservice-scaffold-celery ecpro-microservice-scaffold:lastest \

celery -A upload.celery_tasks worker -l info -Q $APP_NAMESPACE:CELERY:celery_package_post_process
celery -A upload.celery_tasks worker -l info -Q STORAGE:CELERY:celery_package_post_process
```

### 外部依赖

将外部依赖项列在这里，包括 Redis、MySQL、外部 API 服务等。

### 环境变量

微服务部署时，需要传入的环境变量列在这里，包括全局、本应用、外部依赖的配置等。

#### 全局配置

```shell
APP_NAMESPACE=MICROSERVICE_NAME
APP_RESOURCES_DIR=/app/resources
```

#### 应用配置

```shell
A=1
B=2
...
```

#### 外部依赖配置

```shell
REDIS_HOST=127.0.0.1
MYSQL_HOST=127.0.0.1
...
```
