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
                 logo,
                 cnpj,
                 serie,
                 numero_inicial,
                 numero_final):
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

        self.cnpj = cnpj
        self.serie = serie
        self.numero_inicial = numero_inicial
        self.numero_final = numero_final

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
            with open(self.justificativa, 'r') as fjust:
                just = fjust.readline()


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
                        justificativa=just,
                        prefix=self.caminho)
                    fields = [processo2.resposta.infCanc.cStat.valor, processo2.resposta.infCanc.xMotivo.valor]
                    if processo2.resposta.infCanc.cStat.valor == u'101':
                        fields.append(processo2.resposta.infCanc.dhRecbto.valor.strftime('%c'))
                        fields.append(processo2.resposta.infCanc.nProt.valor)

                    try:
                        status.write(u'|'.join(fields))
                    except:
                        print processo2.resposta.xml
                        print fields
                        raise
                
        elif self.mode == u'INUTILIZACAO':
            with open(self.justificativa, 'r') as fjust:
                just = fjust.readline()

            processo1 = self.proc.inutilizar_nota(
                cnpj=self.cnpj,
                serie=self.serie,
                numero_inicial=self.numero_inicial,
                numero_final=self.numero_final,
                justificativa=just
            )

            fields = [processo1.resposta.infInut.cStat.valor, processo1.resposta.infInut.xMotivo.valor]
            if processo1.resposta.infInut.cStat.valor == u'102':
                fields.append(processo1.resposta.infInut.dhRecbto.valor.strftime('%c'))
                fields.append(str(processo1.resposta.infInut.nProt.valor))

            with codecs.open(self.status, 'a', 'utf-8') as status:
                try:
                    status.write(u'|'.join(fields))
                    status.write('\n')
                except:
                    print processo1.resposta.xml
                    print fields
                    raise



