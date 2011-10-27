# -*- coding: utf-8 -*-
import sys
import interfaces
from nfesp import NFeSP
from pysped.nfe.processador_nfe import ProcessadorNFe
#try:
#    import emissor
#except ImportError:
#    from dx.nfe import emissor

class DX_NFE(object):
    """Main Class"""

    def __init__(self, mode, cert, cert_pw, nfe, xml, danfe, status, key, ftype, versao, ambiente, uf, justificativa):
        #self.directory = directory
        self.proc = ProcessadorNFe()
        self.proc.certificado.arquivo = cert
        self.proc.certificado.senha = cert_pw
        self.mode = mode
        self.nfe = nfe
        self.xml = xml
        self.danfe = danfe
        self.status = status
        self.key = key
        self.ftype = ftype
        self.proc.versao = versao
        if ambiente:
            self.proc.ambiente = int(ambiente)
        else:
            self.proc.ambiente = None

        self.proc.estado = uf
        self.proc.salvar_arquivos = True
        self.proc.contingencia_SCAN = False
        self.proc.caminho = u''
        self.justificativa = unicode(justificativa)

    def main(self):
        #print self.mode
        if self.mode == 'EMISSAO':
            self.nfxml = NFeSP(self.nfe)
            self.nfxml.connect()
            self.nfxml.load()
            #print self.nfxml.nfs
            if self.proc.ambiente:
                for n in self.nfxml.nfs:
                    n.infNFe.ide.tpAmb.valor = int(self.proc.ambiente)


            #
            # O retorno de cada webservice é um dicionário
            # estruturado da seguinte maneira:
            # { TIPO_DO_WS_EXECUTADO: {
            #       u'envio'   : InstanciaDaMensagemDeEnvio,
            #       u'resposta': InstanciaDaMensagemDeResposta,
            #       }
            # }
            #
            for processo in self.proc.processar_notas(self.nfxml.nfs):
                #chave_processo = processo.keys()[0]
                #print processo.envio.xml
                #print
                with open(self.status, 'w') as st:
                    st.write('|'.join(
                        [str(processo.resposta.cStat.valor),
                         unicode(processo.resposta.xMotivo.valor)]))
                #print u"Status: " + str(processo.resposta.cStat.valor)
                #print u"Motivo: " + unicode(processo.resposta.xMotivo.valor)
                #print
                #print processo.resposta.reason

        elif self.mode == u'STATUSS':
            processo = self.proc.consultar_servico()
            with open(self.status, 'w') as status:
                #print u"Status: " + str(processo.resposta.cStat.valor)
                #print u"Motivo: " + unicode(processo.resposta.xMotivo.valor)
                #print
                #print processo.resposta.reason
                status.write('|'.join([unicode(processo.resposta.cStat.valor),
                                       unicode(processo.resposta.xMotivo.valor)]))

        elif self.mode == u'STATUSE':
            processo = self.proc.consultar_nota(chave_nfe=self.key)
            with open(self.status, 'w') as status:
                #print u"Status: " + str(processo.resposta.cStat.valor)
                #print u"Motivo: " + unicode(processo.resposta.xMotivo.valor)
                #print
                #print processo.resposta.xml
                status.write('|'.join([unicode(processo.resposta.cStat.valor),
                                       unicode(processo.resposta.xMotivo.valor)]))

        elif self.mode == u'CANCELAMENTO':
            #processo1 = self.proc.consultar_nota(chave_nfe=self.key)
            #print u"Status: " + str(processo1.resposta.cStat.valor)
            #print u"Motivo: " + unicode(processo1.resposta.xMotivo.valor)
            #print
            #print processo1.resposta.xml
            #print processo1.resposta.protNFe.infProt.nProt.valor
            #if processo1.resposta.cStat.valor != u'101':
            processo = self.proc.cancelar_nota(
                chave_nfe=self.key,
                numero_protocolo=processo.resposta.protNFe.infProt.nProt.valor,
                justificativa=self.justificativa)
            with open(self.status, 'w') as status:
                status.write('|'.join([unicode(processo.resposta.cStat.valor),
                                       unicode(processo.resposta.xMotivo.valor)]))

            #print u"Status: " + str(processo2.resposta.status)
            #print u"Motivo: " + unicode(processo2.resposta.xMotivo.valor)
            #print
            #print processo.resposta.xml

        elif self.mode == u'INUTILIZACAO':
            processo = self.proc.inutilizar_nota()
            print u"Status: " + str(processo.resposta.status)
            print u"Motivo: " + unicode(processo.resposta.xMotivo.valor)
            #print
            print processo.resposta.reason

