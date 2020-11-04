from nltk import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from string import punctuation
from heapq import nlargest

class InterpretadorDeTextos():
    def __init__(self, lang='portuguese'):
        self.lang = lang

    def downloadDependenciasNltk():
        from nltk import download
        download('stopwords')
        download('punkt')

    def resumir(self, texto, porcentagem=30):
        try:
            frases = sent_tokenize(texto) # separar o texto em frases
            palavras = word_tokenize(texto) # separar as frases em palavras
            # clean:
            stops = stopwords.words(self.lang)
            stops.extend(list(punctuation))
            words_minusculo = [w.lower() for w in palavras if w not in stops]
            # analiza a frequencia das palavras:
            freq_palavras = {}
            for w in words_minusculo:
                if w not in freq_palavras.keys():
                    freq_palavras[w] = 1
                    continue
                freq_palavras[w] += 1
            max_freq = max(freq_palavras.values())
            for w in freq_palavras.keys():
                freq_palavras[w] = freq_palavras[w]/max_freq
            # analiza frequencias nas frases -> média ponderada
            pesos_frases = {}
            for f in frases:
                for p in freq_palavras.keys():
                    if p in f.lower() and f in pesos_frases:
                        pesos_frases[f] += freq_palavras[p]
                        continue
                    pesos_frases[f] = freq_palavras[p]
            # obtem os X por cento maiores candidatos
            r = nlargest(int(len(pesos_frases)*(porcentagem/100)), pesos_frases, key=pesos_frases.get)
            resumo = ''
            for a in r:
                resumo+=a
            return resumo
        except Exception:
            return "Houve um erro ao resumir esse texto..."

if __name__ == "__main__":
    interpretador = InterpretadorDeTextos()
    InterpretadorDeTextos.downloadDependenciasNltk()
    print(interpretador.resumir("O território que atualmente forma o Brasil foi oficialmente descoberto pelos portugueses em 22 de abril de 1500, em expedição liderada por Pedro Álvares Cabral. Segundo alguns historiadores como Antonio de Herrera e Pietro d'Anghiera, o encontro do território teria sido três meses antes, em 26 de janeiro, pelo navegador espanhol Vicente Yáñez Pinzón, durante uma expedição sob seu comando. A região, então habitada por indígenas ameríndios divididos entre milhares de grupos étnicos e linguísticos diferentes, cabia a Portugal pelo Tratado de Tordesilhas, e tornou-se uma colônia do Império Português.[15] O vínculo colonial foi rompido, de fato, quando em 1808 a capital do reino foi transferida de Lisboa para a cidade do Rio de Janeiro, depois de tropas francesas comandadas por Napoleão Bonaparte invadirem o território português.[16] Em 1815, o Brasil se torna parte de um reino unido com Portugal. Dom Pedro I, o primeiro imperador, proclamou a independência política do país em 1822. Inicialmente independente como um império, período no qual foi uma monarquia constitucional parlamentarista, o Brasil tornou-se uma república em 1889, em razão de um golpe militar chefiado pelo marechal Deodoro da Fonseca (o primeiro presidente), embora uma legislatura bicameral, agora chamada de Congresso Nacional, já existisse desde a ratificação da primeira Constituição, em 1824.[16] Desde o início do período republicano, a governança democrática foi interrompida por longos períodos de regimes autoritários, até um governo civil e eleito democraticamente assumir o poder em 1985, com o fim da ditadura militar."))