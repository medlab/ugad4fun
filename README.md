# Gadgetron Cases of Medical Images Reconstruction

> UGadget: A python library, providing some mri reconstruction cases, based on Gadgetron framework

## Introduction

UGadget is an application-level library, containing some cases, based on Gadgetron framework, to do reconstruction on MRI images.  

## Prerequisite
1. clone gadgetron to your workspace
```bash
git clone https://github.com/gadgetron/gadgetron.git
cd gadgetron
```
2. create a conda environment using environment.yml
```bash
# using mamba to create the gadgetron environment is faster

# use base environment to install mamba
conda activate
conda install mamba -c conda-forge

# use mamba to create environment
mamba env create -f environment.yml
```
3. start gadgetron environment, then build gadgetron
```bash
conda activate gadegtron

mkdir -p build
cd build
cmake -GNinja -DCMAKE_BUILD_TYPE=Release -DUSE_MKL=ON -DCMAKE_INSTALL_PREFIX=${CONDA_PREFIX} ../
ninja
ninja install
```
4. test gadgetron
```bash
# check gadgetron info
$ gadgetron --info
02-17 10:50:55.456 DEBUG [gadgetron_paths.cpp:117] Executable path: "/home/uih/miniconda3/envs/gadgetron/bin/gadgetron"
02-17 10:50:55.456 DEBUG [gadgetron_paths.cpp:123] Default Gadgetron home: "/home/uih/miniconda3/envs/gadgetron"
02-17 10:50:55.456 WARNING [initialization.cpp:38] Environment variable 'OMP_WAIT_POLICY' not set to 'PASSIVE'.
02-17 10:50:55.456 WARNING [initialization.cpp:39] Gadgetron may experience serious performance issues under heavy load (multiple simultaneous reconstructions, etc.)
02-17 10:50:56.418 INFO [system_info.cpp:104] CUDA DEVICE COUNT 0 and error number 35
02-17 10:50:56.418 INFO [main.cpp:86] Gadgetron Version Info
  -- Version            : 4.4.5
  -- Git SHA1           : 41dd90ee85ffe5fd3a0cc6a43422854541931be6
  -- System Memory size : 11964 MB
  -- Python Support     : YES
  -- Julia Support      : NO
  -- Matlab Support     : NO
  -- CUDA Support       : YES
  -- NVCC Flags         : -gencode arch=compute_60,code=sm_60;-gencode arch=compute_61,code=sm_61;-gencode arch=compute_70,code=sm_70;-gencode arch=compute_75,code=sm_75;-gencode arch=compute_80,code=sm_80;-gencode arch=compute_86,code=sm_86 --std=c++17
    * Number of CUDA capable devices: 0

# start a gadgetron server
$ gadgetron
02-17 10:50:31.535 DEBUG [gadgetron_paths.cpp:117] Executable path: "/home/uih/miniconda3/envs/gadgetron/bin/gadgetron"
02-17 10:50:31.535 DEBUG [gadgetron_paths.cpp:123] Default Gadgetron home: "/home/uih/miniconda3/envs/gadgetron"
02-17 10:50:31.535 WARNING [initialization.cpp:38] Environment variable 'OMP_WAIT_POLICY' not set to 'PASSIVE'.
02-17 10:50:31.535 WARNING [initialization.cpp:39] Gadgetron may experience serious performance issues under heavy load (multiple simultaneous reconstructions, etc.)
02-17 10:50:31.535 INFO [main.cpp:90] Gadgetron 4.4.5 [41dd90ee85ffe5fd3a0cc6a43422854541931be6]
02-17 10:50:31.536 DEBUG [storage.cpp:68] Found storage server: /home/uih/miniconda3/envs/gadgetron/bin/mrd-storage-server
02-17 10:50:31.536 INFO [storage.cpp:69] Starting storage server on port 9112
02-17 10:50:31.537 INFO [storage.cpp:28] Verifying connectivity to storage server...
{"level":"info","time":"2023-02-17T10:50:31.582+08:00","message":"Listening on port 9112"}
{"level":"info","requestId":"9c1d8c90-ab1f-4fd7-a963-89103fc90ef6","status":200,"method":"GET","path":"/healthcheck","query":"","latencyMs":1.56,"time":"2023-02-17T10:50:31.743+08:00","message":"request completed"}
02-17 10:50:31.743 INFO [storage.cpp:33] Received successful response from storage server.
02-17 10:50:31.743 INFO [main.cpp:99] Running on port 9002
02-17 10:50:31.743 INFO [Server.cpp:25] Gadgetron home directory: "/home/uih/miniconda3/envs/gadgetron"
02-17 10:50:31.743 INFO [Server.cpp:26] Gadgetron working directory: "/tmp/gadgetron/"
```

Generate an ismrmrd raw data and do reconstruction using gadgetron
```bash
# generate a dataset in the current working directory (./testdata.h5) with 8 coils and 10 repetitions.
$ ismrmrd_generate_cartesian_shepp_logan -r 10
Generating Cartesian Shepp Logan Phantom!!!
Acceleration: 1

$ gadgetron_ismrmrd_client -f testdata.h5
Gadgetron ISMRMRD client
  -- host            :      localhost
  -- port            :      9002
  -- hdf5 file  in   :      testdata.h5
  -- hdf5 group in   :      /dataset
  -- conf            :      default.xml
  -- loop            :      1
  -- hdf5 file out   :      out.h5
  -- hdf5 group out  :      2023-02-17 11:31:57
```
Now you could see a out.h5 file in the current directory.

## Usage

### Research and Development  

1. clone this repository to your workspace
```bash
git clone https://github.com/medlab/ugadget
cd ugadget
```
2. using pip to install this package
```bash
pip install . -U
```
1. link the config directory to gadgetron-required location
```bash
ln -s $PWD/ugadget/workflow_config $CONDA_PREFIX/share/gadgetron/config/workflow_config
```

### Deployment  

Clone the repository to your workspace, then create a Docker image using scripts provided.
```bash
git clone https://github.com/medlab/gadpipe
cd gadegtron-4-fun/shell
bash create_gad_image.sh
bash start_gad_container.sh
```

# Reference:
1. https://gadgetron2020.sciencesconf.org/
2. https://gadgetron.readthedocs.io/
3. https://github.com/gadgetron/GadgetronOnlineClass
4. https://github.com/chidiugonna/learn-gadgetron
5. https://github.com/ismrmrd/ismrmrdviewer
