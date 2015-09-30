#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name="django-lookup",
    version="0.1.0",
    author="Sebastián Acuña",
    author_email="sebastian@unholster.com",
    maintainer="Andrés Villavicencio",
    maintainer_email="andres@unholster.com",
    packages=find_packages(),
    license="MIT License",
    package_data={
        'lookup': [
            '*.*',
        ]
    },
    url="https://github.com/Unholster/django-lookup",
    install_requires=['Unidecode'],
    description="Lookup tables for Django models with management features and fuzzy matching",  # noqa
    classifiers=["Development Status :: 5 - Production/Stable", "Topic :: Utilities"]  # noqa
)
