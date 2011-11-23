# -*- coding: utf-8 -*-
import sys, os, codecs
import interfaces
from nfesp import NFeSP
from pysped.nfe.processador_nfe import ProcessadorNFe

class DX_NFE(object):
    """Main Class"""

    def __init__(self,
                 mode,
                 cert,
                 cert_pw,
                 nfe,
                 xml,
                 danfe,
                 status,
                 key,
                 ftype,
                 versao,
                 ambiente,
                 uf,
                 justificativa,
                 logo):
        #self.directory = directory
        self.proc = ProcessadorNFe(logo=logo)
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
        if os.path.exists(self.status):
            os.unlink(self.status)

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
                with codecs.open(self.status, 'a', 'utf-8') as st:
                    st.write(u'|'.join(
                        [processo.resposta.cStat.valor,
                         processo.resposta.xMotivo.valor])
                    )
                    st.write('\n')

        elif self.mode == u'STATUSS':
            processo = self.proc.consultar_servico()
            with codecs.open(self.status, 'w', 'utf-8') as status:
                status.write(u'|'.join([processo.resposta.cStat.valor,
                                        processo.resposta.xMotivo.valor]))

        elif self.mode == u'STATUSE':
            processo = self.proc.consultar_nota(chave_nfe=self.key)
            with codecs.open(self.status, 'w', 'utf-8') as status:
                status.write(u'|'.join([processo.resposta.cStat.valor,
                                        processo.resposta.xMotivo.valor]))

        elif self.mode == u'CANCELAMENTO':
            processo = self.proc.cancelar_nota(
                chave_nfe=self.key,
                numero_protocolo=processo.resposta.protNFe.infProt.nProt.valor,
                justificativa=self.justificativa)
            with codecs.open(self.status, 'w', 'utf-8') as status:
                status.write(u'|'.join([processo.resposta.cStat.valor,
                                        processo.resposta.xMotivo.valor]))

        elif self.mode == u'INUTILIZACAO':
            processo = self.proc.inutilizar_nota()
            print u"Status: " + str(processo.resposta.status)
            print u"Motivo: " + unicode(processo.resposta.xMotivo.valor)
            #print
            print processo.resposta.reason

