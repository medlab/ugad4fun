import os
import os.path as op
from pathlib import Path
from setuptools import setup 
from setuptools.command.install import install

version = None
with open(Path(rf"ugad4fun/version.py")) as f:
    version = f.read().split('=')[1].strip().strip('\'')
if version is None:
    raise RuntimeError('Could not determine version')

class LinkCommand(install):
    
    def run(self):
        install.run(self)
        os.system('sh scripts/install_config.sh')


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
    install_requires=[
        'numpy',
        'pynufft',
        'ismrmrd',
        'matplotlib'
        ],
    project_urls={
        'Source': 'https://github.com/medlab/ugad4fun',
        },
    cmdclass={
        'install': LinkCommand,
        }
)