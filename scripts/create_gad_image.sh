#!/bin/bash

# 根据Dockfile创建镜像，gadgetron_uih是镜像名称，v1是版本号
sudo docker build -t gadgetron_uih:v1 ../

set -eux
__CURRENT__=`pwd`
__DIR__=$(cd "$(dirname "$0")";pwd)
cd ${__DIR__}

# 根据gadgetron_uih镜像启动临时容器，返回容器id
container_id=$(docker create gadgetron_uih:v1)

# delete this container
sudo docker rm -f $container_id

# clear <none> image
sudo docker save -o ./gadgetron_uih.tar gadgetron_uih:v1
sudo chmod +777 ./gadgetron_uih.tar
sudo docker rmi gadgetron_uih:v1
sudo docker load < ./gadgetron_uih.tar

# delete gadgetron_uih.tar
sudo rm ./gadgetron_uih.tar