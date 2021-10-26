import csv, os, math
from haversine import haversine, Unit
import numpy as np
from numpy import ma

os.system('cls') # Limpando o terminal


def get_data(diretorio): #Função para a aquisição e tratamento dos dados
    aux = list()
    with open(diretorio) as arq:
        reader = csv.reader(arq)
        for line in reader:
            aux.append(line) #Cada linha do arquivo é uma lista, então se colocarmos essa lista em outra lista, teremos uma matriz, nesse caso a matriz se chama aux
    
    del aux[len(aux)-1]  #Remove a ultima linha em branco do arquivo, da pra fazer isso manualmente, mas caso o usuario trabalhe com inumeros arquivos, remover a ultima linha de cada arquivo pode ser um trabalho massante 
    del aux[0:11]        #Remove o cabeçalho do arquivo .csv
    
    for i in range(len(aux)):   
        #Removendo os caracteres desenecessários
        aux[i] = str(aux[i]).strip('[')     
        aux[i] = str(aux[i]).strip(']')
        aux[i] = str(aux[i]).strip("'")
        aux[i] = str(aux[i]).split(';')

        del aux[i][9] #Remove a ultima coluna, pois ela fica vazia, ('')
   
        #Remove as outras colunas, deixando somente a de data, precipitação, temperatura max e temperatura min

        del aux[i][1:3]
        del aux[i][3]
        del aux[i][4:6]

    real = list() #Lista/Matriz final

    #Removendo todas as linhas que possuem o valor null
    for i in range(len(aux)):
        condicao = 0
        for j in range(1,4):
            if aux[i][j] == 'null':
                condicao = 1
        
        if condicao == 0:
            real.append(aux[i])

    
    for i in range(len(real)):
        aux.clear()
        for j in range(4):
            aux.append(real[i][j])
        data = aux[0]
        data = str(data).split('-')
        #print(data)
        real[i].insert(0, data[0])
        real[i].insert(1, data[1])
        real[i].insert(2, data[2])
        del real[i][3]

    return real #Retorna a lista com os dados tratados, onde na lista em cada linha temos: [data, precipitação, temperatura max, temperatura min]

def converte_coord(dado):
    dado = list(math.modf(dado))
    grau = int(dado[1])

    resto = dado[0]*60
    if resto < 0:
        resto = resto * (-1)
    
    resto = list(math.modf(resto))
    minuto = int(resto[1])
    segundos = round(resto[0]*60,4)

    return str(grau) + "° " + str(minuto) + "' " + str(segundos) + '" '

def get_coordinates(diretorio): #Função para obter as coordenadas de cada cidade
    aux = list()
    with open(diretorio) as arq:
        reader = csv.reader(arq)
        for i in reader:
            aux.append(i)
        
    #Tratamento de dados
    del aux[10:]

    estacao = str(aux[0]).split(':')
    estacao = estacao[1].strip(']')
    estacao = (estacao.strip("'")).strip()

    latitude = str(aux[2]).split(':')
    latitude = latitude[1].strip(']')
    latitude = (latitude.strip("'")).strip()

    longitude = str(aux[3]).split(':')
    longitude = longitude[1].strip(']')
    longitude = (longitude.strip("'")).strip()

    altitude = str(aux[4]).split(':')
    altitude = altitude[1].strip(']')
    altitude = (altitude.strip("'")).strip()
    '''
    latitude = converte_coord(float(latitude))
    longitude = converte_coord(float(longitude))   
    '''
    aux.clear()
    aux.append(estacao)
    aux.append(latitude)
    aux.append(longitude)
    aux.append(altitude)

 
    return aux #Retorna um 'vetor' com os dados: [nome da estação, latitude, longitude, altitude]

def normaliza_dados(lista): #Função que retorna a matriz com os dados normalizados
    max_min = list()
    aux1 = list()
    for i in range(6): #Colocando os min e os max de cada coluna da lista tratada (anteriormente) em uma outra lista, fica assim: [ano min, ano max, mes min, mes max, precipitação min, precipitação max, temp max min, temp max max, temp min min, temp min max]
        aux1.clear()
        for j in range(len(lista)):
            aux1.append(float(lista[j][i]))
        max_min.append(min(aux1))
        max_min.append(max(aux1))  
    
    dadosn = list()
    
    for i in range(len(lista)):
        aux1.clear()
        for j in range(6):
            if j == 0: #Ano
                menor = max_min[0]
                maior = max_min[1]
            elif j == 1: #Mes
                menor = max_min[2]
                maior = max_min[3]
            elif j == 2: #Dia
                menor = max_min[4]
                maior = max_min[5]
            elif j == 3: #Precipitação
                menor = max_min[6]
                maior = max_min[7]
            elif j == 4: #Temperatura max
                menor = max_min[8]
                maior = max_min[9]
            elif j == 5: #Temperatura min
                menor = max_min[10]
                maior = max_min[11]

            dado = ((float(lista[i][j]) - float(menor)) / (float(maior) - float(menor))) * 0.6 + 0.2
            aux1.append(dado)
        dadosn.append(aux1)
    return dadosn

def haversine_calc(a,b):
    tupla_1 = (float(a[1]), float(a[2]))
    tupla_2 = (float(b[1]), float(b[2]))

    return round(haversine(tupla_1, tupla_2, Unit.KILOMETERS), 4) #Retorna a distancia entre as duas cidades em Km, com 4 casas decimais

target = r'E:\IC\Dados\TriangulacaoBH\BELOHORIZONTE.csv'
neighorA = r'E:\IC\Dados\TriangulacaoBH\FLORESTAL.csv'
neighorB = r'E:\IC\Dados\TriangulacaoBH\IBIRITE.csv'
neighorC = r'E:\IC\Dados\TriangulacaoBH\SETELAGOAS.csv'

"""  ->Obtendo dados de cada cidade<-  """
targetData = get_data(target)
neighorAData = get_data(neighorA)
neighorBData = get_data(neighorB)
neighorCData = get_data(neighorC)

"""  ->Obtendo coordenadas de cada cidade<-  """
coord_target = get_coordinates(target)
coord_neighorA = get_coordinates(neighorA)
coord_neighorB = get_coordinates(neighorB)
coord_neighorC = get_coordinates(neighorC)

#print(normaliza_dados(targetData))
"""  ->Normalizando dados de cada cidade<-  """
target_dadosn = normaliza_dados(targetData)
neighorA_dadosn = normaliza_dados(neighorAData)
neighorB_dadosn = normaliza_dados(neighorBData)
neighorC_dadosn = normaliza_dados(neighorCData)

""""  ->Calculando a distancia entre as cidades<-  """
d1 = haversine_calc(coord_target, coord_neighorA) #Para a maior compreensão coloquei cada distancia em uma variavel, podia colocar direto na tupla 'd' (3 linhas a frente)
d2 = haversine_calc(coord_target, coord_neighorB)
d3 = haversine_calc(coord_target, coord_neighorC)


"""  ->Colocando a distancias entre cada cidade em uma tupla, e a altitude de cada uma em outra tupla<-  """
d = (d1, d2, d3) #Vetor com as distancias (Km) entre a cidade alvo e as 3 cidades vizinhas
h = (float(coord_target[3]), float(coord_neighorA[3]), float(coord_neighorB[3]), float(coord_neighorC[3])) #Alvo, vizinhaA, vizinhaB, vizinhaC

print(d)
print(h)