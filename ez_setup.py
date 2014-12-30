""" Setup """
from setuptools import setup, find_packages
setup(
    name="FjoSpidie",
    version="2.1",
    packages=find_packages(),
    dependency_links=[
        'https://github.com/espenfjo/pylibpcap/archive/0.6.4.2.tar.gz#egg=pylibpcap-0.6.4.2',
        'lib/suricatasc'
    ],
    install_requires=[
        'selenium',
        'pyaml',
        'pymongo',
        'browsermob-proxy',
        'harpy',
        'pydot',
        'pylibpcap',
        'configobj',
        'simplejson',
        'cidrize',
        'pygeoip',
        'dnspython'
    ],
)
