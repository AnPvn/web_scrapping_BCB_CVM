from SiteManager import SiteManager
from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests

'''
IDEIA:
    como cada site tem uma estrutura diferente, eu passo o endereco de cada url com uma função quando for instanciar o objeto scraping.
    Essa função recebe o objeto beautifulSoup correspondente, e dai ela vasculha de um jeito especifico, ou seja, embora sejam do mesmo tipo, se comportam de maneiras específicas.
'''

class Scraping:
    def __init__(self, url, funcao, mode='lxml'):
        self.__url = url
        self.__funcao = funcao
        '''try:
            self.__bs = BeautifulSoup(urlopen(self.__url), mode)
        except Exception:
            print('Ooops.. por favor, revise o link informado...')
            self.__bs = None        '''
        self.__bs = BeautifulSoup(urlopen(self.__url), mode)

    @property
    def bs(self):
        return self.__bs

    @property
    def url(self):
        return self.__url

    def downloadPDF(self, pasta, nome_arquivo, url):
        try:
            with open(f'{pasta}/{nome_arquivo}.pdf', 'wb') as f:
                f.write(requests.get(url, stream=True).content)
            print('Arquivo salvo com sucesso!')
        except Exception:
            return None
        
    def run(self):
        self.__funcao(self.__bs, self.__url)