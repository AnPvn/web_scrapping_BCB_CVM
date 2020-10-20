class SiteManager():
    def __init__(self):
        self.__sites = []
    
    def getListaDeSites(self):
        return [i for i in self.__sites] # defendendo a lista

    def adicionarSite(self, url):
        if url[0:4] != 'http':
            url = 'https://{}'.format(url)
        if (url in self.__sites) == False:
            self.__sites.append(url)
    
    def removerSite(self, url):
        if url[0:4] != 'http':
            url = 'https://{}'.format(url)
        self.__sites.remove(url)