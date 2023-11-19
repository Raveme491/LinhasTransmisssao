from math import pi

import matplotlib.pyplot as plt
import numpy as np


class SmithChart:
    def __init__(self):
        ...

    def circle_zero(self):
        theta = np.linspace(0, 2 * pi, 180)
        a = 1
        z_r0 = a * np.exp(1j * theta)
        plt.hlines(y=0, xmin=-1, xmax=1, color='black')
        plt.plot(np.real(z_r0), np.imag(z_r0), 'black')

    def creator_circle(self, x):
        phi = np.arange(1, 360)
        theta = phi * pi / 180
        a = 1 / (1 + x)
        m = x / (x + 1)
        n = 0
        Re = a * np.cos(theta) + m
        Im = a * np.sin(theta) + n
        plt.plot(Re, Im, 'green')
        return Re + Im * 1j

    def creator_circle_im(self, x):
        a = abs(1 / x)
        m = 1
        n = 1 / x
        angle = np.linspace(pi / 2, 3 / 2 * pi, 360)
        Re = a * np.cos(angle) + m
        Im = a * np.sin(angle) + n
        z = np.abs(Re + Im * 1j)
        mask = abs(z) <= 1
        Re_inner = Re[mask]
        Im_inner = Im[mask]

        plt.plot(Re_inner, Im_inner, 'red')
        return Re + Im * 1j

    def z2gamma(self, z):
        return (z - 1) / (z + 1)

    def plot(self):
        rvalues = [0.5, 1, 2, 4]
        ivalues = [0.2, 0.5, 1, 2]
        self.circle_zero()

        for real, imag in zip(rvalues, ivalues):
            z_rr = self.creator_circle(real)
            z_rimg = self.creator_circle_im(imag)
            z_rimg2 = self.creator_circle_im(-imag)

        complexos = [r + i * 1j for r, i in zip(rvalues, ivalues)]

        for z in complexos:
            plt.text(
                self.z2gamma(z.imag * 1j).real,
                self.z2gamma(z.imag * 1j).imag,
                f'{z.imag:.2f}j',
                fontsize=10,
                va='bottom',
                ha='center'
                if self.z2gamma(z.imag * 1j).real >= 0
                else 'right',
            )
            plt.text(
                self.z2gamma(z.imag * 1j).real,
                -self.z2gamma(z.imag * 1j).imag,
                f'-{z.imag:.2f}j',
                fontsize=10,
                va='top',
                ha='center'
                if self.z2gamma(z.imag * 1j).real >= 0
                else 'right',
            )
        plt.text(-1.01, 0, '0', fontsize=10, va='center', ha='right')
        plt.text(1.01, 0, '\u221E', fontsize=15, va='center', ha='left')
        plt.show()

    def impedancia_normalizada(self, zl, z0):
        return zl / z0

    def impedancia_graph(self, zl, z0):
        value = self.z2gamma(self.impedancia_normalizada(zl, z0))
        print(value.real, value.imag)
        plt.plot(value.real, value.imag, '-ro', color='black')
        self.plot()


if __name__ == '__main__':
    SmithChart().impedancia_graph(50 + 100j, 50)
