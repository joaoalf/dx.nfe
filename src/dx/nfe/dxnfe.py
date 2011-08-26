# -*- coding: utf-8 -*-
import sys

try:
    import emissor
except:
    from dx.nfe import emissor

class DX_NFE(object):
    """Main Class"""

    def __init__(self, directory, cert, mode, nfe, xml, danfe, key):
        self.directory = directory
        self.cert = cert
        self.mode = mode
        self.nfe = nfe
        self.xml = xml
        self.danfe = danfe
        self.key = key

    def main(self):
        if self.modo == 'EMISSAO':
            if self.formato == 'TXT200':
                self.nfe = self.fillNFEfromTXT200(self.txt)
            else:
                raise NotImplementedFormat(self.formato)
            
            handler = emissor.Emissor(self.nfe,
                                      self.emissor,
                                      self.xml,
                                      self.danfe)
            try:
                handler.run()
            except:
                sys.exit(-1)
        elif modo == 'STATUSE':
            pass
        elif modo == 'STATUSS':
            pass
        elif modo == 'CANCELAMENTO':
            pass
        elif modo == 'INUTILIZACAO':
            pass

    def fillNFEfromTXT200(self, txt):
        pass
    
