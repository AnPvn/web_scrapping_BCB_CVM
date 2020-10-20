import requests

def cvm_gov(bs, url):
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
    print('\n\n')
    print('***** LEGISLACAO *****')
    print(links_de_legislacao)
    print('\n\n\n\n')
    print('***** AUDIENCIAS PÚBLICAS *****')
    print(links_audiencias_publicas)
    print('\n\n\n\n')
    print('***** A DESCOBRIR *****')
    for l in links_a_descobrir:
        print(f'{l}\n')


def bcb_gov(bs, url):
    pass

def susep_gov(bs, url):
    pass