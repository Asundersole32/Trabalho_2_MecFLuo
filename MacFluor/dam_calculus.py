class Dam:
    def __init__(self, fluid_densid, gravity, material_resistence, thickness_min, thickness_max, height_max, material_cost):
        self.fluid_densid = fluid_densid
        self.gravity = gravity
        self.material_resistence = material_resistence
        self.thickness_min = thickness_min
        self.thickness_max = thickness_max
        self.height_max = height_max
        self.material_cost = material_cost

    def hydrostatic_pressure(self, height):
        return self.fluid_densid * self.gravity * height

    def minimum_thickness(self, height):
        pressure = self.hydrostatic_pressure(height)
        return pressure / self.material_resistence

    def objective_function(self, individual):
        total_cost = 0
        valid = True
        thickness_values = []

        # Calcular o custo total da barragem
        for i in range(1, self.height_max + 1):
            # Cada gene binário representa uma espessura
            thickness = individual[i - 1]
            thickness_values.append(thickness)

            # Verificar se a espessura é suficiente para suportar a pressão
            depth = (i + 1) * self.height_max  # Profundidade da camada (usando height_max como profundidade)
            pressure_at_depth = self.hydrostatic_pressure(depth) / 1000  # Conversão para kPa
            min_thickness_required = pressure_at_depth / self.material_resistence

            if thickness < min_thickness_required:
                valid = False  # Se a espessura for menor que a necessária, a barragem falha
                break

            # Calcular o custo total da barragem (custo proporcional à espessura)
            total_cost += thickness * self.material_cost  # Custo proporcional à espessura (simplificado)

        if not valid:
            return float('inf')  # Penalidade se as restrições de espessura não forem atendidas

        return total_cost  # Função objetivo (custo total)

    def checks_stability(self, individual):
        for h in range(1, self.height_max + 1):
            height_thickness = individual[h - 1]

            # Verifica se a espessura está dentro do intervalo permitido
            if height_thickness < self.thickness_min or height_thickness > self.thickness_max:
                return False

            # Verifica se a espessura é suficiente para suportar a pressão hidrostática
            if height_thickness < self.minimum_thickness(h):
                return False

        return True
