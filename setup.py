import os.path as op
from setuptools import setup 
from pathlib import Path

version = None
with open(Path(rf"ugadget/version.py")) as f:
    version = f.read().split('=')[1].strip().strip('\'')
if version is None:
    raise RuntimeError('Could not determine version')

setup(
    name='ugadget',
    author='ADEPT',
    license='MIT',
    version=version,
    description='reconstruction pipelines based on gadgetron framework',
    include_package_data=True,
    packages=[
        'ugadget',
        'ugadget/utils',
        'ugadget/workflow',
        'ugadget/tests',
        ],
    package_data={
        "ugadget": [
            op.join("workflow_config", "*.xml"), # all the config files(xml)
            ],  
        },
    install_requires=[
        'numpy',
        'pynufft',
        'ismrmrd',
        'matplotlib'
        ],
    project_urls={
        'Source': 'https://github.com/medlab/ugadget',
        },
)