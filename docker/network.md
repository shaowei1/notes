# docker 网络概述

要构建具有安全的一致行为的 Web 应用程序，可以使用 Docker 网络特性。根据定义，网络为容器实现了完全隔离。

## 安装 Docker 时，它会自动创建 3 个网络

```
$ docker network ls 
NETWORK ID          NAME                DRIVER 
7fca4eb8c647        bridge              bridge 
9f904ee27bf5        none                null 
cf03ee007fb4        host                host
```



运行一个容器时，可以使用 **the --net**标志指定您希望在哪个网络上运行该容器



- bridge 网络表示所有 Docker 安装中都存在的 docker0 网络。除非使用 **docker run --net=**选项另行指定，否则 Docker 守护进程默认情况下会将容器连接到此网络。在主机上使用 **ifconfig**命令，可以看到此网桥是主机的网络堆栈的一部分。

- none 网络在一个特定于容器的网络堆栈上添加了一个容器。该容器缺少网络接口。

- host 网络在主机网络堆栈上添加一个容器。您可以发现，容器中的网络配置与主机相同。



您可以创建自己的用户定义网络来更好地隔离容器。Docker 提供了一些默认网络驱动程序来创建这些网络。您可以创建一个新 bridge 网络或覆盖一个网络。也可以创建一个网络插件或远程网络并写入您自己的规范中。
您可以创建多个网络。可以将容器添加到多个网络。容器仅能在网络内通信，不能跨网络进行通信。一个连接到两个网络的容器可与每个网络中的成员容器进行通信。当一个容器连接到多个网络时，外部连接通过第一个（按词典顺序）非内部网络提供。

## 在 Power 上创建一个覆盖 Docker 网络

```bash
[root@localhost ~]# docker network create some-network ``e2f569d57eb8506602fdfc3e8a20b12073782dcfd6046ce4ef76de8db3275d21 ` `

[root@localhost ~]# docker network inspect some-network
[
    {
        "Name": "some-network",
        "Id": "997bcfa73708a393dca63f56b1d32c176968222c0cf450604480a02bfe0f2522",
        "Created": "2020-01-03T10:45:13.013458704+08:00",
        "Scope": "local",
        "Driver": "bridge",
        "EnableIPv6": false,
        "IPAM": {
            "Driver": "default",
            "Options": {},
            "Config": [
                {
                    "Subnet": "172.19.0.0/16",
                    "Gateway": "172.19.0.1"
                }
            ]
        },
        "Internal": false,
        "Attachable": false,
        "Ingress": false,
        "ConfigFrom": {
            "Network": ""
        },
        "ConfigOnly": false,
        "Containers": {},
        "Options": {},
        "Labels": {}
    }
]
```

## add container to network

### 创建时显示指定提及

```bash
docker run -itd --name=test1 --net=test-network ppc64le/busybox /bin/sh 
docker network inspect some-network
```

### 动态将容器连接到网络

```bash
docker run -itd --name=test2 ppc64le/busybox /bin/sh
docker network connect test-network test2
```

