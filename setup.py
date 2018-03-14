import sys

from setuptools import setup, find_packages

setup(
    name='currency-converter-kiwi',
    version='0.1.0',
    description='Currency converter entry task.',
    author='Radovan Lapár',
    packages=find_packages(),
    install_requires=[
        'click',
        'forex-python',
        'Flask',
	'uWSGI'
    ],
    setup_requires=[
        'pytest-runner'
    ],
    tests_require=[
        'pytest'
    ],
    entry_points={
        'console_scripts': [
            'currency_converter=currency_converter.cli:main'
        ]
    }
)
