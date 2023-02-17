import os.path as op
from setuptools import setup 
from pathlib import Path

version = None
with open(Path(rf"ugad4fun/version.py")) as f:
    version = f.read().split('=')[1].strip().strip('\'')
if version is None:
    raise RuntimeError('Could not determine version')

setup(
    name='ugad4fun',
    author='ADEPT',
    license='MIT',
    version=version,
    description='reconstruction pipelines based on gadgetron framework',
    include_package_data=True,
    packages=[
        'ugad4fun',
        'ugad4fun/utils',
        'ugad4fun/recon',
        'ugad4fun/tests',
        ],
    package_data={
        "ugad4fun": [
            op.join("recon_config", "*.xml"), # all the config files(xml)
            ],  
        },
    install_requires=[
        'numpy',
        'pynufft',
        'ismrmrd',
        'matplotlib'
        ],
    project_urls={
        'Source': 'https://github.com/medlab/ugad4fun',
        },
)