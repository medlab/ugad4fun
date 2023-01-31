#!/bin/bash
sudo docker build -t gadgetron_new:v1 .

set -eux
__CURRENT__=`pwd`
__DIR__=$(cd "$(dirname "$0")";pwd)
cd ${__DIR__}
 
# nginx:alpine  是镜像名称

# returns container ID
container_id=$(docker create gadgetron_new:v1)  
sudo docker cp $container_id:/usr/local/share/gadgetron/config ./gadgetron/
sudo docker cp $container_id:/usr/local/share/gadgetron/python ./gadgetron/
 
sudo docker rm -f $container_id

sudo docker save -o ./gadgetron_new.tar gadgetron_new:v1
sudo chmod +777 ./gadgetron_new.tar
sudo docker rmi gadgetron_new:v1
sudo docker load < ./gadgetron_new.tar 