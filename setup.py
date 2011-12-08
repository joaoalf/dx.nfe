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
    entry_points={'console_scripts':['dxnfe = dx.nfe.scripts:dxnfe',
                                     'dxgetdata = dx.nfe.scripts:dxgetdata'],},
    zip_safe = False,
    dependency_links = ['https://github.com/joaoalf/PySPED/tarball/master#egg=PySPED-0.1dev_joaoalf_branch'],
    install_requires=['setuptools',
                      'zope.component',
                      'zope.interface==3.8.0',
                      'zope.event',
                      'lxml',
                      'PySPED',
                      'libxml2-python',
                      'lpod-python',],
)
