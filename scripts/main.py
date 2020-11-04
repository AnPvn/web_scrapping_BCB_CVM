# main.py

from SiteManager import SiteManager
from scraping import Scraping
from funcoes_sites import cvm_gov, bcb_gov, susep_gov
from threading import Thread

sm = SiteManager()

def add(url, funcao):
    try:
        sm.adicionarSite(url)
        return Scraping(url, funcao)
    except Exception:
        add(url, funcao)

CVM = add('http://www.cvm.gov.br/legislacao/index.html?numero=&lastNameShow=&lastName=&filtro=todos&dataInicio=&dataFim=&buscado=false&contCategoriasCheck=7', cvm_gov)
BCB = add('https://www.bcb.gov.br/estabilidadefinanceira/buscanormas?dataInicioBusca=17%2F10%2F2020&dataFimBusca=20%2F10%2F2020&tipoDocumento=Todos', bcb_gov)
SUSEP = add('https://www2.susep.gov.br/safe/bnportal/internet/pt-BR/news', susep_gov)

# problema a concertar: falhas ligadas a conecção com a internet

if __name__ == '__main__':
    #print(sm.getListaDeSites())
    #CVM.run()
    #BCB.run()
    #SUSEP.run()
    
    #Thread(target=CVM.run).start()
    Thread(target=BCB.run).start()
