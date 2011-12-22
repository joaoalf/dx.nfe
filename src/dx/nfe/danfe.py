# -*- coding: utf-8 -*-
__author__ = 'joaoalf'

import os, shutil
import lxml.etree as ET
from lpod.document import odf_get_document

class OdfTemplateNotFound(Exception):
    def __init__(self, value=None):
        self.value = value

    def __str__(self):
        print self.value

class XmlNfeNotFound(Exception):
    def __init__(self, value=None):
        self.value = value

    def __str__(self):
        print self.value

class Odf(object):
    """
    This class generate a DANFE in ODF (Open Document Format) from a template file.
    """

    _namespace = 'http://www.portalfiscal.inf.br/nfe'

    orientation = 0
    xml_tree = None

    canhoto_fields = ['AC9', 'AF50', 'AF9', 'AD1']
    cabecalho_fields = ['B1', 'G1', 'O4', 'N6', 'N7', 'O8', 'Q1', 'Q5', 'A10', 'Q10', 'A12', 'J12', 'S12']
    destinatario_fields = ['A15', 'P15', 'V15',
                           'A17', 'M17', 'R17', 'V17',
                           'A19', 'H19', 'L19', 'N19', 'S19', 'V19']
    imposto_fields = ['A22', 'G22', 'L22', 'R22', 'W22',
                      'A24', 'E24', 'I24', 'M24', 'R24', 'W24']
    transportadora_fields = ['A27', 'L27', 'P27', 'U27', 'W27', 'X27',
                             'A29', 'L29', 'T29', 'U29',
                             'A31', 'E31', 'I31', 'L31', 'Q31', 'V31']
    produto_fields = ['A35', 'C35', 'J35', 'K35', 'L35', 'M35', 'N35', 'P35',
                      'R35', 'T35', 'U35', 'V35', 'W35', 'X35', 'Y35', 'Z35']

    def __init__(self, xml_path=None, orientation=0):
        self.xml_path = xml_path
        self.orientation = orientation
        self.nfe_id = None

    def loadXmlFromFile(self):
        if os.path.exists(self.xml_path):
            self.xml_tree = ET.parse(self.xml_path)
        else:
            raise XmlNfeNotFound

    def getNfeId(self):
        return self.xml_tree.xpath('//ns:chNFe', namespaces={'ns': self._namespace})[0].text

    def getTagValue(self, tagname):
        if tagname.find('.'):
            parent, tag = tagname.split('.')[1]
        else:
            tag = tagname
            parent = None

        result_list = self.xml_tree.xpath('//ns:' + tag, namespaces={'ns': self._namespace})
        if parent:
            for i in result_list:
                if i.getparent().tag.replace('{'+self._namespace+'}', '') == parent:
                    return i.text

        else:
            return result_list[0].text

    def setTemplate(self, path):
        if os.path.exists(path):
            shutil.copyfile(path, os.path.join(os.environ['TMPDIR'], self.nfe_id + '.ods'))
            self.danfe = odf_get_document(os.path.join(os.environ['TMPDIR'], self.nfe_id + '.ods'))
        else:
            raise OdfTemplateNotFound

    def fillCanhoto(self):
        body = self.danfe.get_body()
        table = body.get_table_list()[0]

        ## Mensagem
        cell = table.get_cell_list(canhoto_fields[0])[0]
        canhoto_msg = u'RECEBEMOS DE %s O(S) PRODUTO(S) CONSTANTE(S) DA NOTA FISCAL INDICADA AO LADO' % self.getTag('emit.xnome')
        cell.set_cell_value(canhoto_msg)
        table.set_cell(cell.name, cell)

        ## N. NF-e


    