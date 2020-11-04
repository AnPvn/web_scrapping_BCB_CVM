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
    endereco_principal = 'Www.cvm.gov.br' # primeiro W é maiúsculo
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
    for txt in pdfs_para_textos('./pdfs/', 'imagens_temporarias'): # melhorar essa parte do código...
        '''# encontra o título e data
        local_endereco_principal = txt.find(endereco_principal)
        titulo_com_data = txt[local_endereco_principal+2:txt[local_endereco_principal:].find('\n')]
        # a linha acima é necessária para encontrar a quebra de linha após o título e não antes...
        print(titulo_com_data)'''
        # encontra intervavo do conteudo principal
        if txt.find('Atenciosamente') != -1:
            txt = txt[txt.find('Assunto:'):txt.find('Atenciosamente')]
        elif txt.find('Assinado eletronicamente') != -1:
            txt = txt[txt.find('Assunto:'):txt.find('Assinado eletronicamente')]
        else:
            txt = txt[txt.find('Assunto:')]
        '''print('O TEXTO REAL:')
        print(txt)
        print('O RESUMO:')
        print(__interpretador.resumir(txt, porcentagem=35))
        print('\n\n\n')'''



# ainda não consigo obter o texto das tags....
def bcb_gov(bs, url): # uso do selenium é necessário uma vez que as informações desejadas do site são exibidas após o carregamento do javascript (usam angular js, as informações necessárias estão na tag <app-root>)
    driver = webdriver.PhantomJS()
    driver.get(url)
    i=0
    links = driver.find_elements_by_tag_name('a')

    paragrafos = []

    for link in links:
        titulo = link.text
        href="https://www.bcb.gov.br/api/conteudo/app/normativos/exibenormativo?p1="
        prosseguir = False
        if 'Comunicado' in titulo:
            try:
                #print(titulo)
                numero_comunicado = titulo[14:titulo.index(",")].replace(".", "")
                #print(numero_comunicado)
                href=f"https://www.bcb.gov.br/api/conteudo/app/normativos/exibeoutrasnormas?p1=COMUNICADO&p2={numero_comunicado}"
                prosseguir=True
            except ValueError:
                pass
        elif 'Resolução' in titulo:
            try:
                numero_resolucao = titulo[17:]
                numero_resolucao = numero_resolucao[0:numero_resolucao.index(",")]
                #print(titulo)
                #print(numero_resolucao)
                href+=f"Resolução%20BCB&p2={numero_resolucao}"
                prosseguir=True
            except ValueError:
                pass
        elif 'Instrução Normativa' in titulo:
            try:
                numero_inormativa = titulo[27:]
                numero_inormativa = numero_inormativa[0:numero_inormativa.index(",")]
                #print(titulo)
                #print(numero_inormativa)
                href+=f"Instrução%20Normativa%20BCB&p2={numero_inormativa}"
                prosseguir=True
            except ValueError:
                pass
        
        if prosseguir:
            pagina = webdriver.PhantomJS()
            pagina.get(href)
            texto = pagina.find_element_by_tag_name('pre').text
            print(href)
            texto_div = texto[texto.index("<"):]
            print(texto_div)

    '''for link in links:
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
    driver.quit()'''

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