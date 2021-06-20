"""
maggport setup file
"""
from setuptools import find_packages, setup

# Only install package dependencies in install_requires
setup(
    name='maggport',
    version='1.0.0',
    description='A mongodb aggregate export tool',
    long_description='A mongodb aggregate export tool',
    entry_points={
        'console_scripts': [
            'maggport = maggport.maggport:maggport'
        ]
    },
    url='https://github.com/ccavales3/maggport',
    author='Caesar Cavales',
    author_email='c.cavales3@gmail.com',
    license='MIT',
    packages=find_packages(exclude=['tests']),
    install_requires=[
            'click==8.0.1',      # https://github.com/pallets/click
            'pymongo==3.11.4',   # https://github.com/mongodb/mongo-python-driver
            'pandas==1.2.1'      # https://github.com/pandas-dev/pandas
    ],
    zip_safe=False
)
