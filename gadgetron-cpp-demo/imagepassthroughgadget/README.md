
# Purpose

Test out of gadgetron gadget development

# Quick Start

## build it
```bash
# active conda gadgetron environment

mkdir build
cd build
cmake .. -DUSE_MKL=ON -DCMAKE_INSTALL_PREFIX=${CONDA_PREFIX}
cmake --build . --target install

```

## run gadgetron (in conda)
```bash
gadgetron 
```bash
## generator raw data (in coda)
ismrmrd_generate_cartesian_shepp_logan
```
## test it

```bash
# for default
gadgetron_ismrmrd_client -f testdata.h5
# for imagepassthrough
gadgetron_ismrmrd_client -f testdata.h5 -c default_with_image_passthrough.xml
```
## validate it

```bash
HDFView # old but seems works
# or
ismrmrdviewer # which not work here
```
# More information

the config /config/default_with_image_passthrough.xml is just default.xml with imagepassthrough gadget insert  before image finish gadget

# Debug in vscode

Tips: we assume you work under $HOME/work dir

# Refs:

1. https://gadgetron.readthedocs.io/en/latest/gadget.html
2. default.xml https://github.com/gadgetron/gadgetron/blob/4262faea142fac7eac236080ec61ef4a4ce10081/gadgets/mri_core/config/default.xml
3. https://code.visualstudio.com/docs/cpp/launch-json-reference
4. https://code.visualstudio.com/docs/editor/variables-reference#_environment-variables
