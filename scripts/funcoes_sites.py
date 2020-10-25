import requests
from scraping import Scraping
from random import randint
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.keys import Keys

def cvm_gov(bs, url):
    '''endereco_principal = 'http://cvm.gov.br'
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
    '''
    from os import listdir
    from os.path import isfile, join
    from PIL import Image
    from pdf2image import convert_from_path
    import pytesseract
    path = './pdfs/'
    files = [f for f in listdir(path) if isfile(join(path, f))]
    for f in files:
        print(path+f)
        doc = convert_from_path(path+f)
        for page_number, page_data in enumerate(doc):
            txt = pytesseract.image_to_string(Image.fromarray(page_data), lang='por').encode("utf-8")
            print(txt)


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
            #paragrafos = pagina.find_elements_by_tag_name('p')
            #for p in paragrafos:
            #    print(p.get_attribute('textContent'))
            print(pagina.page_source)
            pagina.quit()
    driver.quit()

def susep_gov(bs, url):
    #print(bs.prettify())
    driver = webdriver.PhantomJS()
    driver.get(url)
    print(driver.page_source)