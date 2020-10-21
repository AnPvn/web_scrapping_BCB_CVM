import requests
from scraping import Scraping
from random import randint
from time import sleep
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.keys import Keys

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

def bcb_gov(bs, url): # uso do selenium é necessário uma vez que as informações desejadas do site são exibidas após o carregamento do javascript (usam angular js, as informações necessárias estão na tag <app-root>)
    driver = webdriver.PhantomJS()
    driver.get(url)
    i=0
    links = driver.find_elements_by_tag_name('a')
    for link in links:
        href = link.get_attribute('href')
        if href != None and 'estabilidadefinanceira/exibenormativo?' in href:
            i+=1
            print(f'{i} - {href}')
            pagina = webdriver.PhantomJS()
            pagina.get(url)
            print(pagina.page_source) # aqui fica o html das páginas acessadas
            print('\n\n\n')
            pagina.quit()
    driver.quit()

def susep_gov(bs, url):
    pass