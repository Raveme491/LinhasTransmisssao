import cmath

import numpy as np

from SmithChart import SmithChart


class TocoSimples:
    def __init__(self, zl, z0, comprimento=1) -> None:
        self.carta = SmithChart(zl, z0, comprimento)

    def calculo_admitancia_normalizada(self):
        return 1 / self.carta.impedancia_normalizada()

    def calculo_yd(self):
        y_norm = self.calculo_admitancia_normalizada()
        tau = self.carta.z2gamma(y_norm)
        fase = self.carta.fase_tau(y_norm)
        lambda_inicial = round((180 - fase) * 0.5 / 360, 3)
        lambda_inicial += 0.5 if lambda_inicial < 0 else 0

        circulo_real_1 = (
            self.carta.creator_circle_re(1)[0]
            + self.carta.creator_circle_re(1)[1] * 1j
        )

        restricao = np.isclose(abs(circulo_real_1), abs(tau), atol=1e-2)
        tau_coordenada = circulo_real_1[restricao][0]
        tau_coordenada_pontos_intersecao = np.append(
            tau_coordenada, tau_coordenada.conjugate()
        )

        yl_corretiva_normalizada = 1 - (
            tau_coordenada_pontos_intersecao + 1
        ) / (-tau_coordenada_pontos_intersecao + 1)
        fases_y_corretivas = list(
            map(self.carta.fase_tau, yl_corretiva_normalizada)
        )

        codg = np.round((180 - np.round(fases_y_corretivas, 1)) * 0.5 / 360, 3)
        codg[codg < 0] += 0.5

        angle_tau = (
            np.arctan(
                tau_coordenada_pontos_intersecao.imag
                / tau_coordenada_pontos_intersecao.real
            )
            * 180
            / cmath.pi
        )
        lambda_final = np.round(
            (180 - np.round(angle_tau.real, 1)) * 0.5 / 360, 3
        )
        distancia_entre_lambdas = []
        for lf in lambda_final:
            d = lf - lambda_inicial
            if d < 0:
                d += 0.5
            distancia_entre_lambdas.append(round(d, 3))
        return (
            y_norm,
            lambda_inicial,
            lambda_final,
            codg,
            distancia_entre_lambdas,
        )

    def calculo_toco_curto(self, codg):
        result = np.array([codg[0] - 0.25, codg[1] - 0.25])
        result[result < 0] += 0.5
        return np.round(result, 3)

    def calculo_toco_aberto(self, codg):
        return [codg[0], codg[1]]

    def executor(self):
        (
            y_norm,
            lambda_inicial,
            lambda_final,
            codg,
            distancia_entre_lambdas,
        ) = self.calculo_yd()
        comprimento_toco_curto = self.calculo_toco_curto(codg)
        comprimento_toco_aberto = codg
        resultados = {
            '\u03BBInicial': lambda_inicial,
            '\u03BBFinais': lambda_final,
            'Distancias': distancia_entre_lambdas,
            'yl norm': y_norm,
            'Comprimentos toco curto': comprimento_toco_curto,
            'Comprimentos toco aberto': comprimento_toco_aberto,
        }
        return resultados

    def print_casamento(self):
        resultados = self.executor()
        for key, value in resultados.items():
            print(key, value)
if __name__ == '__main__':
    toco_simples = TocoSimples(zl=20 - 55j, z0=50)
    results = toco_simples.executor()
    toco_simples.print_casamento()