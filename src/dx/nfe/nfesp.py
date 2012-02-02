# -*- coding: utf-8 -*-
from zope.interface import implements
#from zope.component import adapts
from interfaces import INFeDataSource
from datetime import datetime
from pysped.nfe.manual_401 import NFe_200, Det_200, Vol_200, Lacres_200, Dup_200
from pysped.nfe.manual_300 import NFe_110

class GroupNotImplemented(Exception):
    def __init__(self, group):
        Exception.__init__(self)
        self.group = group

    def __str__(self):
        print "Group %s is not implemented!" % self.group

class NFeSP(object):
    implements(INFeDataSource)
    #adapts(NFeXML)
    
    def __init__(self, dsn):
        self.dsn = dsn
        self.txt = None
        self.nfs = None

    def connect(self):
        try:
            self.txt = open(self.dsn.replace('file://', ''))
        except OSError, e:
            print e
            raise

    def load(self):
        d = []
        n = []
        i = -1
        d1 = None
        line = None
        #nota_atual = -1

        for l in self.txt.readlines():
            try:
                line = l.replace('\r\n', '')
                if line.find('|') != -1:
                    line = line.split('|')
                    line.reverse()
                    grupo = line.pop()
                else:
                    grupo = line.replace('\n', '')
                    #print grupo
                    
                #print grupo
                if grupo == 'NOTA FISCAL':
                    #num = int(line.pop())
                    i += 1
                    #nota_atual = i
                elif grupo == 'A':
                    versao = line.pop()
                    #print versao
                    if versao == '1.10':
                        NFe = NFe_110
                    elif versao == '2.00':
                        NFe = NFe_200
                    else:
                        NFe = None
                    id = line.pop()

                    n.append(NFe())
                    n[i].infNFe.Id.valor = id
                    n[i].chave = id[3:]

                elif grupo == 'B':
                    #
                    # Identificação da NF-e
                    #
                    n[i].infNFe.ide.cUF.valor     = line.pop()
                    n[i].infNFe.ide.cNF.valor     = line.pop()
                    n[i].infNFe.ide.natOp.valor   = line.pop()
                    n[i].infNFe.ide.indPag.valor  = line.pop()
                    n[i].infNFe.ide.mod.valor     = line.pop()
                    n[i].infNFe.ide.serie.valor   = line.pop()
                    n[i].infNFe.ide.nNF.valor     = line.pop()
                    data = line.pop()
                    n[i].infNFe.ide.dEmi.valor    = datetime(int(data[:4]), int(data[5:7]), int(data[8:10]))
                    data = line.pop()
                    n[i].infNFe.ide.dSaiEnt.valor = datetime(int(data[:4]),
                                                             int(data[5:7]),
                                                             int(data[8:10]))
                    n[i].infNFe.ide.hSaiEnt.valor = line.pop()
                    n[i].infNFe.ide.tpNF.valor    = line.pop()
                    n[i].infNFe.ide.cMunFG.valor  = line.pop()
                    n[i].infNFe.ide.tpImp.valor   = line.pop()
                    n[i].infNFe.ide.tpEmis.valor  = line.pop()
                    n[i].infNFe.ide.cDV.valor     = line.pop()
                    n[i].infNFe.ide.tpAmb.valor   = line.pop()
                    n[i].infNFe.ide.finNFe.valor  = line.pop()
                    n[i].infNFe.ide.procEmi.valor = line.pop()
                    n[i].infNFe.ide.verProc.valor = line.pop()
                    n[i].infNFe.ide.dhCont.valor  = line.pop()
                    n[i].infNFe.ide.xJust.valor   = line.pop()
                elif grupo == 'C':
                    #
                    # Emitente
                    #
                    n[i].infNFe.emit.xNome.valor = line.pop()
                    n[i].infNFe.emit.xFant.valor = line.pop()
                    n[i].infNFe.emit.IE.valor    = line.pop()
                    n[i].infNFe.emit.IEST.valor  = line.pop()
                    n[i].infNFe.emit.IM.valor    = line.pop()
                    n[i].infNFe.emit.CNAE.valor  = line.pop()
                    n[i].infNFe.emit.CRT.valor   = int(line.pop())

                elif grupo == 'C02':
                    n[i].infNFe.emit.CNPJ.valor  = line.pop()
                elif grupo == 'C02a':
                    n[i].infNFe.emit.CPF.valor  = line.pop()
                elif grupo == 'C05':
                    n[i].infNFe.emit.enderEmit.xLgr.valor    = line.pop()
                    n[i].infNFe.emit.enderEmit.nro.valor     = line.pop() #+ '_'
                    n[i].infNFe.emit.enderEmit.xCpl.valor    = line.pop()
                    n[i].infNFe.emit.enderEmit.xBairro.valor = line.pop()
                    n[i].infNFe.emit.enderEmit.cMun.valor    = line.pop()
                    n[i].infNFe.emit.enderEmit.xMun.valor    = line.pop()
                    n[i].infNFe.emit.enderEmit.UF.valor      = line.pop()
                    n[i].infNFe.emit.enderEmit.CEP.valor     = line.pop()
                    n[i].infNFe.emit.enderEmit.cPais.valor   = line.pop()
                    n[i].infNFe.emit.enderEmit.xPais.valor   = line.pop()
                    n[i].infNFe.emit.enderEmit.fone.valor    = line.pop()
                elif grupo == 'D':
                    raise GroupNotImplemented(grupo)
                    #
                    # Regime tributário
                    #
                    #n[i].infNFe.emit.CRT.valor = 3
                elif grupo == 'E':
                    #
                    # Destinatário
                    #
                    n[i].infNFe.dest.xNome.valor = line.pop()
                    n[i].infNFe.dest.IE.valor    = line.pop()
                    n[i].infNFe.dest.ISUF.valor  = line.pop()
                elif grupo == 'E02':
                    n[i].infNFe.dest.CNPJ.valor  = line.pop()
                elif grupo == 'E03':
                    n[i].infNFe.dest.CPF.valor   = line.pop()
                elif grupo == 'E05':
                    n[i].infNFe.dest.enderDest.xLgr.valor    = line.pop()
                    n[i].infNFe.dest.enderDest.nro.valor     = line.pop() #+ '_'
                    n[i].infNFe.dest.enderDest.xCpl.valor    = line.pop()
                    n[i].infNFe.dest.enderDest.xBairro.valor = line.pop()
                    n[i].infNFe.dest.enderDest.cMun.valor    = line.pop()
                    n[i].infNFe.dest.enderDest.xMun.valor    = line.pop()
                    n[i].infNFe.dest.enderDest.UF.valor      = line.pop()
                    n[i].infNFe.dest.enderDest.CEP.valor     = line.pop()
                    n[i].infNFe.dest.enderDest.cPais.valor   = line.pop()
                    n[i].infNFe.dest.enderDest.xPais.valor   = line.pop()
                    n[i].infNFe.dest.enderDest.fone.valor    = line.pop()
                    #
                    # Emeio
                    #
                    n[i].infNFe.dest.email.valor             = line.pop()
                elif grupo == 'F':
                    n[i].infNFe.retirada.enderDest.CNPJ.valor    = line.pop()
                    n[i].infNFe.retirada.enderDest.xLgr.valor    = line.pop()
                    n[i].infNFe.retirada.enderDest.nro.valor     = line.pop()
                    n[i].infNFe.retirada.enderDest.xCpl.valor    = line.pop()
                    n[i].infNFe.retirada.enderDest.xBairro.valor = line.pop()
                    n[i].infNFe.retirada.enderDest.cMun.valor    = line.pop()
                    n[i].infNFe.retirada.enderDest.xMun.valor    = line.pop()
                    n[i].infNFe.retirada.enderDest.UF.valor      = line.pop()
                elif grupo == 'G':
                    n[i].infNFe.entrega.enderDest.CNPJ.valor    = line.pop()
                    n[i].infNFe.entrega.enderDest.xLgr.valor    = line.pop()
                    n[i].infNFe.entrega.enderDest.nro.valor     = line.pop()
                    n[i].infNFe.entrega.enderDest.xCpl.valor    = line.pop()
                    n[i].infNFe.entrega.enderDest.xBairro.valor = line.pop()
                    n[i].infNFe.entrega.enderDest.cMun.valor    = line.pop()
                    n[i].infNFe.entrega.enderDest.xMun.valor    = line.pop()
                    n[i].infNFe.entrega.enderDest.UF.valor      = line.pop()
                elif grupo == 'H':
                    #grupo = linha.pop()
                    #
                    # Detalhe
                    #
                    d1 = Det_200()
                    d1.imposto.regime_tributario = 3
                    d.append(d1)
                    d1.nItem.valor = line.pop()
                    d1.infAdProd.valor = line.pop()
                elif grupo == 'I':
                    #print line
                    d1.prod.cProd.valor    = line.pop()
                    d1.prod.cEAN.valor     = line.pop()
                    d1.prod.cEAN.valor     = u''
                    d1.prod.xProd.valor    = line.pop()
                    d1.prod.NCM.valor      = line.pop()
                    d1.prod.EXTIPI.valor   = line.pop()
                    d1.prod.CFOP.valor     = line.pop()
                    d1.prod.uCom.valor     = line.pop()
                    d1.prod.qCom.valor     = line.pop()
                    d1.prod.vUnCom.valor   = line.pop()
                    d1.prod.vProd.valor    = line.pop()
                    cEANTrib = line.pop()
                    if cEANTrib == '' and d1.prod.cEAN.valor != '':
                        d1.prod.cEANTrib.valor = d1.prod.cEAN.valor
                    else:
                        d1.prod.cEANTrib.valor = cEANTrib
                        
                    d1.prod.uTrib.valor    = line.pop()
                    d1.prod.qTrib.valor    = line.pop()
                    d1.prod.vUnTrib.valor  = line.pop()
                    d1.prod.vFrete.valor   = line.pop()
                    d1.prod.vSeg.valor     = line.pop()
                    d1.prod.vDesc.valor    = line.pop()
                    d1.prod.vOutro.valor   = line.pop()
                    #
                    # Produto entra no total da NF-e
                    #
                    d1.prod.indTot.valor   = line.pop()
                elif grupo == 'I18':
                    d1.prod.DI.dDI.valor         = line.pop()
                    d1.prod.DI.xLocDesemb.valor  = line.pop()
                    d1.prod.DI.UFDesemb.valor    = line.pop()
                    d1.prod.DI.dDesemb.valor     = line.pop()
                    d1.prod.DI.cExportador.valor = line.pop()
                    #d1.prod.genero.valor   = line.pop()
                elif grupo == 'I25':
                    d1.prod.DI.adi.nAdicao.valor     = line.pop()
                    d1.prod.DI.adi.nSeqAdic.valor    = line.pop()
                    d1.prod.DI.adi.cFabricante.valor = line.pop()
                    d1.prod.DI.adi.vDescDI.valor     = line.pop()
                    #d1.prod.adi.cExportador.valor = line.pop()
                elif grupo == 'J':
                    raise GroupNotImplemented(grupo)
                elif grupo == 'K':
                    raise GroupNotImplemented(grupo)
                elif grupo == 'L':
                    raise GroupNotImplemented(grupo)
                elif grupo == 'L01':
                    raise GroupNotImplemented(grupo)
                elif grupo == 'L105':
                    raise GroupNotImplemented(grupo)
                elif grupo == 'L109':
                    raise GroupNotImplemented(grupo)
                elif grupo == 'L114':
                    raise GroupNotImplemented(grupo)
                elif grupo == 'L117':
                    raise GroupNotImplemented(grupo)
                #
                # Impostos
                #
                elif grupo == 'M':
                    pass
                elif grupo == 'N':
                    d1.imposto.regime_tributario = 3
                elif grupo == 'N02':
                    d1.imposto.ICMS.orig.valor  = line.pop()
                    d1.imposto.ICMS.CST.valor   = line.pop()
                    d1.imposto.ICMS.modBC.valor = line.pop()
                    d1.imposto.ICMS.vBC.valor   = line.pop()
                    d1.imposto.ICMS.pICMS.valor = line.pop()
                    d1.imposto.ICMS.vICMS.valor = line.pop()
                elif grupo == 'N03':
                    d1.imposto.ICMS.orig.valor     = line.pop()
                    d1.imposto.ICMS.CST.valor      = line.pop()
                    d1.imposto.ICMS.modBC.valor    = line.pop()
                    d1.imposto.ICMS.vBC.valor      = line.pop()
                    d1.imposto.ICMS.pICMS.valor    = line.pop()
                    d1.imposto.ICMS.vICMS.valor    = line.pop()
                    d1.imposto.ICMS.modBCST.valor  = line.pop()
                    d1.imposto.ICMS.pMVAST.valor   = line.pop()
                    d1.imposto.ICMS.pRedBCST.valor = line.pop()
                    d1.imposto.ICMS.vBCST.valor    = line.pop()
                    d1.imposto.ICMS.pICMSST.valor  = line.pop()
                    d1.imposto.ICMS.vICMSST.valor  = line.pop()
                elif grupo == 'N04':
                    d1.imposto.ICMS.orig.valor   = line.pop()
                    d1.imposto.ICMS.CST.valor    = line.pop()
                    d1.imposto.ICMS.modBC.valor  = line.pop()
                    d1.imposto.ICMS.pRedBC.valor = line.pop()
                    d1.imposto.ICMS.vBC.valor    = line.pop()
                    d1.imposto.ICMS.pICMS.valor  = line.pop()
                    d1.imposto.ICMS.vICMS.valor  = line.pop()
                elif grupo == 'N05':
                    d1.imposto.ICMS.orig.valor     = line.pop()
                    d1.imposto.ICMS.CST.valor      = line.pop()
                    d1.imposto.ICMS.modBCST.valor  = line.pop()
                    d1.imposto.ICMS.pMVAST.valor   = line.pop()
                    d1.imposto.ICMS.pRedBCST.valor = line.pop()
                    d1.imposto.ICMS.vBCST.valor    = line.pop()
                    d1.imposto.ICMS.pICMSST.valor  = line.pop()
                    d1.imposto.ICMS.vICMSST.valor  = line.pop()
                elif grupo == 'N06':
                    d1.imposto.ICMS.orig.valor  = line.pop()
                    d1.imposto.ICMS.CST.valor   = line.pop()
                elif grupo == 'N07':
                    d1.imposto.ICMS.orig.valor   = line.pop()
                    d1.imposto.ICMS.CST.valor    = line.pop()
                    d1.imposto.ICMS.modBC.valor  = line.pop()
                    d1.imposto.ICMS.pRedBC.valor = line.pop()
                    d1.imposto.ICMS.vBC.valor    = line.pop()
                    d1.imposto.ICMS.pICMS.valor  = line.pop()
                    d1.imposto.ICMS.vICMS.valor  = line.pop()
                elif grupo == 'N08':
                    d1.imposto.ICMS.orig.valor    = line.pop()
                    d1.imposto.ICMS.CST.valor     = line.pop()
                    d1.imposto.ICMS.vBCST.valor   = line.pop()
                    d1.imposto.ICMS.vICMSST.valor = line.pop()
                elif grupo == 'N09':
                    d1.imposto.ICMS.orig.valor     = line.pop()
                    d1.imposto.ICMS.CST.valor      = line.pop()
                    d1.imposto.ICMS.modBC.valor    = line.pop()
                    d1.imposto.ICMS.pRedBC.valor = line.pop()
                    d1.imposto.ICMS.vBC.valor      = line.pop()
                    d1.imposto.ICMS.pICMS.valor    = line.pop()
                    d1.imposto.ICMS.vICMS.valor    = line.pop()
                    d1.imposto.ICMS.modBCST.valor  = line.pop()
                    d1.imposto.ICMS.pMVAST.valor   = line.pop()
                    d1.imposto.ICMS.pRedBCST.valor = line.pop()
                    d1.imposto.ICMS.vBCST.valor    = line.pop()
                    d1.imposto.ICMS.pICMSST.valor  = line.pop()
                    d1.imposto.ICMS.vICMSST.valor  = line.pop()
                elif grupo == 'N10':
                    d1.imposto.ICMS.orig.valor     = line.pop()
                    d1.imposto.ICMS.CST.valor      = line.pop()
                    d1.imposto.ICMS.modBC.valor    = line.pop()
                    d1.imposto.ICMS.vBC.valor      = line.pop()
                    d1.imposto.ICMS.pRedBC.valor   = line.pop()
                    d1.imposto.ICMS.pICMS.valor    = line.pop()
                    d1.imposto.ICMS.vICMS.valor    = line.pop()
                    d1.imposto.ICMS.modBCST.valor  = line.pop()
                    d1.imposto.ICMS.pMVAST.valor   = line.pop()
                    d1.imposto.ICMS.pRedBCST.valor = line.pop()
                    d1.imposto.ICMS.vBCST.valor    = line.pop()
                    d1.imposto.ICMS.pICMSST.valor  = line.pop()
                    d1.imposto.ICMS.vICMSST.valor  = line.pop()
                elif grupo == 'O':
                    d1.imposto.IPI.clEnq.valor    = line.pop()
                    d1.imposto.IPI.CNPJProd.valor = line.pop()
                    d1.imposto.IPI.cSelo.valor    = line.pop()
                    d1.imposto.IPI.qSelo.valor    = line.pop()
                    d1.imposto.IPI.cEnq.valor     = line.pop()
                    #d1.imposto.IPI.vIPI.valor   = u'100.00'
                elif grupo == 'O07':
                    d1.imposto.IPI.CST.valor  = line.pop()
                    d1.imposto.IPI.vIPI.valor = line.pop()
                elif grupo == 'O08':
                    d1.imposto.IPI.CST.valor = line.pop()
                elif grupo == 'O10':
                    d1.imposto.IPI.vBC.valor  = line.pop()
                    d1.imposto.IPI.pIPI.valor = line.pop()
                elif grupo == 'O11':
                    d1.imposto.IPI.qUnid.valor = line.pop()
                    d1.imposto.IPI.vUnid.valor = line.pop()
                elif grupo == 'P':
                    raise GroupNotImplemented(grupo)
                elif grupo == 'Q':
                    pass
                elif grupo == 'Q02':
                    d1.imposto.PIS.CST.valor  = line.pop()
                    d1.imposto.PIS.vBC.valor  = line.pop()
                    d1.imposto.PIS.pPIS.valor = line.pop()
                    d1.imposto.PIS.vPIS.valor = line.pop()
                elif grupo == 'Q03':
                    d1.imposto.PIS.CST.valor       = line.pop()
                    d1.imposto.PIS.qBCProd.valor   = line.pop()
                    d1.imposto.PIS.vAliqProd.valor = line.pop()
                    d1.imposto.PIS.vPIS.valor      = line.pop()
                elif grupo == 'Q04':
                    d1.imposto.PIS.CST.valor = line.pop()
                elif grupo == 'Q05':
                    d1.imposto.PIS.CST.valor  = line.pop()
                    d1.imposto.PIS.vPIS.valor = line.pop()
                elif grupo == 'Q07':
                    d1.imposto.PIS.vBC.valor  = line.pop()
                    d1.imposto.PIS.pPIS.valor = line.pop()
                elif grupo == 'Q10':
                    d1.imposto.PIS.qBCProd.valor   = line.pop()
                    d1.imposto.PIS.vAliqProd.valor = line.pop()
                elif grupo == 'R':
                    d1.imposto.PISST.vPIS.valor  = line.pop()
                elif grupo == 'R02':
                    d1.imposto.PIS.vBC.valor  = line.pop()
                    d1.imposto.PIS.pPIS.valor = line.pop()
                elif grupo == 'R04':
                    d1.imposto.PIS.qBCProd.valor   = line.pop()
                    d1.imposto.PIS.vAliqProd.valor = line.pop()
                elif grupo == 'S':
                    pass
                elif grupo == 'S02':
                    d1.imposto.COFINS.CST.valor     = line.pop()
                    d1.imposto.COFINS.vBC.valor     = line.pop()
                    d1.imposto.COFINS.pCOFINS.valor = line.pop()
                    d1.imposto.COFINS.vCOFINS.valor = line.pop()
                elif grupo == 'S03':
                    d1.imposto.COFINS.CST.valor       = line.pop()
                    d1.imposto.COFINS.qBCProd.valor   = line.pop()
                    d1.imposto.COFINS.vAliqProd.valor = line.pop()
                    d1.imposto.COFINS.vCOFINS.valor   = line.pop()
                elif grupo == 'S04':
                    d1.imposto.COFINS.CST.valor       = line.pop()
                elif grupo == 'S05':
                    d1.imposto.COFINS.CST.valor       = line.pop()
                    d1.imposto.COFINS.vCOFINS.valor   = line.pop()
                elif grupo == 'S07':
                    d1.imposto.COFINS.vBC.valor     = line.pop()
                    d1.imposto.COFINS.pCOFINS.valor = line.pop()
                elif grupo == 'S09':
                    d1.imposto.COFINS.qBCProd.valor   = line.pop()
                    d1.imposto.COFINS.vAliqProd.valor = line.pop()
                elif grupo == 'T':
                    d1.imposto.COFINSST.vCOFINS.valor = line.pop()
                elif grupo == 'T02':
                    d1.imposto.COFINSST.vBC.valor     = line.pop()
                    d1.imposto.COFINSST.pCOFINS.valor = line.pop()
                elif grupo == 'T04':
                    d1.imposto.COFINSST.qBCProd.valor   = line.pop()
                    d1.imposto.COFINSST.vAliqProd.valor = line.pop()
                elif grupo == 'U':
                    d1.imposto.ISSQN.vBC.valor       = line.pop()
                    d1.imposto.ISSQN.vAliq.valor     = line.pop()
                    d1.imposto.ISSQN.vISSQN.valor    = line.pop()
                    d1.imposto.ISSQN.cMunFG.valor    = line.pop()
                    d1.imposto.ISSQN.cListServ.valor = line.pop()
                    # Inclui o detalhe na NF-e
                elif grupo == 'W':
                    # Totais
                    #print "Totais"
                    #print d
                    for prod in d:
                        prod.imposto.regime_tributario = 3
                        n[i].infNFe.det.append(prod)

                elif grupo == 'W02':
                    n[i].infNFe.total.ICMSTot.vBC.valor     = line.pop()
                    n[i].infNFe.total.ICMSTot.vICMS.valor   = line.pop()
                    n[i].infNFe.total.ICMSTot.vBCST.valor   = line.pop()
                    n[i].infNFe.total.ICMSTot.vST.valor     = line.pop()
                    n[i].infNFe.total.ICMSTot.vProd.valor   = line.pop()
                    n[i].infNFe.total.ICMSTot.vFrete.valor  = line.pop()
                    n[i].infNFe.total.ICMSTot.vSeg.valor    = line.pop()
                    n[i].infNFe.total.ICMSTot.vDesc.valor   = line.pop()
                    n[i].infNFe.total.ICMSTot.vII.valor     = line.pop()
                    n[i].infNFe.total.ICMSTot.vIPI.valor    = line.pop()
                    n[i].infNFe.total.ICMSTot.vPIS.valor    = line.pop()
                    n[i].infNFe.total.ICMSTot.vCOFINS.valor = line.pop()
                    n[i].infNFe.total.ICMSTot.vOutro.valor  = line.pop()
                    n[i].infNFe.total.ICMSTot.vNF.valor     = line.pop()
                elif grupo == 'W17':
                    n[i].infNFe.total.ISSQNtot.vServ.valor   = line.pop()
                    n[i].infNFe.total.ISSQNtot.vBC.valor     = line.pop()
                    n[i].infNFe.total.ISSQNtot.vISS.valor    = line.pop()
                    n[i].infNFe.total.ISSQNtot.vPIS.valor    = line.pop()
                    n[i].infNFe.total.ISSQNtot.vCOFINS.valor = line.pop()
                elif grupo == 'W23':
                    n[i].infNFe.total.retTrib.vRetPIS.valor    = line.pop()
                    n[i].infNFe.total.retTrib.vRetCOFINS.valor = line.pop()
                    n[i].infNFe.total.retTrib.vRetCSLL.valor   = line.pop()
                    n[i].infNFe.total.retTrib.vBCIRRF.valor    = line.pop()
                    n[i].infNFe.total.retTrib.vIRRF.valor      = line.pop()
                    n[i].infNFe.total.retTrib.vBCRetPrev.valor = line.pop()
                    n[i].infNFe.total.retTrib.vRetPrev.valor   = line.pop()
                elif grupo == 'X':
                    n[i].infNFe.transp.modFrete.valor = line.pop()
                elif grupo == 'X03':
                    n[i].infNFe.transp.transporta.xNome.valor  = line.pop()
                    n[i].infNFe.transp.transporta.IE.valor     = line.pop()
                    n[i].infNFe.transp.transporta.xEnder.valor = line.pop()
                    n[i].infNFe.transp.transporta.UF.valor     = line.pop()
                    n[i].infNFe.transp.transporta.xMun.valor   = line.pop()
                elif grupo == 'X04':
                    n[i].infNFe.transp.transporta.CNPJ.valor = line.pop()
                elif grupo == 'X05':
                    n[i].infNFe.transp.transporta.CPF.valor = line.pop()
                elif grupo == 'X11':
                    n[i].infNFe.transp.retTransp.vServ.valor    = line.pop()
                    n[i].infNFe.transp.retTransp.vBCRet.valor   = line.pop()
                    n[i].infNFe.transp.retTransp.pICMSRet.valor = line.pop()
                    n[i].infNFe.transp.retTransp.vICMSRet.valor = line.pop()
                    n[i].infNFe.transp.retTransp.CFOP.valor     = line.pop()
                    n[i].infNFe.transp.retTransp.cMunFG.valor   = line.pop()
                elif grupo == 'X18':
                    n[i].infNFe.transp.veicTransp.placa.valor = line.pop()
                    n[i].infNFe.transp.veicTransp.UF.valor    = line.pop()
                    n[i].infNFe.transp.veicTransp.RNTC.valor  = line.pop()
                elif grupo == 'X22':
                    n[i].infNFe.transp.reboque.placa.valor = line.pop()
                    n[i].infNFe.transp.reboque.UF.valor    = line.pop()
                    n[i].infNFe.transp.reboque.RNTC.valor  = line.pop()
                elif grupo == 'X26':
                    v1 = Vol_200()
                    v1.qVol.valor  = line.pop()
                    v1.esp.valor   = line.pop()
                    v1.marca.valor = line.pop()
                    v1.nVol.valor  = line.pop()
                    v1.pesoL.valor = line.pop()
                    v1.pesoB.valor = line.pop()
                    n[i].infNFe.transp.vol.append(v1)
                elif grupo == 'X33':
                    l1 = Lacres_200()
                    l1.nLacre.valor  = line.pop()
                    n[i].infNFe.transp.vol.append(l1)
                elif grupo == 'Y':
                    pass
                elif grupo == 'Y02':
                    n[i].infNFe.cobr.fat.nFat.valor  = line.pop()
                    n[i].infNFe.cobr.fat.vOrig.valor = line.pop()
                    n[i].infNFe.cobr.fat.vDesc.valor = line.pop()
                    n[i].infNFe.cobr.fat.vLiq.valor  = line.pop()
                elif grupo == 'Y07':
                    dup1 = Dup_200()
                    dup1.nDup.valor  = line.pop()
                    dup1.dVenc.valor = line.pop()
                    dup1.vDup.valor  = line.pop()
                    n[i].infNFe.cobr.dup.append(dup1)
                elif grupo == 'Z':
                    n[i].infNFe.infAdic.infAdFisco.valor = line.pop()
                    n[i].infNFe.infAdic.infCpl.valor     = line.pop()
                elif grupo == 'Z04':
                    n[i].infNFe.infAdic.obsCont.xCampo.valor = line.pop()
                    n[i].infNFe.infAdic.obsCont.xTexto.valor = line.pop()
                elif grupo == 'Z07':
                    n[i].infNFe.infAdic.obsFisco.xCampo.valor = line.pop()
                    n[i].infNFe.infAdic.obsFisco.xTexto.valor = line.pop()
                elif grupo == 'Z10':
                    n[i].infNFe.infAdic.procRef.nProc.valor   = line.pop()
                    n[i].infNFe.infAdic.procRef.indProc.valor = line.pop()
                elif grupo == 'ZA':
                    raise GroupNotImplemented(grupo)
                elif grupo == 'ZB':
                    raise GroupNotImplemented(grupo)

            except TypeError:
                print line
                raise


        self.nfs = n
                
    def validate(self):
        #for line in self.txt:
        #    pass
        return True
    
    
