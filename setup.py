# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import os

setup(
    name=u'dx.nfe', 
    version=u'1.0', 
    author=u'João Alfredo Gama Batista', 
    author_email=u'joaoalf@dotx.com.br', 
    description=u'Emissor de Nota Fiscal Eletrônica.',
    namespace_packages=['dx',],
    package_dir={'': 'src'},
    packages=find_packages('src'), 
    include_package_data=True,
    entry_points={'console_scripts':['dxnfe = dx.nfe.scripts:dxnfe',],},
    install_requires=['setuptools',
                      'zope.component', 
                      'zope.interface',
                      'zope.event',
                      'lxml',
                      'PyXMLSec',
                      'reportlab',
                      'Geraldo'],
)
