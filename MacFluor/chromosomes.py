class Cromossomo:
    def __init__(self,valor_binario):
        self.valor_binario = valor_binario
        self.aptidao = None
        self.decodificado = None

    def get_aptidao(self):
        return self.aptidao