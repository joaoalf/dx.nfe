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
        opts.tags = config.get(u'getdata', u'tags')
        if not opts.xml:
            opts.xml = config.get(u'getdata', u'xml')
        if not opts.first_only:
            if config.get(u'getdata', u'primeiro') == '0':
                opts.first_only = False
            elif config.get(u'getdata', u'primeiro') == '1':
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
                      help=u"""Arquivo contendo a justificativa para cancelamento""")
    parser.add_option(
        u'-C',
        u'--cnpj',
        type=u'string',
        action=u'store',
        help=u"""CNPJ para inutilizacao""")
    parser.add_option(
        u'-S',
        u'--serie',
        type=u'string',
        action=u'store',
        help=u"""Serie da NFs para inutilizacao""")
    parser.add_option(
        u'-b',
        u'--numero_inicial',
        type=u'string',
        action=u'store',
        help=u"""Numero inicial para inutilizacao""")
    parser.add_option(
        u'-e',
        u'--numero_final',
        type=u'string',
        action=u'store',
        help=u"""Numero final para inutilizacao""")

    opts, args = parser.parse_args()

    config = ConfigParser.RawConfigParser()
    if not opts.config:
        config.read(CONF_FILE)
    else:
        config.read([opts.config])

    try:
        if not opts.status:
            opts.status = config.get(u'main', u'status')
    except (ConfigParser.NoOptionError, ConfigParser.NoSectionError, ValueError):
        parser.print_help()
        print "Parametro incorreto: -s ", opts.status
        sys.exit(-1)

    try:
        if not opts.uf:
            opts.uf = config.get(u'main', u'uf')

    except (ConfigParser.NoOptionError, ConfigParser.NoSectionError, ValueError):
        parser.print_help()
        print "Parametro incorreto: -u ", opts.uf
        sys.exit(-1)


        #if not opts.cert:
    opts.cert = config.get(u'main', u'cert')
    opts.cert_pw = config.get(u'main', u'senha')
    opts.versao = config.get(u'main', u'versao')
    opts.ambiente = config.get(u'main', u'ambiente')
    opts.logo = config.get(u'main', u'logo')

    try:
        if not opts.modo:
            opts.modo = config.get(u'main', u'modo')

    except (ConfigParser.NoOptionError, ConfigParser.NoSectionError, ValueError):
        parser.print_help()
        print "Parametro incorreto: -m ", opts.modo
        sys.exit(-1)

    if opts.modo == u'EMISSAO' or opts.modo == u'emissao':
        try:
            if not opts.nfe:
                opts.nfe = config.get(u'main', u'nfe')

        except (ConfigParser.NoOptionError, ConfigParser.NoSectionError, ValueError):
            parser.print_help()
            print "Parametro incorreto: -n ", opts.nfe
            sys.exit(-1)

        try:
            if not opts.prefixo:
                opts.xml = config.get(u'main', u'prefixo')

        except (ConfigParser.NoOptionError, ConfigParser.NoSectionError, ValueError):
            parser.print_help()
            print "Parametro incorreto: -p ", opts.prefixo
            sys.exit(-1)

        try:
            if not opts.tipo:
                opts.tipo = config.get(u'main', u'tipo')

        except (ConfigParser.NoOptionError, ConfigParser.NoSectionError, ValueError):
            parser.print_help()
            print "Parametro incorreto: -t ", opts.tipo
            sys.exit(-1)

    elif opts.modo == u'CANCELAMENTO' or opts.modo == u'cancelamento':
        try:
            if not opts.chave:
                raise ValueError

        except (ConfigParser.NoOptionError, ConfigParser.NoSectionError, ValueError):
            parser.print_help()
            print "Parametro incorreto: -k ", opts.chave
            sys.exit(-1)

        try:
            if not opts.justificativa:
                raise ValueError

        except (ConfigParser.NoOptionError, ConfigParser.NoSectionError, ValueError):
            parser.print_help()
            print "Parametro incorreto: -j ", opts.justificativa
            sys.exit(-1)

        try:
            if not opts.prefixo:
                raise ValueError

        except (ConfigParser.NoOptionError, ConfigParser.NoSectionError, ValueError):
            parser.print_help()
            print "Parametro incorreto: -p ", opts.prefixo
            sys.exit(-1)

    elif opts.modo == u'STATUSS' or opts.modo == u'statuss':

        try:
            if not opts.prefixo:
                raise ValueError

        except (ConfigParser.NoOptionError, ConfigParser.NoSectionError, ValueError):
            parser.print_help()
            print "Parametro incorreto: -p ", opts.prefixo
            sys.exit(-1)

    elif opts.modo == u'STATUSE' or opts.modo == u'statuse':
        try:
            if not opts.chave:
                raise ValueError

        except (ConfigParser.NoOptionError, ConfigParser.NoSectionError, ValueError):
            parser.print_help()
            print "Parametro incorreto: -k ", opts.chave
            sys.exit(-1)

    elif opts.modo == u'INUTILIZACAO' or opts.modo == u'inutilizacao':
        try:
            if not opts.cnpj:
                raise ValueError

        except (ConfigParser.NoOptionError, ConfigParser.NoSectionError, ValueError):
            parser.print_help()
            print "Parametro incorreto: -C ", opts.cnpj
            sys.exit(-1)

        try:
            if not opts.serie:
                raise ValueError

        except (ConfigParser.NoOptionError, ConfigParser.NoSectionError, ValueError):
            parser.print_help()
            print "Parametro incorreto: -S ", opts.serie
            sys.exit(-1)

        try:
            if not opts.numero_inicial:
                raise ValueError

        except (ConfigParser.NoOptionError, ConfigParser.NoSectionError, ValueError):
            parser.print_help()
            print "Parametro incorreto: -b ", opts.numero_inicial
            sys.exit(-1)

        try:
            if not opts.numero_final:
                raise ValueError

        except (ConfigParser.NoOptionError, ConfigParser.NoSectionError, ValueError):
            parser.print_help()
            print "Parametro incorreto: -e ", opts.numero_final
            sys.exit(-1)

        try:
            if not opts.numero_final:
                raise ValueError

        except (ConfigParser.NoOptionError, ConfigParser.NoSectionError, ValueError):
            parser.print_help()
            print "Parametro incorreto: -j ", opts.justificativa
            sys.exit(-1)

        try:
            if not opts.prefixo:
                raise ValueError

        except (ConfigParser.NoOptionError, ConfigParser.NoSectionError, ValueError):
            parser.print_help()
            print "Parametro incorreto: -p ", opts.prefixo
            sys.exit(-1)

        try:
            if not opts.justificativa:
                raise ValueError

        except (ConfigParser.NoOptionError, ConfigParser.NoSectionError, ValueError):
            parser.print_help()
            print "Parametro incorreto: -j ", opts.justificativa
            sys.exit(-1)

    else:
        parser.print_help()
        print u"Parametro incorreto: -m ", opts.modo
        sys.exit(-1)

    del config
