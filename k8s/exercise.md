# k8s

### start

```bash
git clone git@github.com:maguowei/k8s-docker-desktop-for-mac.git
git co c454799db7cb14a51f23cd7e6c05d5c437ffcbe4
$ cat images
k8s.gcr.io/kube-proxy:v1.14.6=gotok8s/kube-proxy:v1.14.6
k8s.gcr.io/kube-controller-manager:v1.14.6=gotok8s/kube-controller-manager:v1.14.6
k8s.gcr.io/kube-scheduler:v1.14.6=gotok8s/kube-scheduler:v1.14.6
k8s.gcr.io/kube-apiserver:v1.14.6=gotok8s/kube-apiserver:v1.14.6
k8s.gcr.io/coredns:1.3.1=gotok8s/coredns:1.3.1
k8s.gcr.io/pause:3.1=gotok8s/pause:3.1
k8s.gcr.io/etcd:3.3.10=gotok8s/etcd:3.3.10

./load_images.sh  # 拉取启动 Kubernetes 所需的所有镜像

```



### Init

```bash
# 查看集群
kubectl config get-contexts

# 切换 Kubernetes 集群
kubectl config use-context docker-for-desktop

# 安装 Dashboard
$ kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v1.10.1/src/deploy/recommended/kubernetes-dashboard.yaml

# 启动 dashboard
$ kubectl proxy

docker rmi $(docker images --filter "dangling=true" -q --no-trunc)
docker rm -f $(docker ps -a | grep ecpro)
docker rmi -f $(docker images | grep ecpro | awk {'print $1":"$2'})
docker rmi -f $(docker images -a | grep ecpro | awk {'print $3'})


$ curl -O https://raw.githubusercontent.com/kubernetes/dashboard/v1.10.1/src/deploy/recommended/kubernetes-dashboard.yaml

$ cat kubernetes-dashboard.yaml | grep kubernetes-dashboard
$ docker pull gcrxio/kubernetes-dashboard-amd64:v1.10.1
$ docker tag gcrxio/kubernetes-dashboard-amd64:v1.10.1 k8s.gcr.io/kubernetes-dashboard-amd64:v1.10.1

>> imagePullPolicy: IfNotPresent << 修改配置文件从本地拉取, add 在image: k8s.gcr.io/kubernetes-dashboard-amd64:v1.10.1后面

# delete pod
$ kubectl delete -f https://raw.githubusercontent.com/kubernetes/dashboard/v1.10.1/src/deploy/recommended/kubernetes-dashboard.yaml

# 重新安装dashboard
$ kubectl apply -f kubernetes-dashboard.yaml


# 获取令牌
$ kubectl -n kube-system describe secret default| awk '$1=="token:"{print $2}'

```

### command

```bash
kubectl version
kubectl config view

kubectl get all

kubectl create -f pod.yaml
kubectl get pods
kubectl get pods --all-namespaces | grep dashboard
kubectl get nodes


brew install pstree
pstree -g 2
kubectl --kubeconfig ~/.kube/config  get nodes

```

#### containters

>  ImagePullPolicy 的值默认是 Always，即每次创建 Pod 都重新拉取一次镜像。另外，当容器的镜像是类似于 nginx 或者 nginx:latest 这样的名字时，ImagePullPolicy 也会被认为 Always。
>
> Lifecycle 字段。它定义的是 Container Lifecycle Hooks。顾名思义，Container Lifecycle Hooks 的作用，是在容器状态发生变化时触发一系列“钩子”。我们来看这样一个例子：

```bash
docker inspect `container_name` | grep IPAddress

# 将容器的8000端口映射到docker主机的8001端口
iptables -t nat -A  DOCKER -p tcp --dport 8001 -j DNAT --to-destination 172.17.0.19:8000

```

### nodeport

```yaml
kind: Service
apiVersion: v1
metadata:
  name: influxdb
spec:
  type: NodePort
  ports:
    - port: 8086
      nodePort: 30000
  selector:
    name: influxdb
```



集群外就可以使用kubernetes任意一个节点的IP加上30000端口访问该服务了。kube-proxy会自动将流量以round-robin的方式转发给该service的每一个pod。

这种服务暴露方式，无法让你指定自己想要的应用常用端口，不过可以在集群上再部署一个反向代理作为流量入口。



### Ingress

Ingress controller是由Kubernetes管理的负载均衡器。

Kubernetes Ingress提供了负载平衡器的典型特性：HTTP路由，粘性会话，SSL终止，SSL直通，TCP和UDP负载平衡等

