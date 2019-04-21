from setuptools import setup, find_packages
from pathlib import Path

with Path('README.md').open() as fh:
    long_description = fh.read()

setup(
    name='crowdread',
    version='0.0.1',
    author='Guillem Borrell',
    description='A package to crowdsource crop reads',
    long_description=long_description,
    packages=find_packages(),
    install_requires=['starlette', 'uvicorn', 'pynng', 'click',
                      'pyarrow', 'pandas', 'ujson', 'trio'],
    entry_points={
        'console_scripts': [
            'crowdread_api = crowdread.api:main',
            'crowdread_worker = crowdread.worker:main'
            ]
        }
    )
