import cmath


class CasadorQuartoOnda:
    def __init__(self, z0, rl) -> None:
        self.z0 = z0
        self.rl = rl

    def calculo_zs(self):
        """
        Retorna o valor de Zs que casa as impedâncias da carga e rede
        *Puramente resistivas
        """
        return round(cmath.sqrt(self.z0 * self.rl).real, 2)


if __name__ == '__main__':
    casador = CasadorQuartoOnda(z0=50, rl=170)
    print(casador.calculo_zs())