```bash
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  name: influxdb
spec:
  rules:
    - host: influxdb.kube.example.com
      http:
        paths:
          - backend:
              serviceName: influxdb
              servicePort: 8086
              
# 外部访问URL http://influxdb.kube.example.com/ping 访问该服务，入口就是80端口，然后Ingress controller直接将流量转发给后端Pod，不需再经过kube-proxy的转发，比LoadBalancer方式更高效。
```



### service

#### Loadbalancer

kubectl get svc influxdb
NAME       TYPE           CLUSTER-IP     EXTERNAL-IP   PORT(S)          AGE
influxdb   LoadBalancer   10.102.55.84   localhost     8086:31296/TCP   43s

内部可以使用ClusterIP加端口来访问服务

外部可以用以下两种方式访问该服务：

- 使用任一节点的IP加30051端口访问该服务
- 使用`EXTERNAL-IP`来访问，这是一个VIP，是云供应商提供的负载均衡器IP，如localhost:8086。

### pod

> 从外部访问pod
>
> https://jimmysong.io/blog/accessing-kubernetes-pods-from-outside-of-the-cluster/

```bash
kubectl explain pod
kubectl explain pods.spec.containers
kubectl top pod|node
kubectl get rc,svc 
kubectl create --validate -f /path/to/mongo-svc.yaml 
kubectl get po -l name=mongo-master -o wide 
kubectl delete pod --all

# settings
kubectl get pod kubia-manual -o yaml
kubectl edit pod kubia-manual
kubectl apply -f <新配置文件名.yaml>

kubectl apply -f ./run-my-nginx.yaml
kubectl get pods -l run=my-nginx -o wide
kubectl get pods -l run=my-nginx -o yaml | grep podIP

kubectl get endpoints hostnames
kubectl get svc hostnames


$ kubectl create -f nginx.yaml
$ kubectl attach -it nginx -c shell
# 在这个容器里，我们不仅可以看到它本身的 ps ax 指令，还可以看到 nginx 容器的进程，以及 Infra 容器的 /pause 进程。这就意味着，整个 Pod 里的每个容器的进程，对于所有容器来说都是可见的：它们共享了同一个 PID Namespace。
 ps ax
PID   USER     TIME  COMMAND
    1 root      0:00 /pause
    7 root      0:00 nginx: master process nginx -g daemon off;
   12 101       0:00 nginx: worker process
   13 root      0:00 sh
   18 root      0:00 ps ax

```

##### Status

pod.status.phase，就是 Pod 的当前状态，它有如下几种可能的情况：

- Pending。这个状态意味着，Pod 的 YAML 文件已经提交给了 Kubernetes，API 对象已经被创建并保存在 Etcd 当中。但是，这个 Pod 里有些容器因为某种原因而不能被顺利创建。比如，调度不成功。
- Running。这个状态下，Pod 已经调度成功，跟一个具体的节点绑定。它包含的容器都已经创建成功，并且至少有一个正在运行中。
- Succeeded。这个状态意味着，Pod 里的所有容器都正常运行完毕，并且已经退出了。这种情况在运行一次性任务时最为常见。
- Failed。这个状态下，Pod 里至少有一个容器以不正常的状态（非 0 的返回码）退出。这个状态的出现，意味着你得想办法 Debug 这个容器的应用，比如查看 Pod 的 Events 和日志。Unknown。
- 这是一个异常状态，意味着 Pod 的状态不能持续地被 kubelet 汇报给 kube-apiserver，这很有可能是主从节点（Master 和 Kubelet）间的通信出现了问题。

Pod 是 Kubernetes 里的原子调度单位。这就意味着，Kubernetes 项目的调度器，是统一按照 Pod 而非容器的资源需求进行计算的。

![](/Users/root1/Github/note/k8s/imgs/pod.png)

Infra 容器一定要占用极少的资源，所以它使用的是一个非常特殊的镜像，叫作：k8s.gcr.io/pause。这个镜像是一个用汇编语言编写的、永远处于“暂停”状态的容器，解压后的大小也只有 100~200 KB 左右。

Pod 里的容器 A 和容器 B 来说：

- 它们可以直接使用 localhost 进行通信；
- 它们看到的网络设备跟 Infra 容器看到的完全一样；
- 一个 Pod 只有一个 IP 地址，也就是这个 Pod 的 Network Namespace 对应的 IP 地址；
- 当然，其他的所有网络资源，都是一个 Pod 一份，并且被该 Pod 中的所有容器共享；
- Pod 的生命周期只跟 Infra 容器一致，而与容器 A 和 B 无关。

