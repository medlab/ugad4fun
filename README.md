# test by hand about gadgetron

# 环境
## 研发环境
### VS Code DevContainer（本质上是在Docker中开发）(首选)

先在VS Code中安装 Remote Development 远程开发扩展包

### Python 模块开发

1. 可以在Gadgetron项目中建立一个工作目录，如work，在里面直接本clone本项目
2. 把相关Python/xml链接到对应配置目录
3. 在VS Code中玩起来

### 流程示意

```bash
# 1. git clone gadgetron 
# 2. cd gadgetron
# 3. mkdir work
# 4. cd work
# 5. clone this project

# 1. open gadgetron in dev container -k
#  # build&install gadgetron, https://gadgetron.readthedocs.io/en/latest/building.html#building-in-conda-environment
#  # tips: for release you should change CMAKE_BUILD_TYPE to Release
#  mkdir build
#  cd build
#  cmake -GNinja -DCMAKE_BUILD_TYPE=Debug -DUSE_MKL=ON -DCMAKE_INSTALL_PREFIX=${CONDA_PREFIX} ../
#  # tips, change 13 to your cpu core number+1
#  cmake --build . -- -j13
#  cmake --build . --target install
# 2. cd gadgetron-4-fun/gadgetron-python-demo
# 3. link gadgetron config file and python module from gadgetron-4-fun

ln -s $PWD/passthough_demo.xml $CONDA_PREFIX/share/gadgetron/config/passthough_demo.xml
ln -s $PWD/passthough_demo.py $CONDA_PREFIX/share/gadgetron/python/passthough_demo.py 

# 4. generate test data
ismrmrd_generate_cartesian_shepp_logan -k
# 5. [first terminal] start a gadgetron instance
#   tips: you can run on different port like: gadgetron -p 10002
gadgetron 
# 6. [second terminal] run test data with you config and python module 
#   tips: you can run on different port like: gadgetron_ismrmrd_client -f testdata.h5  -p 10002 -c passthough_demo.xml
gadgetron_ismrmrd_client -f testdata.h5 -c passthough_demo.xml

# 7. view it
# #pip3 install git+https://github.com/ismrmrd/ismrmrdviewer.git
# #or use HDFView
# ismrmrdviewer does not work for me, and the gadgetron_ismrmrd_client seems ignore line data back to it
# BTW, ismrmrdviewer must run on you host conda!
ismrmrdviewer

```

### 本机开发(同样依托Conda)

(在本机环境尝试没有成功, 原因不详)

参照 https://gadgetron.readthedocs.io/en/latest/building.html#setting-up-a-development-environment

## 运行&测试环境(使用简单)

该环境是将Gadgetron的运行环境封装到Docker容器，需要在Linux系统安装Git和Docker，适合直接运行或者测试人员使用，安装方便，使用简单。

### 流程示意

