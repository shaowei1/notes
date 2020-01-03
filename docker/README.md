# Build
## COPY and ADD
docker client 会把所有文件发送给 docker daemon

COPY 和 ADD 命令具有相同的特点：只复制目录中的内容而不包含目录自身

## WORKDIR
WORKDIR 命令为后续的 RUN、CMD、COPY、ADD 等命令配置工作目录


## Copy multistage
```
COPY --from=builder /app/dist /usr/share/nginx/html
```
其中的 COPY 命令通过指定 --from=0 参数，把前一阶段构建的产物拷贝到了当前的镜像中
```
FROM golang:1.7.3
WORKDIR /go/src/github.com/sparkdevo/href-counter/
RUN go get -d -v golang.org/x/net/html
COPY app.go    .
RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o app .

FROM alpine:latest
RUN apk --no-cache add ca-certificates
WORKDIR /root/
COPY --from=0 /go/src/github.com/sparkdevo/href-counter/app .
CMD ["./app"]
```

## ADD
解压压缩文件并把它们添加到镜像中
从 url 拷贝文件到镜像中

```
WORKDIR /app
ADD nickdir.tar.gz .

or

ADD http://example.com/big.tar.xz /usr/src/things/
RUN tar -xJf /usr/src/things/big.tar.xz -C /usr/src/things
RUN make -C /usr/src/things all

or

RUN mkdir -p /usr/src/things \
    && curl -SL http://example.com/big.tar.xz \
    | tar -xJC /usr/src/things \
    && make -C /usr/src/things all
```

## 加快Dockerfile构建
```
其中 myhc.py 文件不经常变化，而 checkmongo.py、checkmysql.py 和 checkredis.py 这三个文件则经常变化，那么我们可这样来设计 Dockerfile 文件：

WORKDIR /app
COPY myhc.py .
COPY check* ./
```
/app 和 myhc.py 都会使用缓存， 只有check* 才会build
当文件 size 比较大且文件的数量又比较多，尤其是需要执行安装等操作时使用

##
```
exec "$@"
```
It basically takes all the extra command line arguments and execs them as a command. The intention is basically "Do everything in this .sh script, then in the same shell run the command the user passes in on the command line".
exec 是 bash 的内置命令

shell 的内件命令exec执行命令时，不启用新的shell进程。

source 和 . 不启用新的shell，在当前shell中执行，设定的局部变量在执行完命令后仍然有效。

bash 或 sh 或 shell script 执行时，另起一个子shell，其继承父shell的环境变量，其子shelll的变量执行完后不影响父shell。

exec是用被执行的命令行替换掉当前的shell进程，且exec命令后的其他命令将不再执行。
