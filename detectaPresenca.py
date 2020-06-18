import requests
from lxml import html
import csv
import lxml.html

# Muda User-Agent
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10; rv:33.0) Gecko/20100101 Firefox/33.0'}

def main():
    # Cria o arquivo CSV
    headerDoCSV = ['Nome','Partido', 'Estado' 'P_Presenca', 'P_AusenciaJustificada', 'P_AusenciaNaoJustificada', 'C_Presenca', 'C_AusenciaJustificada', 'C_AusenciaNaoJustificada']
    listaDePresenca = open('listaDePresenca.xls', 'w')
    csvwriter = csv.writer(listaDePresenca, delimiter='\t')
    csvwriter.writerow(headerDoCSV)

    with open('deputados.txt') as file:
        deputadoID = file.readlines()
        deputadoID = [x.strip() for x in deputadoID]

    for deputado in deputadoID:
        # Acessa o site da camara
        urlNumeros = 'https://www.camara.leg.br/deputados/' + deputado + '/_atuacao?ano=2019'
        urlNomes = 'https://www.camara.leg.br/deputados/' + deputado + '/'
        try:
            responseNumeros = requests.get(urlNumeros, headers=headers)
            responseNome = requests.get(urlNomes, headers=headers)
            nomeTree = lxml.html.fromstring(responseNome.content)
            numeroTree = lxml.html.fromstring(responseNumeros.content)
        except:
            print("[ERROR] Nao foi possivel buscar informacoes no site do deputado")

        # Busca os campos com os numeros
        nomeDeputado = nomeTree.xpath('//h2[@class="nome-deputado"]/text()')
        nomePartido = nomeTree.xpath('//span[@class="foto-deputado__partido-estado"]/text()')
        presencaEmPlenario = numeroTree.xpath('//dt[@class="list-table__definition-term"]/text()')
        numeroPresencaEmPlenario = numeroTree.xpath('//dd[@class="list-table__definition-description"]/text()')
        limpoNumeroPresencaEmPlenario = []
        limpoNumeroPresencaEmPlenario.append(nomeDeputado[0])
        limpoNumeroPresencaEmPlenario.append(nomePartido[0].split(' - ')[0])
        limpoNumeroPresencaEmPlenario.append(nomePartido[0].split(' - ')[1])

        for numero in numeroPresencaEmPlenario:
            limpoNumeroPresencaEmPlenario.append(numero.split('\n')[1].split(' ')[-1])

        # Escreve dados no CSV
        csvwriter.writerow(limpoNumeroPresencaEmPlenario)
        print(limpoNumeroPresencaEmPlenario)
    listaDePresenca.close()

if __name__ == '__main__':
    main()
