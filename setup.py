# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='sample',
    version='0.1.0',
    description='description',
    long_description=readme,
    author='name',
    author_email='example@email.com',
    url='https://example.url.com',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
