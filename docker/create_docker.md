# 构建Docker镜像

- 通过 Dockerfile 自动构建镜像；

```bash
docker build -t image-name -f Dockerfile .
docker images
```

1. 尽量精简，不安装多余的软件包。
2. 尽量选择 Docker 官方提供镜像作为基础版本，减少镜像体积。
3. Dockerfile 开头几行的指令应当固定下来，不建议频繁更改，有效利用缓存。
4. 多条 RUN 命令使用''连接，有利于理解且方便维护。
5. 通过 -t 标记构建镜像，有利于管理新创建的镜像。
6. 不在 Dockerfile 中映射公有端口
7. Push 前先在本地运行，确保构建的镜像无误。

- 通过容器操作，并执行 Commit 打包生成镜像。

```
 docker run -i -t centos
 yum update && yum install openssh-server
 # open a new session
 docker ps
 docker commit f5f1beda4075 test:v1.0
 docker images
```
docker run -t -i --env-file ./.env.example -v /Users/path/project/app:/app -p 80:80 --name container-name image_id

# 保存镜像到压缩包
docker save -o xxx.tar ${image_id}

# 解压镜像
docker load -i xxx.tar
