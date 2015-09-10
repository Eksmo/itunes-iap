from __future__ import with_statement

from setuptools import setup


def get_readme():
    try:
        with open('README.rst') as f:
            return f.read().strip()
    except IOError:
        return ''


requirements = [
    'requests>=2.7.0',
    'six',
]

test_requirements = [
    'pytest>=2.7.2',
    'vcrpy>=1.7.3',
    'mock>=1.3.0',
]

setup(
    name='itunes-iap',
    version='0.6.6',
    description='Itunes In-app purchase verification api.',
    long_description=get_readme(),
    author='Jeong YunWon',
    author_email='itunesiap@youknowone.org',
    url='https://github.com/youknowone/itunes-iap',
    packages=[
        'itunesiap',
    ],
    install_requires=requirements,
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    tests_require=requirements + test_requirements,
    extras_require={
        'test': test_requirements,
    },
)
