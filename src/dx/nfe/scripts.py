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
                      help=u"""Arquivo de configuracao""")
    parser.add_option(u'-x',
                      u'--xml',
                      type=u'string',
                      action=u'store',
                      help=u"""Arquivo XML""")
    parser.add_option(u'-f',
                      u'--first-only',
                      dest=u'first_only',
                      action=u'store_true',
                      help=u"""Retorna apenas a primeira instancia de cada tag""")

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

    except ConfigParser.NoOptionError as e:
        parser.print_help()
        print
        print 'Parametro faltando: --%s' % e.option
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
    parser.add_option(
        u'-c',
        u'--config',
        type=u'string',
        action=u'store',
        help=u"""Configration file""")
    parser.add_option(
        u'-u',
        u'--uf',
        type=u'string',
        action=u'store',
        help=u"""Unidade Federativa""")
    parser.add_option(
        u'-s',
        u'--status',
        type=u'string',
        action=u'store',
        help=u"""Arquivo de status""")
    parser.add_option(
        u'-m',
        u'--modo',
        type=u'string',
        action=u'store',
        help=u"""Modo de operacao: [ EMISSAO | STATUSE | STATUSS | CANCELAMENTO | INUTILIZACAO ]""")
    parser.add_option(
        u'-n',
        u'--nfe',
        type=u'string',
        action=u'store',
        help=u"""Arquivo de NFE""")
    parser.add_option(
        u'-p',
        u'--prefixo',
        type=u'string',
        action=u'store',
        help=u"""Prefixo da geração dos arquivos""")
    parser.add_option(
        u'-x',
        u'--xml',
        type=u'string',
        action=u'store',
        help=u"""Arquivo XML""")
    parser.add_option(
        u'-d',
        u'--danfe',
        type=u'string',
        action=u'store',
        help=u"""Arquivo DANFE""")
    parser.add_option(
        u'-k',
        u'--chave',
        type=u'string',
        action=u'store',
        help=u"""Chave da NFE""")
    parser.add_option(
        u'-t',
        u'--tipo',
        type=u'string',
        action=u'store',
        help=u"""Formato do arquivo de entrada""")
    parser.add_option(
        u'-j',
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

        if not opts.uf:
            opts.uf = config.get(u'main', u'uf')
        opts.cert = config.get(u'main', u'cert')
        opts.cert_pw = config.get(u'main', u'senha')
        opts.versao = config.get(u'main', u'versao')
        opts.ambiente = config.get(u'main', u'ambiente')
        opts.logo = config.get(u'main', u'logo')

        if not opts.modo:
            opts.modo = config.get(u'main', u'modo')

        elif opts.modo == u'EMISSAO' or opts.modo == u'emissao':
            if not opts.nfe:
                opts.nfe = config.get(u'main', u'nfe')

            if not opts.prefixo:
                opts.xml = config.get(u'main', u'prefixo')

            if not opts.tipo:
                opts.tipo = config.get(u'main', u'tipo')

        elif opts.modo == u'CANCELAMENTO' or opts.modo == u'cancelamento':
            if not opts.chave:
                raise ConfigParser.NoOptionError('chave', 'main')

            if not opts.justificativa:
                raise ConfigParser.NoOptionError('justificativa', 'main')

            if not opts.prefixo:
                raise ConfigParser.NoOptionError('prefixo', 'main')

        elif opts.modo == u'STATUSS' or opts.modo == u'statuss':
            if not opts.prefixo:
                raise ConfigParser.NoOptionError('prefixo', 'main')

        elif opts.modo == u'STATUSE' or opts.modo == u'statuse':
            if not opts.chave:
                raise ConfigParser.NoOptionError('chave', 'main')

            if not opts.prefixo:
                raise ConfigParser.NoOptionError('prefixo', 'main')

        elif opts.modo == u'INUTILIZACAO' or opts.modo == u'inutilizacao':
            if not opts.cnpj:
                raise ConfigParser.NoOptionError('cnpj', 'main')

            if not opts.serie:
                raise ConfigParser.NoOptionError('serie', 'main')

            if not opts.numero_inicial:
                raise ConfigParser.NoOptionError('numero_inicial', 'main')

            if not opts.numero_final:
                raise ConfigParser.NoOptionError('numero_final', 'main')

            if not opts.prefixo:
                raise ConfigParser.NoOptionError('prefixo', 'main')

            if not opts.justificativa:
                raise ConfigParser.NoOptionError('justificativa', 'main')

        else:
            parser.print_help()
            print u"Parametro incorreto: -m ", opts.modo
            sys.exit(-1)

    except ConfigParser.NoOptionError as e:
        parser.print_help()
        print
        print 'Parametro faltando: --%s' % e.option
        sys.exit(-1)

    except ValueError:
        raise

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
    parser.add_option(u'-H',
        u'--host',
        type=u'string',
        action=u'store',
        help=u"""Servidor de renderizacao de PDF""")
    parser.add_option(u'-P',
        u'--port',
        type=u'string',
        action=u'store',
        help=u"""Porta do servidor de renderizacao de PDF""")

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

        if not opts.orientacao:
            opts.orientacao = config.get(u'danfe', u'orientacao')

        if not opts.prefixo:
            opts.prefixo = config.get(u'danfe', u'prefixo')

        if not opts.host:
            opts.host = config.get(u'danfe', u'host')

        if not opts.port:
            opts.port = config.get(u'danfe', u'port')

    except ConfigParser.NoOptionError as e:
        parser.print_help()
        print
        print 'Parametro faltando: --%s' % e.option
        sys.exit(-1)

    except ValueError:
        raise

    del config

    App = dx.nfe.danfe.Odf(
        opts.xml,
        opts.template,
        opts.saida,
        opts.orientacao,
        opts.logo,
        (opts.host, int(opts.port)),
        opts.prefixo
    )
    App.main()
