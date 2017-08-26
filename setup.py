# coding: utf-8
from __future__ import unicode_literals

from setuptools import (
    setup,
    find_packages,
)


setup(
    name='natasha',
    version='0.7.0',
    description='Named-entity recognition for russian language',
    url='https://github.com/bureaucratic-labs/natasha',
    author='Dmitry Veselov',
    author_email='d.a.veselov@yandex.ru',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Text Processing :: Linguistic',
    ],
    keywords='natural language processing, russian morphology, named entity recognition, tomita',
    packages=find_packages(),
    install_requires=[
        'yargy'
    ],
)
