
# 查询docker data file
curl http://127.0.0.1:9200/_nodes/stats/fs\?pretty

# install
docker pull bachue/elasticsearch-ik:6.2.4

# start error
elasticsearch:5.0.0 max virtual memory areas vm.max_map_count [65530] likely too low, increase to at least [262144]

From this link The vm_max_map_count kernel setting needs to be set to at least 262144 for production use. Depending on your platform:
Linux
$ grep vm.max_map_count /etc/sysctl.conf
vm.max_map_count=262144

sysctl -w vm.max_map_count=262144

# Running in Development Mode
Create user defined network (useful for connecting to other services attached to the same network (e.g. Kibana)):

$ docker network create somenetwork
Run Elasticsearch:

$ docker run -d --name elasticsearch --net somenetwork -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" elasticsearch:tag

# chrommium
RUN apk -U add chromium udev ttf-freefont
and

pyppeteer.launch(
            headless=True,
            executablePath="/usr/bin/chromium-browser",
            args=['--no-sandbox', '--disable-gpu']
        )