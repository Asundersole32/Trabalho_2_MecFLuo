import random
import copy

def tournament_selection(population, fitness, k=3):
    """Seleciona o melhor indivíduo dentre k candidatos escolhidos aleatoriamente."""
    selected = random.sample(population, k)
    return min(selected, key=fitness)

def crossover_individuals(ind1, ind2):
    """Realiza um crossover de um ponto entre dois indivíduos (listas de floats)."""
    point = random.randint(1, len(ind1) - 1)
    child1 = ind1[:point] + ind2[point:]
    child2 = ind2[:point] + ind1[point:]
    return child1, child2

def mutate_individual(ind, dam, mutation_rate):
    """
    Aplica mutação em cada gene (espessura) do indivíduo.
    A mutação consiste em ajustar a espessura com uma perturbação aleatória
    limitada a 10% do intervalo disponível para aquele nível.
    """
    new_ind = ind.copy()
    for i in range(len(new_ind)):
        if random.random() < mutation_rate:
            lower_bound = dam.minimum_thickness(i + 1)
            upper_bound = dam.thickness_max
            delta = (upper_bound - lower_bound) * 0.1
            new_val = new_ind[i] + random.uniform(-delta, delta)
            new_val = max(new_val, lower_bound)
            new_val = min(new_val, upper_bound)
            new_ind[i] = new_val
    return new_ind

def gera_populacao_inicial_dam(dam, population_size):
    """Gera uma população inicial onde cada indivíduo é uma lista de espessuras válidas."""
    population = []
    for _ in range(population_size):
        individual = []
        for h in range(1, dam.height_max + 1):
            lower_bound = dam.minimum_thickness(h)
            upper_bound = dam.thickness_max
            value = random.uniform(lower_bound, upper_bound)
            individual.append(value)
        population.append(individual)
    return population

def algoritmo_genetico_dam(dam, population_size, generations, mutation_rate=0.1, crossover_rate=0.7, tournament_k=3):
    """
    Executa o algoritmo genético para otimizar o projeto da barragem.
    Cada indivíduo é uma lista de espessuras para cada nível. A função fitness
    é dada pelo método objective_function da classe Dam.
    """
    # Gera população inicial
    population = gera_populacao_inicial_dam(dam, population_size)
    
    # Função de fitness: menor custo é melhor
    def fitness(ind):
        return dam.objective_function(ind)
    
    best_costs = []
    for gen in range(generations):
        new_population = []
        while len(new_population) < population_size:
            parent1 = tournament_selection(population, fitness, k=tournament_k)
            parent2 = tournament_selection(population, fitness, k=tournament_k)
            # Realiza crossover com probabilidade definida
            if random.random() < crossover_rate:
                child1, child2 = crossover_individuals(parent1, parent2)
            else:
                child1, child2 = parent1.copy(), parent2.copy()
            # Aplica mutação
            child1 = mutate_individual(child1, dam, mutation_rate)
            child2 = mutate_individual(child2, dam, mutation_rate)
            new_population.extend([child1, child2])
        population = new_population[:population_size]
        
        # Elitismo simples: preserva o melhor indivíduo da geração
        best_parent = min(population, key=fitness)
        worst_child = max(population, key=fitness)
        if fitness(best_parent) < fitness(worst_child):
            index = population.index(worst_child)
            population[index] = best_parent
        
        best_ind = min(population, key=fitness)
        best_costs.append(fitness(best_ind))
        print(f"Geração {gen+1}: Melhor custo = {fitness(best_ind)}")
        
    return best_ind, best_costs
