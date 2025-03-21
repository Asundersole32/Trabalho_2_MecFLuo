from chromosomes import Cromossomo
import math
import random
import copy

def mutacao(filho):
    enfermeira = ''
    for bit in filho.valor_binario:
        bitM = bit
        taxaMutacao = random.uniform(0, 1)
        if(taxaMutacao <= 0.07):
            bitM = abs(int(bitM)-1)
        enfermeira += str(bitM)

    filho.valor_binario = enfermeira
    filho.decodificado = decodificacao(filho.valor_binario)
    filho.aptidao = calcula_aptidao(filho.decodificado)
    return filho


def crossover(cromossomoA, cromossomoB):
    tamanhoCromossomo = len(cromossomoA.valor_binario)
    pontoCorte = random.randint(1, tamanhoCromossomo-1)

    parteUmA = cromossomoA.valor_binario[:pontoCorte]
    parteDoisA = cromossomoA.valor_binario[pontoCorte:]
    parteUmB = cromossomoB.valor_binario[:pontoCorte]
    parteDoisB = cromossomoB.valor_binario[pontoCorte:]

    valorBinfilhoUm = parteUmA + parteDoisB
    filhoUm = Cromossomo(valorBinfilhoUm)
    filhoUm.decodificado = decodificacao(valorBinfilhoUm)
    filhoUm.aptidao = calcula_aptidao(filhoUm.decodificado)

    valorBinfilhoDois = parteUmB + parteDoisA
    filhoDois = Cromossomo(valorBinfilhoDois)
    filhoDois.decodificado = decodificacao(valorBinfilhoDois)
    filhoDois.aptidao = calcula_aptidao(filhoDois.decodificado)

    return filhoUm, filhoDois

def decodificacao(valor_binario):
    qtd_bits = len(valor_binario)
    valor_decimal = int(valor_binario, 2)
    return -20 + ((20+20) * (valor_decimal / (2**qtd_bits-1)))


def monta_valor_binario():
    # Tamanho do cromosso é 6(potencia) + ~3,3 (precisao)
    tamanho = 10
    cromossomo = ''
    for _ in range(tamanho):
        bit = random.randint(0, 1)
        cromossomo += str(bit)

    return cromossomo


def calcula_aptidao(valor_decodificado):
    return (math.cos(valor_decodificado) * valor_decodificado) + 2

def gera_populacao_inicial(numero_populacao):
    lista_populacao = []

    for _ in range(numero_populacao):
        valor_binario = monta_valor_binario()
        cromossomo = Cromossomo(valor_binario)
        cromossomo.decodificado = decodificacao(valor_binario)
        cromossomo.aptidao = calcula_aptidao(cromossomo.decodificado)
        lista_populacao.append(cromossomo)

    return lista_populacao

def algoritmo_genetico(numero_populacao, geracoes):
    # Lista para armazenar os resultados para o gráfico
    # Guarda a melhor aptidao de Cada nova iteração
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

            # Compara qual cromossomo é o melhor (menor aptidao)
            if cromossomo_1.aptidao < cromossomo_2.aptidao:
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
            filho1 = mutacao(filho1)
            filho2 = mutacao(filho2)

            # Inserção na nova população
            lista_populacao_nova.append(filho1)
            lista_populacao_nova.append(filho2)

        # Ordenação dos filhos em ordem crescente de aptidão
        lista_populacao_nova = sorted(lista_populacao_nova, key=Cromossomo.get_aptidao)

        piorFilho = lista_populacao_nova[-1]

        # Ordenação dos pais em ordem crescente de aptidão
        lista_populacao = sorted(lista_populacao, key=Cromossomo.get_aptidao)
        melhor_pai = lista_populacao[0]

        if (piorFilho.aptidao > melhor_pai.aptidao):
            # Removendo o pior filho
            for i in range(len(lista_populacao_nova)):
                if lista_populacao_nova[i].aptidao == piorFilho.aptidao:
                    del lista_populacao_nova[i]
                    break

            # E mantendo o melhor pai da população anterior para a próxima geração
            lista_populacao_nova.append(melhor_pai)

        lista_populacao_nova = sorted(lista_populacao_nova, key=Cromossomo.get_aptidao)
        lista_melhor_aptidao.append(lista_populacao_nova[0])

        lista_populacao = lista_populacao_nova

    return lista_melhor_aptidao
