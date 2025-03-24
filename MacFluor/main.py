from dam_calculus import Dam
from AG import algoritmo_genetico_dam

def main():
    print("=== Otimização do Projeto da Barragem via Algoritmo Genético ===")
    # Criação da instância Dam com parâmetros de exemplo
    dam = Dam(
        fluid_densid=997,
        gravity=9.81,
        material_resistence=2500,
        thickness_min=0.1,  # Este parâmetro pode ser utilizado se desejar fixar um mínimo extra
        thickness_max=10,
        height_max=5,
        material_cost=50
    )

    # Parâmetros do algoritmo genético
    population_size = 100
    generations = 100
    mutation_rate = 0.5
    crossover_rate = 0.7
    tournament_k = 10

    best_individual, best_costs = algoritmo_genetico_dam(
        dam, population_size, generations, mutation_rate, crossover_rate, tournament_k
    )

    print("\nMelhor solução encontrada:")
    for i, espessura in enumerate(best_individual, start=1):
        print(f" Nível {i}: Espessura = {espessura:.4f}")
    print("Custo total:", dam.objective_function(best_individual))

if __name__ == '__main__':
    main()
