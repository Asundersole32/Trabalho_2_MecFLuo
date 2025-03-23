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
        for h in range(1, self.height_max + 1):
            height_thickness = individual[h - 1]
            if height_thickness < self.minimum_thickness(h):
                return float('inf')

            volume = height_thickness * 1
            total_cost += volume * self.material_cost
        return total_cost

    def checks_stability(self, individual):
        for h in range(1, self.height_max + 1):
            height_thickness = individual[h - 1]
            if height_thickness < self.minimum_thickness(h):
                return False
        return True
