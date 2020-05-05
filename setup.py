
from setuptools import setup, find_packages


with open('README.md') as file:
    description = file.read()


with open('requirements/main.txt') as file:
    requirements = [_.strip() for _ in file]


setup(
    name='natasha',
    version='1.1.0',

    description='Named-entity recognition for russian language',
    long_description=description,
    long_description_content_type='text/markdown',

    url='https://github.com/natasha/natasha',
    author='Natasha contributors',
    author_email='d.a.veselov@yandex.ru, alex@alexkuk.ru',
    license='MIT',

    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Text Processing :: Linguistic',
    ],
    keywords='natural language processing, russian',

    packages=find_packages(),
    package_data={
        'natasha': [
            'data/dict/*.txt',
            'data/emb/*.tar',
            'data/model/*.tar',
        ]
    },
    install_requires=requirements
)
