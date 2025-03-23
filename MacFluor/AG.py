from chromosomes import Chromosome
import math
import random
import copy

def mutation(children):
    nurse = ''
    for bit in children.binary_value:
        bitM = bit
        mutation_factor = random.uniform(0, 1)
        if(mutation_factor <= 0.07):
            bitM = abs(int(bitM)-1)
        nurse += str(bitM)

    children.binary_value = nurse
    children.decoded = decodification(children.binary_value)
    children.aptitude = calculate_fitness(children.decoded)
    return children


def crossover(chromosomeA, chromosomeB):
    chromosome_size = len(chromosomeA.binary_value)
    cut_point = random.randint(1, chromosome_size-1)

    part_oneA = chromosomeA.binary_value[:cut_point]
    part_twoB = chromosomeA.binary_value[cut_point:]
    part_oneB = chromosomeB.binary_value[:cut_point]
    part_twoB = chromosomeB.binary_value[cut_point:]

    valorBinfilhoUm = part_oneA + part_twoB
    filhoUm = Chromosome(valorBinfilhoUm)
    filhoUm.decoded = decodification(valorBinfilhoUm)
    filhoUm.aptitude = calculate_fitness(filhoUm.decoded)

    valorBinfilhoDois = part_oneB + part_twoB
    filhoDois = Chromosome(valorBinfilhoDois)
    filhoDois.decoded = decodification(valorBinfilhoDois)
    filhoDois.aptitude = calculate_fitness(filhoDois.decoded)

    return filhoUm, filhoDois

def decodification(valor_binario):
    qtd_bits = len(valor_binario)
    valor_decimal = int(valor_binario, 2)
    return -20 + ((20+20) * (valor_decimal / (2**qtd_bits-1)))


def build_binary_value():
    # Tamanho do cromosso é 6(potencia) + ~3,3 (precisao)
    tamanho = 10
    cromossomo = ''
    for _ in range(tamanho):
        bit = random.randint(0, 1)
        cromossomo += str(bit)

    return cromossomo


def calculate_fitness(valor_decodificado):
    return (math.cos(valor_decodificado) * valor_decodificado) + 2

def gera_populacao_inicial(numero_populacao):
    lista_populacao = []

    for _ in range(numero_populacao):
        valor_binario = build_binary_value()
        cromossomo = Chromosome(valor_binario)
        cromossomo.decoded = decodification(valor_binario)
        cromossomo.aptitude = calculate_fitness(cromossomo.decoded)
        lista_populacao.append(cromossomo)

    return lista_populacao

def algoritmo_genetico(numero_populacao, geracoes):
    # Lista para armazenar os resultados para o gráfico
    # Guarda a melhor aptitude de Cada nova iteração
    lista_melhor_aptidao = []

    # Definicao da populacao inicial
    lista_populacao = gera_populacao_inicial(numero_populacao)

    for _ in range(geracoes):
        lista_selecionados = []

        for i in range(len(lista_populacao)):
            # Aleatoriamente escolhe dois cromossomos para comparar
            posicao_Aleatoria = random.randint(0, len(lista_populacao)-1)
            cromossomo_1 = copy.deepcopy(lista_populacao[posicao_Aleatoria])

            posicao_Aleatoria = random.randint(0, len(lista_populacao)-1)
            cromossomo_2 = copy.deepcopy(lista_populacao[posicao_Aleatoria])

            # Compara qual cromossomo é o melhor (menor aptitude)
            if cromossomo_1.aptitude < cromossomo_2.aptitude:
                lista_selecionados.append(cromossomo_1)
            else:
                lista_selecionados.append(cromossomo_2)

        lista_populacao_nova = []

        for i in range(0, len(lista_selecionados), 2):
            cromossomoA = lista_selecionados[i]
            cromossomoB = lista_selecionados[i+1]

            # Crossover
            taxaCrossover = random.uniform(0, 1)
            if(taxaCrossover <= 0.6):
                filho1, filho2 = crossover(cromossomoA, cromossomoB)
            else:
                filho1, filho2 = cromossomoA, cromossomoB

            # Mutação
            filho1 = mutation(filho1)
            filho2 = mutation(filho2)

            # Inserção na nova população
            lista_populacao_nova.append(filho1)
            lista_populacao_nova.append(filho2)

        # Ordenação dos filhos em ordem crescente de aptidão
        lista_populacao_nova = sorted(lista_populacao_nova, key=Chromosome.get_aptitude)

        piorFilho = lista_populacao_nova[-1]

        # Ordenação dos pais em ordem crescente de aptidão
        lista_populacao = sorted(lista_populacao, key=Chromosome.get_aptitude)
        melhor_pai = lista_populacao[0]

        if (piorFilho.aptitude > melhor_pai.aptitude):
            # Removendo o pior children
            for i in range(len(lista_populacao_nova)):
                if lista_populacao_nova[i].aptitude == piorFilho.aptitude:
                    del lista_populacao_nova[i]
                    break

            # E mantendo o melhor pai da população anterior para a próxima geração
            lista_populacao_nova.append(melhor_pai)

        lista_populacao_nova = sorted(lista_populacao_nova, key=Chromosome.get_aptitude)
        lista_melhor_aptidao.append(lista_populacao_nova[0])

        lista_populacao = lista_populacao_nova

    return lista_melhor_aptidao
