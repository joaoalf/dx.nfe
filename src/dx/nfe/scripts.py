# -*- coding: utf-8 -*-

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
    CONF_FILE = ['./dxnfe.cfg',
                 '/etc/dxnfe.cfg',
                 '/usr/local/etc/dxnfe.cfg']
    ##

    parser = OptionParser(usage=u"""%prog [options]""")
    parser.add_option(u'-c',
                      u'--config',
                      type=u'string',
                      action=u'store',
                      help=u"""Configration file""")
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

        if not opts.modo:
            opts.modo = config.get(u'main', u'modo')
        if opts.modo == 'EMISSAO':
            if not opts.nfe:
                opts.nfe = config.get(u'main', u'nfe')
            if not opts.xml:
                opts.xml = config.get(u'main', u'xml')
            if not opts.danfe:
                opts.danfe = config.get(u'main', u'danfe')
            if not opts.tipo:
                opts.tipo = config.get(u'main', u'tipo')
        elif opts.modo == u'CANCELAMENTO':
            if not opts.chave:
                raise ValueError

        del config
    except (ConfigParser.NoOptionError, ValueError):
        parser.print_help()
        raise
        sys.exit(-1)

    #print opts.tipo
    
    app = dx.nfe.dxnfe.DX_NFE(
        opts.modo,
        opts.cert,
        opts.cert_pw,
        opts.nfe,
        opts.xml,
        opts.danfe,
        opts.status,
        opts.chave,
        opts.tipo,
        opts.versao,
        opts.ambiente)
    #print dir(app)
    app.main()
    
