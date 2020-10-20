# main.py

from SiteManager import SiteManager
from scraping import Scraping
from funcoes_sites import *

sm = SiteManager()

def add(url, funcao):
    sm.adicionarSite(url)
    return Scraping(url, funcao)

CVM = add('http://www.cvm.gov.br/legislacao/index.html?numero=&lastNameShow=&lastName=&filtro=todos&dataInicio=&dataFim=&buscado=false&contCategoriasCheck=7', cvm_gov)
BCB = add('https://www.bcb.gov.br/estabilidadefinanceira/buscanormas?conteudo=9l7qrtaf4fwn65', bcb_gov)
SUSEP = add('https://www2.susep.gov.br/safe/bnportal/internet/pt-BR/news', susep_gov)

if __name__ == '__main__':
    print(sm.getListaDeSites())
    CVM.run()
