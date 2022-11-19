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

# 1. open gadgetron in dev container
#  # build&install gadgetron, https://gadgetron.readthedocs.io/en/latest/building.html#building-in-conda-environment
#  # tips: for release you should change CMAKE_BUILD_TYPE to Release
#  cmake -GNinja -DCMAKE_BUILD_TYPE=Debug -DUSE_MKL=ON -DCMAKE_INSTALL_PREFIX=${CONDA_PREFIX} ../
#  # tips, change 13 to your cpu core number+1
#  cmake --build . -- -j13
#  cmake --build . --target install
# 2. cd gadgetron-4-fun/gadgetron-python-demo
# 3. link gadgetron config file and python module from gadgetron-4-fun

ln -s $PWD/passthough_demo.xml $CONDA_PREFIX/share/gadgetron/config/passthough_demo.xml
ln -s $PWD/passthough_demo.py $CONDA_PREFIX/share/gadgetron/python/passthough_demo.py 

# 4. generate test data
ismrmrd_generate_cartesian_shepp_logan
# 5. [first terminal] start a gadgetron instance
#   tips: you can run on different port like: gadgetron -p 10002
gadgetron 
# 6. [second terminal] run test data with you config and python module 
#   tips: you can run on different port like: gadgetron_ismrmrd_client -f testdata.h5  -p 10002 -c passthough_demo.xml
gadgetron_ismrmrd_client -f testdata.h5 -c passthough_demo.xml

```

### 本机开发(同样依托Conda)

(在本机环境尝试没有成功, 原因不详)

参照 https://gadgetron.readthedocs.io/en/latest/building.html#setting-up-a-development-environment

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
