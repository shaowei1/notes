# Namespace

docker run -it busybox /bin/sh

ps

- /bin/sh 被施展了“障眼法”，他以为自己是就是第一个进程
- PID Namespace, Mount, UTS, IPC, Network, User
    Mount Namespace让被隔离进程只看到当前Namespace的挂载信息
    Network Namespace 让被隔离进程只看到当前Namespace的网络设备和配置
    容器是一种特殊的进程, 只能看到当前Namespace所限制的资源、文件、设备、状态或配置
- clone 是线程操作，linux 的线程是用进程实现的
- docker是单进程的，当里面可以执行netstat 进程，不过是野孩子，单进程的意思是只有一个进程是可控的

# 限制与隔离
## 很多资源和对象不能被Namespace 隔离，比如时间
settimeofday(2) # 修改了时间，跟个Guest os的时间都变了
Seccomp可以对容器内部发起的所有系统调用进行过滤和甄别来进行安全加固，拖累性能。

## Linux Cgroups( Linux Control Group): 限制一个进程能够使用的资源上限，cpu, memory, hard, network spand
- Cgroup 还能够对进程设置优先级、审计、以及将进程挂起和恢复等操作
- 提供文件接口 /sys/fs/cgroups
```
mount -t cgroup
# blkio: 为块设备设定I/O限制，一般用于磁盘等设备
# cpuset: 为进程分配单独的CPU核和对应的内存节点
# memory: 为进程设定使用限制
ls /sys/fs/cgroup/cpu
# 进程在cfs_perisod的一段时间内，只能被分配总量为cfs_quota的cpu时间
cd /sys/fs/cgroup/cpu && mkdir container
while : ; do : ; done &
top # /prop/stats获取数据, 容器不知道被cgroup限制了,lxcfs可以不挂载该目录,
cat /sys/fs/cgroup/cpu/container/cpu.cfs_quota_us
cat /sys/fs/cgroup/cpu/container/cpu.cfs_period_us
echo 226 > /sys/fs/cgroup/cpu/container/task
top # //var/lib/lxcfs/proc/memoinfo -FUSE-> /prop/meminfo  , kubernetes- ds run lxcfs
# vanilla kubernetes, ipvs repalce iptables, RPC replace rest, rancher, openshift
docker run -it --cpu-period=100000 --cpu-quota=20000 ubuntu /bin/bash
cat /sys/fs/cgroup/cpu/container_id/cpu.cfs_quota_us
cat /sys/fs/cgroup/cpu/container_id/cpu.cfs_period_us
# 只能占据20% 的cpu带宽
```

## 由于容器的本身就是一个进程,用户的应用进程实际上就是容器里PID=1的进程,也就是其他后续创建的所有进程的父进程=>在一个容器里,没办法运行两个不同的应用,除非你能找到一个公共的PID=1的程序来充当两个不同应用的父进程,systemd或supervisord代替应用本身作为容器的启动进程

## 容器本身的设计希望容器和应用能共同生命周期,否则外活内死不利于编排
