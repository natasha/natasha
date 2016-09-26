from setuptools import setup, find_packages

setup(
    name='natasha',
    version='0.2.0',
    description='Named-entity recognition for russian language',
    url='https://github.com/bureaucratic-labs/natasha',
    author='Dmitry Veselov',
    author_email='d.a.veselov@yandex.ru',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='natural language processing, russian morphology, named entity recognition, tomita',
    packages=find_packages(),
    install_requires=[
        'yargy==0.3.0'
    ],
    extras_require={
        'web': [
            'ujson',
            'aiohttp',
        ],
    },
)
