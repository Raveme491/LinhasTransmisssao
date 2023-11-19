import cmath

import numpy as np

from SmithChart import SmithChart


class CasamentoCapacitorIndutor:
    def __init__(self, zl, z0, frequencia=None, comprimento=1) -> None:
        self.carta = SmithChart(zl, z0, comprimento)
        self.frequencia = frequencia
        self.z0 = z0

    def calculo_carac_casamento(self):
        zl_norm = self.carta.impedancia_normalizada()
        tau = self.carta.z2gamma(zl_norm)
        fase = self.carta.fase_tau(zl_norm)
        lambda_inicial = (
            (180 - fase) * 0.5 / 360
            if fase < 180
            else (180 - fase) * 0.5 / 360 + 0.5
        )

        circulo_real_1 = (
            self.carta.creator_circle_re(1)[0]
            + self.carta.creator_circle_re(1)[1] * 1j
        )

        restricao = np.isclose(abs(circulo_real_1), abs(tau), atol=1e-2)

        tau_coordenada = circulo_real_1[restricao][0]
        tau_coordenada = np.append(tau_coordenada, tau_coordenada.conjugate())

        z_in_normalizada = (tau_coordenada + 1) / (-tau_coordenada + 1)

        angle_tau = (
            np.arctan(tau_coordenada.imag / tau_coordenada.real)
            * 180
            / cmath.pi
        )
        lambda_final = (180 - np.round(angle_tau.real, 1)) * 0.5 / 360

        distancia = np.round(lambda_final - lambda_inicial, 3)
        distancia[distancia < 0] += 0.5

        return lambda_inicial, lambda_final, distancia, z_in_normalizada

    def capacitancia_necessaria(self, reatancia):
        return 1 / (2 * cmath.pi * abs(reatancia) * self.frequencia)

    def indutancia_necessaria(self, reatancia):
        return abs(reatancia) / (2 * cmath.pi * self.frequencia)

    def casamento_impedancia(self):
        (
            lambda_inicial,
            lambda_final,
            distancia,
            z_in_normalizada,
        ) = self.calculo_carac_casamento()

        reatancia_corretivas = np.imag(z_in_normalizada) * self.z0 * 1j
        valor_cap_ind = []
        if z_in_normalizada[0] > 0 and self.frequencia is not None:
            valor_cap_ind.append(
                self.capacitancia_necessaria(z_in_normalizada[0].imag)
            )
            valor_cap_ind.append(
                self.indutancia_necessaria(z_in_normalizada[1].imag)
            )
        elif z_in_normalizada[0] < 0 and self.frequencia is not None:
            valor_cap_ind.append(
                self.capacitancia_necessaria(z_in_normalizada[1].imag)
            )
            valor_cap_ind.append(
                self.indutancia_necessaria(z_in_normalizada[0].imag)
            )
        return (
            round(lambda_inicial, 3),
            lambda_final,
            distancia,
            reatancia_corretivas,
            valor_cap_ind,
        )


if __name__ == '__main__':
    transformador = CasamentoCapacitorIndutor(
        z0=100, zl=35 - 50j, comprimento=0.419, frequencia=1e9
    )
    print(transformador.casamento_impedancia())
