from setuptools import setup 
from pathlib import Path

version = None
with open(Path(rf"gad4fun\version.py")) as f:
    version = f.read().split('=')[1].strip().strip('\'')
if version is None:
    raise RuntimeError('Could not determine version')

setup(
    name='gad4fun',
    author='ADEPT',
    license='MIT',
    version=version,
    description='reconstruction pipelines based on gadgetron',
    include_package_data=True,
    packages=[
        'gad4fun',
        'gad4fun/utils',
        'gad4fun/recon',
        ],
    package_data={
        "gad4fun/recon_config": ["*.xml"] ,  # all the config files(xml)
        },
    install_requires=[
        'numpy',
        'pynufft',
        'ismrmrd',
        'matplotlib'
        ],
    project_urls={
        'Source': 'https://github.com/medlab/gadgetron-4-fun/',
        },
)