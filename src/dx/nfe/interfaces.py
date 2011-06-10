# -*- coding: utf-8 -*-
from zope.interface import Interface, Attribute

class INFeDataSource(Interface):
    """
    Este adaptador converte Notas Fiscais do formato da aplicacao de entrada
    para o formato XML padrão.
    """
    dsn = Attribute("Data Source Name")

    def connect(self):
        """
        Estabelece conexao com a fonte de dados.
        """
        
    def validate(self, f):
        """
        Valida o formato de entrada do arquivo txt. 
        """

    def load(self, f):
        """
        Carrega os dados do arquivo em um dicionario.
        """
        
class INFeXml(Interface):
    """
    Este modelo representa a NF-e no seu formato xml.
    """

    root = Attribute("Raiz do documento XML.")
    
    def __repr__:
        """
        Exibe a repreentacao da NF-e em XML.
        """

class IXmlMsg(Interface):
    """
    Este modelo representa uma mensagem SOAP em XML.
    """
    
    root = Attribute("Raiz do documento XML.")
    
    def __repr__:
        """
        Exibe a representacao da Mensagem XML.
        """

class IDanfe(Interface):
    """
    Esta View gera a representacao da NF-e como DANFE.
    """

class IWebServiceClient(Interface):
    """
    Este adaptador conecta no webservice da receita para transmissao de
    mensagens.
    """

    uri = Attribute("URI do webservice")
    timeout = Attribute("Tempo para finalizar a tentativa de conexão")
    
    