#except (ConfigParser.NoOptionError, ConfigParser.NoSectionError, ValueError):
#    parser.print_help()
#    sys.exit(-1)

    #print opts.tipo
    
    app = dx.nfe.dxnfe.DX_NFE(
        opts.modo.upper(),
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
        opts.uf.upper(),
        opts.justificativa,
        opts.logo,
        opts.cnpj,
        opts.serie,
        opts.numero_inicial,
        opts.numero_final
)
    #print dir(app)
    app.main()

def dxdanfe():
    """Generate a DANFE from a xml file
    """
    import sys
    import ConfigParser
    from optparse import OptionParser
    import dx.nfe.danfe

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
    parser.add_option(u'-l',
        u'--logo',
        type=u'string',
        action=u'store',
        help=u"""Logo file""")
    parser.add_option(u'-p',
        u'--prefixo',
        type=u'string',
        action=u'store',
        help=u"""Prefixo da geração dos arquivos""")
    parser.add_option(u'-t',
        u'--template',
        type=u'string',
        action=u'store',
        help=u"""Caminho do template do DANFE""")
    parser.add_option(u'-o',
        u'--orientacao',
        type=u'string',
        action=u'store',
        help=u"""1 - Retato / 2 - Paisagem""")
    parser.add_option(u'-s',
        u'--saida',
        type=u'string',
        action=u'store',
        help=u"""Arquivo de saida""")

    opts, args = parser.parse_args()

    config = ConfigParser.RawConfigParser()
    if not opts.config:
        config.read(CONF_FILE)
    else:
        config.read([opts.config])

    try:
        if not opts.xml:
            opts.xml = config.get(u'danfe', u'xml')

        if not opts.template:
            opts.template = config.get(u'danfe', u'template')

        if not opts.logo:
            opts.logo = config.get(u'danfe', u'logo')

        if not opts.saida:
            opts.logo = config.get(u'danfe', u'saida')

    except (ConfigParser.NoOptionError, ValueError):
        parser.print_help()
        sys.exit(-1)

    del config

    App = dx.nfe.danfe.Odf(opts.xml, opts.template, opts.saida, opts.orientacao, opts.logo, opts.prefixo)
    App.main()
