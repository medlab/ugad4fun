#!/bin/bash

# 根据Dockfile创建镜像，gadgetron_new是镜像名称，v1是版本号
sudo docker build -t gadgetron_new:v1 .

set -eux
__CURRENT__=`pwd`
__DIR__=$(cd "$(dirname "$0")";pwd)
cd ${__DIR__}

# 根据gadgetron_new镜像启动临时容器，返回容器id
container_id=$(docker create gadgetron_new:v1)  

# 将容器中的Gadgetron pipeline配置xml文件和Python运行脚本文件夹拷贝到外部的gadgetron目录下，方便后序启动正式容器的目录映射
sudo docker cp $container_id:/usr/local/share/gadgetron/config ./gadgetron/
sudo docker cp $container_id:/usr/local/share/gadgetron/python ./gadgetron/

# 删除该容器
sudo docker rm -f $container_id

# 因为Dockfile创建镜像会生成很多个<none>的无用匿名镜像占用资源，下面的不是是为了清除<none>镜像
sudo docker save -o ./gadgetron_new.tar gadgetron_new:v1
sudo chmod +777 ./gadgetron_new.tar
sudo docker rmi gadgetron_new:v1
sudo docker load < ./gadgetron_new.tar 