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
                 prefix,
                 #danfe,
                 status,
                 key,
                 ftype,
                 versao,
                 ambiente,
                 uf,
                 justificativa,
                 logo):
        #self.directory = directory
        if mode == u'EMISSAO':
            self.caminho = os.path.join(prefix, os.path.split(nfe)[1][:-4])
        else:
            self.caminho = prefix
        self.proc = ProcessadorNFe(caminho=self.caminho, logo=logo)
        self.proc.certificado.arquivo = cert
        self.proc.certificado.senha = cert_pw
        self.mode = mode
        self.nfe = nfe
        #self.xml = xml
        #self.danfe = danfe
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
        #self.proc.caminho = u''
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
                fields = [processo.resposta.cStat.valor,
                          processo.resposta.xMotivo.valor]
                status.write(u'|'.join(fields))

        elif self.mode == u'STATUSE':
            processo = self.proc.consultar_nota(chave_nfe=self.key, prefix=self.caminho)
            with codecs.open(self.status, 'w', 'utf-8') as status:
                fields = [processo.resposta.cStat.valor, processo.resposta.xMotivo.valor]
                if processo.resposta.cStat.valor in (u'100', u'110'):
                    fields.append(processo.resposta.protNFe.infProt.nProt.valor)
                elif processo.resposta.cStat.valor == u'101':
                    fields.append(processo.resposta.retCancNFe.infCanc.nProt.valor)

                status.write(u'|'.join(fields))

        elif self.mode == u'CANCELAMENTO':
            processo1 = self.proc.consultar_nota(chave_nfe=self.key, prefix=self.caminho)
            fields = [processo1.resposta.cStat.valor, processo1.resposta.xMotivo.valor]
            if processo1.resposta.cStat.valor in (u'100', u'110'):
                fields.append(processo1.resposta.protNFe.infProt.nProt.valor)
            elif processo1.resposta.cStat.valor == u'101':
                fields.append(processo1.resposta.retCancNFe.infCanc.nProt.valor)

            with codecs.open(self.status, 'a', 'utf-8') as status:
                status.write(u'|'.join(fields))
                status.write('\n')

                if processo1.resposta.cStat.valor in (u'100', u'110'):
                    processo2 = self.proc.cancelar_nota(
                        chave_nfe=self.key,
                        numero_protocolo=processo1.resposta.protNFe.infProt.nProt.valor,
                        justificativa=self.justificativa,
                        prefix=self.caminho)
                    fields = [processo2.resposta.infCanc.cStat.valor, processo2.resposta.infCanc.xMotivo.valor]
                    if processo2.resposta.infCanc.cStat.valor == u'101':
                        fields.append(processo2.resposta.infCanc.dhRecbto.valor)
                        fields.append(processo2.resposta.infCanc.nProt.valor)

                    try:
                        status.write(u'|'.join(fields))
                    except:
                        print processo2.resposta.xml
                
        elif self.mode == u'INUTILIZACAO':
            processo = self.proc.inutilizar_nota()
            print u"Status: " + str(processo.resposta.status)
            print u"Motivo: " + unicode(processo.resposta.xMotivo.valor)
            #print
            print processo.resposta.reason

