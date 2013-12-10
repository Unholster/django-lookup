# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name= "unholster.django-lookup",
    version= "0.1.0",
    author = u"Unholster",
    author_email = "sebastian@unholster.com",
    maintainer = u"Andrés Villavicencio",
    maintainer_email = "andres@unholster.com",
    packages = find_packages(),
    license = "MIT License",
    package_data={
        'lookup' : [
            '*.*',
        ]
    },
    url="https://github.com/Unholster/django-lookup",
    install_requires =['Unidecode',],
    description="Easy SlugField management",
    long_description=read("README.md"),
    classifiers=["Development Status :: 5 - Production/Stable", "Topic :: Utilities"]
)
