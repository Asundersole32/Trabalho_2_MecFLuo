class Chromosome:
    def __init__(self, binary_value):
        self.binary_value = binary_value
        self.aptitude = None
        self.decoded = None

    def get_aptitude(self):
        return self.aptitude
