# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
from js_color_picker import __version__


setup(
    name='js-color-picker',
    version=__version__,
    description=open('README.rst').read(),
    author='Compound Partners Ltd',
    author_email='hello@compoundpartners.co.uk',
    packages=find_packages(),
    platforms=['OS Independent'],
    install_requires=[],
    include_package_data=True,
    zip_safe=False,
)
