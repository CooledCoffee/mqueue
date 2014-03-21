# -*- coding: utf-8 -*-
from distutils.core import setup

setup(
    name='mqueue',
    version='0.1',
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
        'test': ['fixtures'],
    },
    install_requires=[
        'decorated',
    ],
    packages=[
        'mqueue',
    ],
    url='https://github.com/CooledCoffee/mqueue/',
)
