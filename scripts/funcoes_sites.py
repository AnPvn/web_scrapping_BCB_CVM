import requests
from scraping import Scraping
from random import randint

def cvm_gov(bs):
    links_de_legislacao = []
    links_audiencias_publicas = []
    links_a_descobrir = []
    for a in bs.find_all('a'):
        if '/legislacao/' in a['href']:
            links_de_legislacao.append(a['href'])
        elif '/audiencias_publicas/' in a['href']:
            links_audiencias_publicas.append(a['href'])
        else:
            links_a_descobrir.append(a['href'])
    
    for link in links_de_legislacao:
        #Scraping(link, lambda a: a).downloadPDF('./', f'{randint(0, 10000)}', 
        pass

def bcb_gov(bs):
    pass

def susep_gov(bs):
    pass