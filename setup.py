# -*- coding: utf-8 -*-
from distutils.core import setup
import setuptools

setup(
    name='mqueue',
    version='0.4.1',
    author='Mengchen LEE',
    author_email='CooledCoffee@gmail.com',
    classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Topic :: Software Development :: Libraries',
    ],
    description='Simple queue based on mysql.',
    extras_require={
        'test': ['fixtures2'],
    },
    install_requires=[
        'decorated >= 1.5.2',
        'loggingd',
    ],
    package_dir={'': 'src'},
    packages=setuptools.find_packages(where='src'),
    url='https://github.com/CooledCoffee/mqueue/',
)
