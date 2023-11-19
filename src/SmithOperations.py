from SmithChart import SmithChart


class OperacoesSmith:
    def impedancia_graph(self):
        zl_norm = self.impedancia_normalizada()
        tau = self.z2gamma(zl_norm)
        plt.plot(tau.real, tau.imag, '-ro')
        fase_normal = self.fase_tau(zl_norm)
        z_in = self.impedancia_in(self.comprimento, fase_normal, tau, self.z0)
        max_voltage, min_voltage = self.max_min_tensao(fase_normal)
        self.plot(zl_norm, tau, fase_normal, z_in, max_voltage, min_voltage)

    def impedancia_in(self, comprimento, fase, tau, z0):
        lambda_inicio = (
            (180 - fase) * 0.5 / 360
            if fase < 180
            else (180 - fase) * 0.5 / 360 + 0.5
        )
        lambda_fim = lambda_inicio + comprimento

        angulo_fim = 180 - lambda_fim * 360 / 0.5
        tau_l_final = abs(tau) * cmath.exp((angulo_fim) * 1j * cmath.pi / 180)
        z_in_normalizada = (tau_l_final + 1) / (-tau_l_final + 1)
        z_in = z_in_normalizada * z0
        return z_in

    def max_min_tensao(self, fase):
        lambda_atual = (180 - fase) * 0.5 / 360
        max_voltage = 0.25 - lambda_atual
        min_voltage = 0.5 - lambda_atual

        return max_voltage, min_voltage