```bash
# 1. git clone gadgetron-4-fun
$ sudo git clone -b gadgetron_config_and_python https://github.com/Nothing10086/gadgetron-4-fun.git
Cloning into 'gadgetron-4-fun'...
remote: Enumerating objects: 202, done.
remote: Counting objects: 100% (202/202), done.
remote: Compressing objects: 100% (106/106), done.
remote: Total 202 (delta 118), reused 167 (delta 92), pack-reused 0
Receiving objects: 100% (202/202), 16.19 MiB | 2.30 MiB/s, done.
Resolving deltas: 100% (118/118), done.

# 2. cd gadgetron-4-fun
$ cd gadgetron-4-fun
$ ls
create_gad_image.sh  gadgetron           gadgetron_data         LICENSE    start_gad_container.sh
Dockerfile           gadgetron-cpp-demo  gadgetron-python-demo  README.md

# 3. create gadgetron docker image by script(第一次运行完该脚本后docker镜像已经创建成功，后面无需运行该脚本)
$ bash create_gad_image.sh
Sending build context to Docker daemon  34.55MB
Step 1/10 : FROM gadgetron/ubuntu_2004 AS gadgetron_image
latest: Pulling from gadgetron/ubuntu_2004
d51af753c3d3: Pull complete
fc878cd0a91c: Pull complete
6154df8ff988: Pull complete
fee5db0ff82f: Pull complete
50ecbc15495d: Pull complete
f72068aa33d5: Pull complete
d891b9e4e42a: Pull complete
76dabc572afa: Pull complete
968a5f645d3f: Pull complete
fa78b2c0e924: Pull complete
67dd671a117e: Pull complete
98f2a9f62653: Pull complete
592f13ac527a: Pull complete
27ef2abb7825: Pull complete
c12dcbd47181: Pull complete
a2935b66b646: Pull complete
87aaecacfae5: Pull complete
6b8bce02d55f: Pull complete
8284b18bf40f: Pull complete
beb9f97b245a: Pull complete
75b65971c706: Pull complete
Digest: sha256:3f4609712b9153d25657368d9fb0dab5aade64aeccb10f38a2da1d20a48b7f13
Status: Downloaded newer image for gadgetron/ubuntu_2004:latest
 ---> 70de548be6a5
Step 2/10 : LABEL org.opencontainers.image.authors="Xiannan.Cao"
 ---> Running in 01ba7d175615
Removing intermediate container 01ba7d175615
 ---> 80f550fc285b
Step 3/10 : EXPOSE 8002
 ---> Running in 34511d5ada0a
Removing intermediate container 34511d5ada0a
 ---> bd35df3744e2
Step 4/10 : EXPOSE 9001
 ---> Running in 2bdfd1150ef8
Removing intermediate container 2bdfd1150ef8
 ---> 82a8b1273818
Step 5/10 : EXPOSE 9002
 ---> Running in 8247f8752dbb
Removing intermediate container 8247f8752dbb
 ---> a3f84d20df42
Step 6/10 : EXPOSE 9080
 ---> Running in 0d3278a79f17
Removing intermediate container 0d3278a79f17
 ---> 9969e7b96015
Step 7/10 : COPY ./gadgetron_data/config/*.xml /usr/local/share/gadgetron/config/
 ---> e7efac7fb2f5
Step 8/10 : COPY ./gadgetron_data/python/*.py /usr/local/share/gadgetron/python/
 ---> 8f40a2913fef
Step 9/10 : COPY ./gadgetron_data/pynufft-2022.2.3-py3-none-any.whl /tmp/gadgetron_data/
 ---> da909ebad498
Step 10/10 : RUN cd /tmp/gadgetron_data && pip install pynufft-2022.2.3-py3-none-any.whl
 ---> Running in 7cd054923776
Processing ./pynufft-2022.2.3-py3-none-any.whl
Requirement already satisfied: scipy in /usr/local/lib/python3.8/dist-packages (from pynufft==2022.2.3) (1.5.4)
Requirement already satisfied: numpy in /usr/local/lib/python3.8/dist-packages (from pynufft==2022.2.3) (1.19.4)
Installing collected packages: pynufft
Successfully installed pynufft-2022.2.3
WARNING: You are using pip version 20.2.4; however, version 23.0 is available.
You should consider upgrading via the '/usr/bin/python3 -m pip install --upgrade pip' command.
Removing intermediate container 7cd054923776
 ---> ed3d1f5b9c38
Successfully built ed3d1f5b9c38
Successfully tagged gadgetron_new:v1
++ pwd
+ __CURRENT__=/gadgetron-4-fun
+++ dirname create_gad_image.sh
++ cd .
++ pwd
+ __DIR__=/gadgetron-4-fun
+ cd /gadgetron-4-fun
++ docker create gadgetron_new:v1
+ container_id=d4693a2db886fba1d69ec9c7d14dd62eb593b72d9ceb5b14a403b6c810080f02
+ sudo docker cp d4693a2db886fba1d69ec9c7d14dd62eb593b72d9ceb5b14a403b6c810080f02:/usr/local/share/gadgetron/config ./gadgetron/
+ sudo docker cp d4693a2db886fba1d69ec9c7d14dd62eb593b72d9ceb5b14a403b6c810080f02:/usr/local/share/gadgetron/python ./gadgetron/
+ sudo docker rm -f d4693a2db886fba1d69ec9c7d14dd62eb593b72d9ceb5b14a403b6c810080f02
d4693a2db886fba1d69ec9c7d14dd62eb593b72d9ceb5b14a403b6c810080f02
+ sudo docker save -o ./gadgetron_new.tar gadgetron_new:v1
+ sudo chmod +777 ./gadgetron_new.tar
+ sudo docker rmi gadgetron_new:v1
Untagged: gadgetron_new:v1
Deleted: sha256:ed3d1f5b9c383c725be9997d5e11f20b861ccd8fb077638b87e59388967c0e22
Deleted: sha256:caeecdc2aa12c86ab2513cbfcf89d5aac419a4931c92565ba4f87d6c2a3fcb00
Deleted: sha256:da909ebad498e8824a828eb9d0bdcb01982871829190db3bf8cb51df687a1da7
Deleted: sha256:e4e5d22b9c920e382526f6f1fd7218a5918863944d20c1edce6c82b464da93da
Deleted: sha256:8f40a2913fefb5a66a1da009e0d3df9fadd379fe5f7fa30ebbaeaef3533ba44a
Deleted: sha256:d5a4f39ba099dbed96c5a44bff467b3b2642f1f20f533d65b76f60b0d287dbe6
Deleted: sha256:e7efac7fb2f5d5c0cfc4ad97b5c2cb2ba4e041d445ad391a81a76cdb2f4c620b
Deleted: sha256:844b82bbddc3042dad9dcc000c23f9a125e75963808e87dad4717b0590e75cc4
Deleted: sha256:9969e7b96015893e9822302a820b01664b5cbebccedb6f63be138e9ae33cba11
Deleted: sha256:a3f84d20df424537ee98fce1e617cf6122a38f0586ea3d7dd2182e03f5bd08d6
Deleted: sha256:82a8b1273818baed26b4ca81376251c92412cf9010c44ad7447dcb140cca2736
Deleted: sha256:bd35df3744e2bbe117bca851cde38ee00a6d8fc364f672769c6c9e64e19757c1
Deleted: sha256:80f550fc285bc864fa16e112cf07a77565be23d2344af4232cc7682b10e96289
+ sudo docker load
cd13aa1d3369: Loading layer [==================================================>]  8.192kB/8.192kB
fba9ad7c0607: Loading layer [==================================================>]   16.9kB/16.9kB
3bfac2a0413e: Loading layer [==================================================>]  16.17MB/16.17MB
fc6916c8fb62: Loading layer [==================================================>]   17.5MB/17.5MB
Loaded image: gadgetron_new:v1

# 4. start gadgetron docker(后续只需运行该脚本就能启动docker容器，无需运行create_gad_image.sh)
$ bash start_gad_container.sh
02-01 03:14:11.245 INFO [main.cpp:50] Gadgetron 4.1.1 [123d9cfc8254fac6a5bb92d3eed68e6767001e42]
02-01 03:14:11.246 INFO [main.cpp:51] Running on port 9002
02-01 03:14:11.247 INFO [Server.cpp:25] Gadgetron home directory: "/usr/local"
02-01 03:14:11.247 INFO [Server.cpp:26] Gadgetron working directory: "/tmp/gadgetron/"
```



## 发布环境

### Docker
基于官方包做一个新的docker镜像去安装
### Conda
直接打包然后原地解开使用

# refs:
1. https://gadgetron2020.sciencesconf.org/
2. https://gadgetron.readthedocs.io/
3. https://github.com/medlab/gadgetron-python-demo
4. https://github.com/gadgetron/GadgetronOnlineClass
5. https://github.com/chidiugonna/learn-gadgetron
6. https://github.com/ismrmrd/ismrmrdviewer
