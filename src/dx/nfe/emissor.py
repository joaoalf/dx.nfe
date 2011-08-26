# -*- coding: utf-8 -*-

try:
    from PySPED.pysped.nfe import ProcessadorNFe
    from PySPED.pysped.nfe.webservices_flags import *
    from PySPED.pysped.nfe.manual_401 import *
except:
    from pysped.nfe import ProcessadorNFe
    from pysped.nfe.webservices_flags import *
    from pysped.nfe.manual_401 import *
from datetime import datetime

class Emissor(object):
    """Emissor"""

    def __init__(self, nfe, emissor, xml, danfe, cert_file, cert_pwd, versao, uf):
        self.nfe = nfe
        self.emissor = emissor
        self.xml = xml
        self.danfe = danfe
        self.cert_file = cert_file
        self.cert_pwd = cert_pwd
        self.versao = versao
        self.uf = uf

    def run(self):
        p = ProcessadorNFe()
        p.versao              = self.versao
        p.estado              = self.uf
        p.certificado.arquivo = self.cert_file
        p.certificado.senha   = self.cert_pwd
        p.salva_arquivos      = True
        p.contingencia_SCAN   = False
        p.caminho = u'' 

        #
        # O retorno de cada webservice é um dicionário
        # estruturado da seguinte maneira:
        # { TIPO_DO_WS_EXECUTADO: {
        #       u'envio'   : InstanciaDaMensagemDeEnvio,
        #       u'resposta': InstanciaDaMensagemDeResposta,
        #       }
        # }
        #
        for processo in p.processar_notas([self.nfe]):
            chave_processo = processo.keys()[0]
            print
            print
            print
            print chave_processo
            print
            print processo[chave_processo][u'envio'].xml
            print
            print processo[chave_processo][u'resposta'].xml
