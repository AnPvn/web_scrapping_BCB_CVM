import requests
from scraping import Scraping
from random import randint

from time import sleep

def cvm_gov(bs, url):
    endereco_principal = 'http://cvm.gov.br'
    id = 0
    for link_primario in bs.find_all('a'):
        if ('/legislacao/' in link_primario['href']) or ('/audiencias_publicas/' in link_primario['href']):
            scrap = Scraping(endereco_principal+link_primario['href'], None)
            for link_secundario in scrap.bs.find_all('a'): # procurando_link_do_pdf
                try:
                    if link_secundario['title'] == 'download' and '.pdf' in link_secundario['href']:
                        id+=1
                        address = endereco_principal+link_secundario['href']
                        scrap.downloadPDF('./pdfs', f'{id}', address)
                        print(f'{id}    ->    {address}')
                except KeyError:
                    pass

def bcb_gov(bs, url):
    pass

def susep_gov(bs, url):
    pass