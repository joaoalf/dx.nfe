# -*- coding: utf-8 -*-
__author__ = 'joaoalf'

import os, shutil, re, decimal, datetime
import lxml.etree as ET
from lpod.frame import odf_create_image_frame
from lpod.document import odf_get_document
import code128
from py3o.renderclient import RenderClient

class OdfTemplateNotFound(Exception):
    def __init__(self, value=None):
        Exception.__init__(self)
        self.value = value

    def __str__(self):
        print self.value

class XmlNfeNotFound(Exception):
    def __init__(self, value=None):
        Exception.__init__(self)
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

    def __init__(self,
                 xml_path=None,
                 template_prefix=None,
                 output=u'',
                 orientation=u'1',
                 logo=u'',
                 server=('127.0.0.1', 8994),
                 prefix=u''):
        self.xml_path = xml_path
        self.template_prefix = template_prefix
        self.output = output
        self.orientation = orientation
        self.logo = logo
        self.server = server
        self.prefix = prefix
        self.nfe_id = None
        self.template_path = os.path.join(
            self.template_prefix,
            u'DanfeTemplate' + unicode(self.orientation) + u'.ods'
        )

    def main(self):
        self.loadXmlFromFile()
        self.nfe_id = self.getNfeId()
        self.setTemplate()
        self.fillDANFE()
        shutil.copyfile(self.tmp_path, os.path.join(self.prefix, self.output.replace('.pdf', '.ods')))
        os.unlink(self.tmp_path)
        self.convertToPdf2()

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

    def setTemplate(self):
        if self.output == u'':
            self.output = self.nfe_id + '.ods'

        if os.path.exists(self.template_path):
            self.tmp_path = os.path.join(os.environ['TMPDIR'], self.output.replace('.pdf', '.ods'))
            shutil.copyfile( self.template_path, self.tmp_path)
            self.danfe = odf_get_document(self.tmp_path)
        else:
            print self.template_path
            raise OdfTemplateNotFound

    def fillCanhoto(self):
        body = self.danfe.get_body()
        table = body.get_table_list()[0]

        ## Mensagem
        cell = table.get_cell_list(canhoto_fields[0])[0]
        canhoto_msg = u'RECEBEMOS DE %s O(S) PRODUTO(S) CONSTANTE(S) DA NOTA FISCAL INDICADA AO LADO' % self.getTagValue('emit.xnome')
        cell.set_cell_value(canhoto_msg)
        table.set_cell(cell.name, cell)

        ## N. NF-e

    def genBarcode(self):
        barcode = code128.Code128()
        barcode.getImage(self.nfe_id, 10)

    def fillDANFE(self):
        body = self.danfe.get_body()
        danfe = body.get_table_list()[0]
        danfe_value = None

        for n in self.xml_tree.iter():
            #print n
            if n.tag.find(self._namespace) == -1:
                continue

            try:
                danfe_key = u'.'.join([
                    n.getparent().tag.replace('{'+self._namespace+'}', ''),
                    n.tag.replace('{'+self._namespace+'}', '')]
                )

                if re.search('[.][vqp][A-Z]', danfe_key):
                    try:
                        danfe_value = decimal.Decimal(n.text)
                    except decimal.InvalidOperation:
                        danfe_value = None
                    #print danfe_key, danfe_value
                elif re.search('[.][d][A-Z]', danfe_key):
                    try:
                        danfe_value = datetime.datetime.strptime(n.text, '%Y-%m-%d')
                    except:
                        raise
                elif danfe_key.find('nNF') != -1:
                    danfe_value = int(n.text)
                elif danfe_key.find('CEP') != -1:
                    danfe_value = n.text[:5] + '-' + n.text[5:]
                elif danfe_key.find('CNPJ') != -1:
                    danfe_value = n.text[:2] + '.' +\
                                  n.text[2:5] + '.' +\
                                  n.text[5:8] + '/' +\
                                  n.text[8:12] + '-' + n.text[12:]

                elif danfe_key.find('CPF') != -1:
                    danfe_value = n.text[:3] + '.' +\
                                  n.text[3:6] + '.' +\
                                  n.text[6:9] + '-' +\
                                  n.text[9:]

                elif danfe_key.find('chNFe') != -1:
                    danfe_value = n.text[:4] + '.' +\
                                  n.text[4:8] + '.' +\
                                  n.text[8:12] + '.' +\
                                  n.text[12:16] + '.' +\
                                  n.text[16:20] + '.' +\
                                  n.text[20:24] + '.' +\
                                  n.text[24:28] + '.' +\
                                  n.text[28:32] + '.' +\
                                  n.text[32:36] + '.' +\
                                  n.text[36:40] + '.' +\
                                  n.text[40:]
                elif danfe_key.find('modFrete') != -1:
                    if n.text == '0':
                        danfe_value = "0 - EMITENTE"
                    elif n.text == '1':
                        danfe_value = "1 - DESTINATARIO"

                else:
                    danfe_value = n.text
                #print danfe_key
            except AttributeError:
                danfe_key = None

            if danfe_key:
                if re.search('ICMS[0-9][0-9]\.', danfe_key):
                    danfe_key = danfe_key[:4] + danfe_key[6:]
                    #print danfe_key

                if danfe_key == u'emit.xNome':
                    xnome = danfe_value

                for x, y, c in danfe.get_cells(content=u'%%'+danfe_key+u'%%'):
                    #print c.get_type(), c.get_value()
                    if isinstance(danfe_value, str) or isinstance(danfe_value, unicode):
                        c.set_value(c.get_value().replace(u'%%'+danfe_key+u'%%', danfe_value))
                    else:
                        c.set_value(danfe_value)

                    danfe.set_cell((x, y), c)
                    if danfe_key.find('ide.nNF') == -1 and danfe_key.find('ide.serie') == -1:
                        break

        # Put the logo
        x, y, c = danfe.get_cells(content=u'danfe.xLogo')[0]
        logo_uri = self.danfe.add_file(self.logo)

        frame = odf_create_image_frame(
            logo_uri,
            size=('5.20cm', '2.10cm'),
            position=('0cm', '0cm')
        )


        #frame.set_size(frame.get_size())
        #frame.set_attribute('table:end-cell-address', 'Paisagem.F8')
        #print frame.get_attributes()

        danfe.set_cell_image((x, y), frame, type=self.danfe.get_type())
        #frame.set_size(('5.87cm', '2.65cm'))
        danfe.get_frame_list()[0].set_attribute('table:end-cell-address', 'Paisagem.F8')
        danfe.get_frame_list()[0].set_attribute('table:end-x', '5.20cm')
        danfe.get_frame_list()[0].set_attribute('table:end-y', '2.10cm')
        danfe.get_frame_list()[0].set_attribute('svg:width', '5.20cm')
        danfe.get_frame_list()[0].set_attribute('svg:height', '2.10cm')
        #print danfe.get_frame_list()[0].get_attributes()

        # Put the barcode
        x, y, c = danfe.get_cells(content=u'danfe.xBarcode')[0]
        self.genBarcode()

        barcode_uri = self.danfe.add_file(self.nfe_id + '.png')

        frame = odf_create_image_frame(
            barcode_uri,
            size=('9.35cm', '0.85cm'),
            position=('0cm', '0cm')
        )

        danfe.set_cell_image((x, y), frame, type=self.danfe.get_type())
        danfe.get_frame_list()[1].set_attribute('table:end-cell-address', 'Paisagem.Z3')

        # Put the canhoto
        x, y, c = danfe.get_cells(content=u'danfe.xCanhoto')[0]
        danfe_value = u'RECEBEMOS DE %s O(S) PRODUTO(S) CONSTANTE(S) DA NOTA FISCAL INDICADA AO LADO' % xnome
        c.set_value(danfe_value)

        danfe.set_cell((x, y), c)

        # Clean the unused fields
        for x, y, c in danfe.get_cells(content=u'%%'):
            value = c.get_value() or '%%None%%'
            regex = re.search('%%.*%%', value)
            c.set_value(value.replace(regex.group(0), u''))
            danfe.set_cell((x, y), c)


        self.danfe.save()
        os.unlink(self.nfe_id + '.png')


    def convertToPdf(self):
        client = RenderClient(self.server[0], self.server[1])
        #client.login('toto', 'plouf')
        #print self.output.replace('.pdf', '.ods'), self.output

        client.render(os.path.join(self.prefix, self.output.replace('.pdf', '.ods')),
                      os.path.join(self.prefix, self.output))
    def convertToPdf2(self):
        cmd = 'scp -i /etc/pdfgen.key ' + \
              os.path.join(self.prefix, self.output.replace('.pdf', '.ods')) + \
              ' ' + \
              'pdfgen@10.25.18.5:'
        os.system(cmd)

        cmd = 'ssh -i /etc/pdfgen.key ' + \
              'pdfgen@10.25.18.5 ' + \
              'unoconv ' + \
              self.output.replace('.pdf', '.ods')
        os.system(cmd)

        cmd = 'scp -i /etc/pdfgen.key ' + \
              'pdfgen@10.25.18.5:' + \
              self.output + \
              ' ' + \
              os.path.join(self.prefix, self.output)
        os.system(cmd)
        
        
