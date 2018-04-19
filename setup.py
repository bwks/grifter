import os
from setuptools import setup


def read(file_name):
    with open(os.path.join(os.path.dirname(__file__), file_name), 'r') as f:
        return f.read()

setup(
    name='vagrant-topology-builder',
    version='0.1',
    author='Brad Searle',
    author_email='bradleysearle@gmail.com',
    packages=['hammer',
              'tests'],
    license='GNU GENERAL PUBLIC LICENSE Version 3',
    long_description=read('README.txt'),
    install_requires=[
        'jinja2',
        'pyyaml',
    ],
)
