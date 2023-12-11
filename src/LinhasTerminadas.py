from cmath import exp, inf, pi, tan, tanh


class LTTerminadas:
    def __init__(self, z0, zl, z_s=0, gama=0, comprimento=1, vss=0) -> None:
        self.z0 = z0
        self.zl = zl
        self.gama = gama
        self.comprimento = comprimento
        self.z_s = z_s
        self.vss = vss

    def tau_l(self):
        return (self.zl - self.z0) / (self.zl + self.z0)

    def rote(self):
        return (1 + abs(self.tau_l())) / (1 - abs(self.tau_l()))

    def z_in(self):
        if self.zl == inf:
            return -self.z0 * 1j / tan(2 * pi * self.comprimento)
        if self.gama.real:
            return (
                self.z0
                * (self.zl + self.z0 * tanh(self.gama * self.comprimento))
                / (self.z0 + self.zl * tanh(self.gama * self.comprimento))
            )
        return (
            self.z0
            * (self.zl + self.z0 * 1j * tan(2 * pi * self.comprimento))
            / (self.z0 + self.zl * 1j * tan(2 * pi * self.comprimento))
        )

    def v_in(self):
        return self.vss * self.z_in() / (self.z_in() + self.z_s)

    def v0_mais(self, z):
        if self.gama:
            return self.v_in() / (
                exp(complex(self.gama * z)) + exp(-self.gama * z)
            )
        return self.v_in() / (
            exp(2j * pi * z) + self.tau_l() * exp(-2j * pi * z)
        )

    def vl(self):
        return self.v0_mais(self.comprimento) * (1 + self.tau_l())
    
    def linha_t(self, z):
        print(f'tau: {self.tau_l()}\nROTE: {self.rote()}\nZin: {self.z_in()}\nVin: {self.v_in()}\nV0+: {self.v0_mais(z)}\nVl: {self.vl()}')


if __name__ == '__main__':
    lt = LTTerminadas(
        z0=50,
        zl=100,
        gama=0,
        comprimento=0.25,
        vss=10 * exp(pi / 6 * 1j),
        z_s=25,
    )
    lt2 = LTTerminadas(z0=50, zl=50 - 25j, comprimento=0.125)
    #print(lt2.z_in())
    lt.linha_t(.25)
