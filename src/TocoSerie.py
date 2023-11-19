import cmath

import numpy as np

from SmithChart import SmithChart


class TocoSerie:
    def __init__(self, zl, z0, comprimento=1) -> None:
        self.carta = SmithChart(zl, z0, comprimento)

    def calculo_carac_casamento(self):
        zl_norm = self.carta.impedancia_normalizada()
        tau = self.carta.z2gamma(zl_norm)
        fase = self.carta.fase_tau(zl_norm)
        lambda_inicial = round((180 - fase) * 0.5 / 360, 3)

        circulo_real_1 = (
            self.carta.creator_circle_re(1)[0]
            + self.carta.creator_circle_re(1)[1] * 1j
        )

        restricao = np.isclose(abs(circulo_real_1), abs(tau), atol=1e-2)

        tau_coordenada = circulo_real_1[restricao][0]
        tau_coordenada = np.append(tau_coordenada, tau_coordenada.conjugate())

        zl_corretiva_normalizada = 1 - (tau_coordenada + 1) / (
            -tau_coordenada + 1
        )
        fases_z_corretivas = list(
            map(self.carta.fase_tau, zl_corretiva_normalizada)
        )

        codg = np.round((180 - np.round(fases_z_corretivas, 1)) * 0.5 / 360, 3)
        codg[codg < 0] += 0.5

        angle_tau = (
            np.arctan(tau_coordenada.imag / tau_coordenada.real)
            * 180
            / cmath.pi
        )
        lambda_final = np.round(
            (180 - np.round(angle_tau.real, 1)) * 0.5 / 360, 3
        )
        distancia_entre_lambdas = [lf - lambda_inicial for lf in lambda_final]
        return (
            zl_norm,
            lambda_inicial,
            lambda_final,
            codg,
            distancia_entre_lambdas,
        )

    def calculo_toco_curto(self, codg):
        return [codg[0], codg[1]]

    def calculo_toco_aberto(self, codg):
        result = np.array([codg[0] - 0.25, codg[1] - 0.25])
        result[result < 0] += 0.5
        return np.round(result, 3)

    def executor(self):
        (
            zl_norm,
            lambda_inicial,
            lambda_final,
            codg,
            distancia_entre_lambdas,
        ) = self.calculo_carac_casamento()
        comprimento_toco_aberto = self.calculo_toco_aberto(codg)
        comprimento_toco_curto = self.calculo_toco_curto(codg)

        resultados = {
            '\u03BBInicial': lambda_inicial,
            '\u03BBFinais': lambda_final,
            'Distancias': distancia_entre_lambdas,
            'Zl norm': zl_norm,
            'Comprimentos toco curto': comprimento_toco_curto,
            'Comprimentos toco aberto': comprimento_toco_aberto,
        }

        return resultados


if __name__ == '__main__':
    toco_simples = TocoSerie(zl=11 + 25j, z0=50)
    results = toco_simples.executor()
    for key, value in results.items():
        print(key, value)
