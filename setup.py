# pylint: disable=missing-docstring
from distutils.core import setup

setup(
    name='noticast-iot-core',
    version='0.1-dev',
    packages=['noticast'],
    install_requires=['AWSIoTPythonSDK', 'requests', 'raven'])
