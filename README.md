# test by hand about gadgetron

# 环境
## 研发环境
### VS Code DevContainer(首选)

先在VS Code中安装 Remote Development 远程开发扩展包

#### Python 模块开发

1. 可以在Gadgetron项目中建立一个工作目录，如work，在里面直接本clone本项目
2. 把相关Python/xml链接到对应配置目录
3. 在VS Code中玩起来

```bash
# 1. git clone gadgetron 
# 2. cd gadgetron
# 3. mkdir work
# 4. cd work
# 5. clone this project

# 1. open gadgetron in dev container
# 2. cd gadgetron/work/gadgetron-python-demo
# 3. link gadgetron config file from gadgetron-4-fun

ln -s $PWD/passthough_demo.xml $CONDA_PREFIX/share/gadgetron/config/
ln -s $PWD/passthough_demo.py $CONDA_PREFIX/share/gadgetron/python/

# 4. generate test data
ismrmrd_generate_cartesian_shepp_logan
# 5. [first terminal] start a gadgetron instance with custom port(I don't know why the default 9002 is used by someone?)
gadgetron -p 10002 
# 6. [second terminal] gadgetron_ismrmrd_client -f testdata.h5  -p 10002 
gadgetron_ismrmrd_client -f testdata.h5  -p 10002 -c passthough_demo.xml

```

### Conda(尝试没有成功)

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
