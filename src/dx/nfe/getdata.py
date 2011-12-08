# -*- coding: utf-8 -*-
__author__ = 'joaoalf'

import sys
import lxml.etree

class GetData(object):
    """GetData receives a list of xml tags and extract then from a xml file"""

    _namespace = 'http://www.portalfiscal.inf.br/nfe'

    def __init__(self, xml=u'', tags=[], first_only=False):
        self.xml = xml
        self.tags = tags
        self.first_only = first_only

    def main(self):
        try:
            #xml_file = codecs.open(self.xml, 'r', 'utf-8')
            infNFe = lxml.etree.parse(self.xml)
        except:
            raise

        for t in self.tags:
            if self.first_only:
                try:
                    n = infNFe.xpath('//ns:'+t, namespaces={'ns': self._namespace})[0]
                    print n.getparent().tag.replace('{'+self._namespace+'}', '') + '.' + t + u': ' + n.text
                except IndexError:
                    pass
            else:
                nodes = infNFe.xpath('//ns:'+t, namespaces={'ns': self._namespace})
                if nodes:
                    for n in nodes:
                        print n.getparent().tag.replace('{'+self._namespace+'}', '') + '.' + t + u': ' + n.text

        del infNFe

        sys.exit(0)

        