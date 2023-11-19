import cmath

import matplotlib.pyplot as plt
import numpy as np


class SmithChart:
    def __init__(self, zl, z0, comprimento=0.125) -> None:
        self.zl = zl
        self.z0 = z0
        self.comprimento = comprimento

    def circle_zero(self):
        theta = np.linspace(0, 2 * cmath.pi, 180)
        a = 1
        z_r0 = a * np.exp(1j * theta)
        plt.hlines(y=0, xmin=-1, xmax=1, color='black')
        plt.plot(np.real(z_r0), np.imag(z_r0), 'black')

    def creator_circle_re(self, x):
        phi = np.arange(1, 360)
        theta = phi * cmath.pi / 180
        a = 1 / (1 + x)
        m = x / (x + 1)
        n = 0
        Re = a * np.cos(theta) + m
        Im = a * np.sin(theta) + n
        return Re, Im

    def creator_circle_im(self, x):
        try:
            a = abs(1 / x)
            m = 1
            n = 1 / x
            angle = np.linspace(cmath.pi / 2, 3 / 2 * cmath.pi, 540)
            Re = a * np.cos(angle) + m
            Im = a * np.sin(angle) + n
            z = np.abs(Re + Im * 1j)
            mask = abs(z) <= 1
            Re_inner = Re[mask]
            Im_inner = Im[mask]

            return Re_inner, Im_inner
        except ZeroDivisionError:
            ...

    def creator_circle_tau_l(self, raio):
        phi = np.arange(1, 360)
        theta = phi * cmath.pi / 180
        tau_l_circle = raio * np.exp(1j * theta)
        return tau_l_circle

    def plot_geral(self, impedancia_normalizada, tau):
        self.circle_zero()

        Re, Im = self.creator_circle_re(impedancia_normalizada.real)
        Re_inner, Im_inner = self.creator_circle_im(
            impedancia_normalizada.imag
        )

        tau_l_circle = self.creator_circle_tau_l(tau)

        plt.plot(Re, Im, 'black')
        plt.plot(Re_inner, Im_inner, 'black')
        plt.plot(np.real(tau_l_circle), np.imag(tau_l_circle), color='black')
        plt.plot([0, np.real(tau)], [0, np.imag(tau)], marker='o')

    def plot_caracteristicas_da_linhas(
        self,
        impedancia_normalizada,
        tau,
        theta_tauL,
        z_in,
        max_voltage,
        min_voltage,
    ):
        self.plot_geral(impedancia_normalizada, tau)
        rote = self.ROTE(tau)
        angulo = (
            'j' + str(round(theta_tauL, 3))
            if theta_tauL > 0
            else '-j' + str(abs(round(theta_tauL, 3)))
        )
        plt.gca().get_yaxis().get_major_formatter().set_powerlimits((0, 0))
        plt.text(
            x=-1,
            y=1,
            s=f'zl:{impedancia_normalizada:.3f}\n\u0393:{abs(tau):.3f}$e^{{{angulo}}}$ \nROTE:{rote:.3f}\nZin:{z_in:.2f}\nMaxV:{max_voltage:.3f}\u03BB\nMinV:{min_voltage:.3f}\u03BB',
            fontsize=10,
            va='top',
            ha='left',
        )
        plt.text(-1.01, 0, '0', fontsize=10, va='center', ha='right')
        plt.text(1.01, 0, '\u221E', fontsize=15, va='center', ha='left')
        plt.show()

    def z2gamma(self, z):
        if z == cmath.inf:
            return 1
        return (z - 1) / (z + 1)

    def fase_tau(self, zl_norm):
        if self.zl == cmath.inf:
            return 0
        tau = self.z2gamma(zl_norm)
        if tau:
            if zl_norm.imag >= 1:
                return (cmath.atan(tau.imag / tau.real) * 180 / cmath.pi).real
            if zl_norm.imag > 0 or -1 < zl_norm.imag < 0:
                return (
                    cmath.atan(tau.imag / tau.real) * 180 / cmath.pi
                ).real + 180
            return (
                cmath.atan(tau.imag / tau.real) * 180 / cmath.pi
            ).real + 360

        return tau

    def ROTE(self, tau):
        try:
            return (1 + abs(tau)) / (1 - abs(tau))
        except ZeroDivisionError:
            return cmath.inf

    def impedancia_normalizada(self):
        return self.zl / self.z0

    def impedancia_graph(self):
        zl_norm = self.impedancia_normalizada()
        tau = self.z2gamma(zl_norm)
        plt.plot(tau.real, tau.imag, '-ro')
        fase_normal = self.fase_tau(zl_norm)
        z_in = self.impedancia_in(self.comprimento, fase_normal, tau, self.z0)
        max_voltage, min_voltage = self.max_min_tensao(fase_normal)
        self.plot_caracteristicas_da_linhas(
            zl_norm, tau, fase_normal, z_in, max_voltage, min_voltage
        )

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


if __name__ == '__main__':
    # SmithChart(20-55j, 50, .125).impedancia_graph()
    # SmithChart(20-55j, 50, .125).impedancia_graph()
    tau1 = SmithChart(50 + 100j, 50, 1).z2gamma(1 + 2j)
    tau2 = SmithChart(150 + 100j, 50, 1).z2gamma(3 + 2j)
    SmithChart(50 + 100j, 50, 1).plot_geral(1 + 2j, tau1)
    SmithChart(150 + 100j, 50, 1).plot_geral(3 + 2j, tau2)
    plt.show()
