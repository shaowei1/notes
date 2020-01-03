
docker pull redis

docker run -p 6379:6379 --name some-redis -d redis

$ docker run --name some-redis -d redis redis-server --appendonly yes

docker run -it --network some-network --rm redis redis-cli -h some-redis


```
FROM redis
COPY redis.conf /usr/local/etc/redis/redis.conf
CMD [ "redis-server", "/usr/local/etc/redis/redis.conf" ]
```


$ docker run -v /myredis/conf/redis.conf:/usr/local/etc/redis/redis.conf --name myredis redis redis-server /usr/local/etc/redis/redis.conf
