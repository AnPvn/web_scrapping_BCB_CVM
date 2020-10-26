import requests
from scraping import Scraping
from random import randint
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.keys import Keys
from InterpretadorDeTexto import InterpretadorDeTextos

__interpretador = InterpretadorDeTextos()
InterpretadorDeTextos.downloadDependenciasNltk()

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
    for txt in pdfs_para_textos('./pdfs/', 'imagens_temporarias'):
        print('resumindo...')
        print(__interpretador.resumir(txt))



# ainda não consigo obter o texto das tags....
def bcb_gov(bs, url): # uso do selenium é necessário uma vez que as informações desejadas do site são exibidas após o carregamento do javascript (usam angular js, as informações necessárias estão na tag <app-root>)
    driver = webdriver.PhantomJS()
    driver.get(url)
    i=0
    links = driver.find_elements_by_tag_name('a')

    paragrafos = []

    for link in links:
        href = link.get_attribute('href')
        if href != None and 'estabilidadefinanceira/exibenormativo?' in href:
            i+=1
            print(f'{i} - {href}')
            pagina = webdriver.PhantomJS()
            pagina.get(url)
            for p in pagina.find_elements_by_tag_name('p'):
                try:
                    paragrafos.append(p.text)
                except StaleElementReferenceException:
                    pass
                except NoSuchElementException:
                    pass
            #print(pagina.page_source)
            pagina.quit()
    print(paragrafos)
    driver.quit()

def susep_gov(bs, url):
    #print(bs.prettify())
    driver = webdriver.PhantomJS()
    driver.get(url)
    print(driver.page_source)

def pdfs_para_textos(path, path_imagens): # retorna uma lista com os textos dos pdfs
    from os import listdir, remove
    from os.path import isfile, join
    from PIL import Image
    from pdf2image import convert_from_path # poppler needed.... sudo apt-get install -y poppler-utils
    import pytesseract # para usar com portugues: sudo apt-get install tesseract-ocr-por
    files = [f for f in listdir(path) if isfile(join(path, f))]
    textos = []
    for f in files:
        print(path+f)
        nome = f[:-4]
        try:
            imagens = convert_from_path(path+f)
        except Exception:
            print(f"Houve um problema ao tentar ler o arquivo: {path+f}")
            continue
        i=0
        for imagem in imagens:
            imagem.save(f'{path}/{path_imagens}/{nome}({i}).jpg', 'JPEG')
            i+=1
        txt = ""
        for j in range(0, i):
            arquivo = f'{path}/{path_imagens}/{nome}({j}).jpg'
            txt += pytesseract.image_to_string(Image.open(arquivo), lang='por')
            remove(arquivo)
        textos.append(txt)
    return textos