class Ponto:
    def __init__(self, dimensoes, coord=None):
        a = []
        if coord == None and dimensoes >= 1:
            self.coordenadas = [0 for i in range(0, dimensoes)]
        elif coord != None:
            self.coordenadas = coord
            dimensoes = len(coord)
            del a
        else:
            self.coordenadas = None

class ClassificadorDeAplicacao:
    def __init__(self, numero_de_caracteristicas):
        cardinalidade_do_conjunto_das_partes = 2**numero_de_caracteristicas
        self.pontos_marcantes = [Ponto(numero_de_caracteristicas) for i in range(0, cardinalidade_do_conjunto_das_partes) if i!=0]
        
        # COMO ADAPTAR O CÓDIGO ABAIXO PARA EM VEZ DE a,
        #   TER UM ARRAY CUJA CARDINALIDADE CORRESPONDE AO NUMERO DE COLUNAS A PREENCHER NO ARRAY self.pontos_marcantes
        # depois que conseguir fazer isso, dividir todos os numeros de cada array coordenadas de cada ponto pelo numero correspondente (resto da divisao de 3 por i)
        # ex: input = 3    out = [(1,0,0),(0,1,0),(0,0,1),(1,1,0),(1,0,1),(0,1,1),(1,1,1)]
            
            
        
        
        
        a=0
        for i in range(0, len(self.pontos_marcantes)):
            print(a)
            for _ in range(0, len(self.pontos_marcantes[i].coordenadas)):
                self.pontos_marcantes[i].coordenadas[a] = 1
            a+=1
            if a >= 3:
                a = (a%3) - 1
            
    
    def __str__(self):
        txt = ""
        for p in self.pontos_marcantes:
            txt += f"{p.coordenadas}\n"
        return txt
        

print(ClassificadorDeAplicacao(3))