# -*- coding: utf-8 -*-

CONF_FILE = ['./dxnfe.cfg',
             '/etc/dxnfe.cfg',
             '/usr/local/etc/dxnfe.cfg']

def dxgetdata():
    """Get tags from a xml file
    """
    import sys
    import ConfigParser
    from optparse import OptionParser
    import dx.nfe.getdata

    parser = OptionParser(usage=u"""%prog [options]""")
    parser.add_option(u'-c',
                      u'--config',
                      type=u'string',
                      action=u'store',
                      help=u"""Configration file""")
    parser.add_option(u'-x',
                      u'--xml',
                      type=u'string',
                      action=u'store',
                      help=u"""Xml file""")
    parser.add_option(u'-f',
                      u'--first-only',
                      dest=u'first_only',
                      action=u'store_true',
                      help=u"""Return only the first element found""")

    opts, args = parser.parse_args()

    config = ConfigParser.RawConfigParser()
    if not opts.config:
        config.read(CONF_FILE)
    else:
        config.read([opts.config])

    try:
        opts.tags = config.get(u'dxgetdata', u'tags')
        if not opts.xml:
            opts.xml = config.get(u'dxgetdata', u'xml')
        if not opts.first_only:
            if config.get(u'dxgetdata', u'primeiro') == '0':
                opts.first_only = False
            elif config.get(u'dxgetdata', u'primeiro') == '1':
                opts.first_only = True
        
        del config
    except (ConfigParser.NoOptionError, ValueError):
        parser.print_help()
        raise
        sys.exit(-1)

    App = dx.nfe.getdata.GetData(opts.xml, opts.tags.split(), opts.first_only)
    App.main()

def dxnfe():
    """Script principal da aplicação"""
    import sys
    #import os
    #import random
    #import time
    import ConfigParser
    #import datetime
    #from decimal import Decimal
    from optparse import OptionParser
    import dx.nfe.dxnfe
    #from dx.nfe import emissor, cancelador, inutilizador

    ## Constants
    ##

    parser = OptionParser(usage=u"""%prog [options]""")
    parser.add_option(u'-c',
                      u'--config',
                      type=u'string',
                      action=u'store',
                      help=u"""Configration file""")
    parser.add_option(u'-u',
                      u'--uf',
                      type=u'string',
                      action=u'store',
                      help=u"""Unidade Federativa""")
    parser.add_option(u'-s',
                      u'--status',
                      type=u'string',
                      action=u'store',
                      help=u"""Arquivo de status""")
    parser.add_option(u'-m',
                      u'--modo',
                      type=u'string',
                      action=u'store',
                      help=u"""Modo de operacao: [ EMISSAO | STATUSE | STATUSS | CANCELAMENTO | INUTILIZACAO ]""")
    parser.add_option(u'-n',
                      u'--nfe',
                      type=u'string',
                      action=u'store',
                      help=u"""Arquivo de NFE""")    
    parser.add_option(u'-p',
                      u'--prefixo',
                      type=u'string',
                      action=u'store',
                      help=u"""Prefixo da geração dos arquivos""")
    parser.add_option(u'-x',
                      u'--xml',
                      type=u'string',
                      action=u'store',
                      help=u"""Arquivo XML""")
    parser.add_option(u'-d',
                      u'--danfe',
                      type=u'string',
                      action=u'store',
                      help=u"""Arquivo DANFE""")    
    parser.add_option(u'-k',
                      u'--chave',
                      type=u'string',
                      action=u'store',
                      help=u"""Chave da NFE""")    
    parser.add_option(u'-t',
                      u'--tipo',
                      type=u'string',
                      action=u'store',
                      help=u"""Formato do arquivo de entrada""")
    parser.add_option(u'-j',
                      u'--justificativa',
                      type=u'string',
                      action=u'store',
                      help=u"""Justificativa para cancelamento""")

    opts, args = parser.parse_args()

    config = ConfigParser.RawConfigParser()
    if not opts.config:
        config.read(CONF_FILE)
    else:
        config.read([opts.config])

    try:
        if not opts.status:
            opts.status = config.get(u'main', u'status')
        #if not opts.cert:
        opts.cert = config.get(u'main', u'cert')
        opts.cert_pw = config.get(u'main', u'senha')
        opts.versao = config.get(u'main', u'versao')
        opts.ambiente = config.get(u'main', u'ambiente')
        opts.logo = config.get(u'main', u'logo')

        if not opts.modo:
            opts.modo = config.get(u'main', u'modo')
        if opts.modo == 'EMISSAO':
            if not opts.nfe:
                opts.nfe = config.get(u'main', u'nfe')
            if not opts.prefixo:
                opts.xml = config.get(u'main', u'prefixo')
            #if not opts.danfe:
            #    opts.danfe = config.get(u'main', u'danfe')
            if not opts.tipo:
                opts.tipo = config.get(u'main', u'tipo')
        elif opts.modo == u'CANCELAMENTO':
            if not opts.chave or not opts.justificativa:
                raise ValueError

        del config
    except (ConfigParser.NoOptionError, ConfigParser.NoSectionError, ValueError):
        parser.print_help()
        sys.exit(-1)

    #print opts.tipo
    
    app = dx.nfe.dxnfe.DX_NFE(
        opts.modo,
        opts.cert,
        opts.cert_pw,
        opts.nfe,
        opts.prefixo,
        #opts.danfe,
        opts.status,
        opts.chave,
        opts.tipo,
        opts.versao,
        opts.ambiente,
        opts.uf,
        opts.justificativa,
        opts.logo)
    #print dir(app)
    app.main()
    