Kubernetes 项目只要把所有 Volume 的定义都设计在 Pod 层级即可。



### Configure access to multiple clusters

#### config-demo

```bash
apiVersion: v1
kind: Config
preferences: {}

clusters:
- cluster:
  name: development
- cluster:
  name: scratch

users:
- name: developer
- name: experimenter

contexts:
- context:
  name: dev-frontend
- context:
  name: dev-storage
- context:
  name: exp-scratch
```

#### add cluster details to your configuration file

```bash


kubectl config --kubeconfig=config-demo set-cluster development --server=https://1.2.3.4 --certificate-authority=fake-ca-file
kubectl config --kubeconfig=config-demo set-cluster scratch --server=https://5.6.7.8 --insecure-skip-tls-verify
```

#### Add user details to your configuration file:

```bash
kubectl config --kubeconfig=config-demo set-credentials developer --client-certificate=fake-cert-file --client-key=fake-key-seefile
kubectl config --kubeconfig=config-demo set-credentials experimenter --username=exp --password=some-password
```

> 
> To delete a user you can run `kubectl --kubeconfig=config-demo config unset users.`
>
> To remove a cluster, you can run `kubectl --kubeconfig=config-demo config unset clusters.`
>
> To remove a context, you can run `kubectl --kubeconfig=config-demo config unset contexts.`



#### Add context details to your configuration file:

```bash
kubectl config --kubeconfig=config-demo set-context dev-frontend --cluster=development --namespace=frontend --user=developer
kubectl config --kubeconfig=config-demo set-context dev-storage --cluster=development --namespace=storage --user=developer
kubectl config --kubeconfig=config-demo set-context exp-scratch --cluster=scratch --namespace=default --user=experimenter
```

####  see the added details

```shell
kubectl config --kubeconfig=config-demo view
```

The `fake-ca-file`, `fake-cert-file` and `fake-key-file` above is the placeholders for the real path of the certification files. You need change these to the real path of certification files in your environment.

Some times you may want to use base64 encoded data here instead of the path of the certification files, then you need add the suffix `-data` to the keys. For example, `certificate-authority-data`, `client-certificate-data`, `client-key-data`.

Each context is a triple (cluster, user, namespace). For example, the `dev-frontend` context says, “Use the credentials of the `developer` user to access the `frontend` namespace of the `development` cluster”.

#### Set the current context:

```shell
kubectl config --kubeconfig=config-demo use-context dev-frontend
kubectl config --kubeconfig=config-demo view --minify
```

## Set the KUBECONFIG environment variable

```shell
# add a new config
export KUBECONFIG=$KUBECONFIG:config-demo:config-demo-2
export KUBECONFIG=$KUBECONFIG:$HOME/.kube/config
chown $(id -u):$(id -g) $HOME/.kube/config
kubectl config view

```

## Clean up

```shell
# Return your KUBECONFIG environment variable to its original value. 
export KUBECONFIG=$KUBECONFIG_SAVED
```

### install 证书

```shell
# https://kubernetes.io/zh/docs/concepts/cluster-administration/certificates/
brew tap riboseinc/easy-rsa
brew install easy-rsa

 easyrsa init-pki
 easyrsa --batch "--req-cn=${MASTER_IP}@`date +%s`" build-ca nopass
 
 easyrsa --subject-alt-name="IP:${MASTER_IP},"\
"IP:${MASTER_CLUSTER_IP},"\
"DNS:kubernetes,"\
"DNS:kubernetes.default,"\
"DNS:kubernetes.default.svc,"\
"DNS:kubernetes.default.svc.cluster,"\
"DNS:kubernetes.default.svc.cluster.local" \
--days=10000 \
build-server-full server nopass

```

### ubuntu install kubeadm

```bash
# method 1
sudo snap install  kubeadm  --classic
sudo snap install  kube-proxy --classic
sudo snap install  kubelet  --classic

snap run kubeadm init --ignore-preflight-errors=Swap


sudo apt-get update && sudo apt-get install -y apt-transport-https curl
curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
cat <<EOF | sudo tee /etc/apt/sources.list.d/kubernetes.list
deb https://apt.kubernetes.io/ kubernetes-xenial main
EOF
sudo apt-get update
sudo apt-get install -y kubelet kubeadm kubectl
sudo apt-mark hold kubelet kubeadm kubectl
```

### Working docker environment

```bash
git clone https://github.com/kubernetes/kubernetes
cd kubernetes
make quick-release
```

