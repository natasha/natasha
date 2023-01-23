
from setuptools import setup, find_packages


with open('README.md') as file:
    description = file.read()


setup(
    name='natasha',
    version='1.5.0',

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

    packages=find_packages(
        exclude=['tests']
    ),
    package_data={
        'natasha': [
            'data/dict/*.txt',
            'data/emb/*.tar',
            'data/model/*.tar',
        ]
    },
    install_requires=[
        'pymorphy2',
        'razdel>=0.5.0',
        'navec>=0.9.0',
        'slovnet>=0.6.0',
        'yargy>=0.14.0',
        'ipymarkup>=0.8.0',
    ]
)
