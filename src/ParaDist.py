from cmath import acosh, log, pi, sqrt

from scipy.constants import epsilon_0, mu_0


class CabosCoaxias:
    def __init__(
        self,
        a: float,
        b: float,
        frequencia: float,
        mu_r: float,
        e_r: float,
        sigma_c: float,
        sigma_d: float,
    ) -> None:
        self.raio_interno = a
        self.raio_externo = b
        self.frequencia = frequencia
        self.mu_r = mu_r
        self.e_r = e_r
        self.sigma_c = sigma_c
        self.sigma_d = sigma_d

    def resistencia_linha(self):
        return round(
            (
                1000
                * (1 / self.raio_interno + 1 / self.raio_externo)
                * sqrt(pi * self.frequencia * mu_0 * self.mu_r / self.sigma_c)
                / (2 * pi)
            ).real,
            4,
        )

    def indutancia_linha(self):
        return (
            (mu_0 * self.mu_r)
            * log(self.raio_externo / self.raio_interno)
            / (2 * pi)
        ).real

    def capacitancia_linha(self):
        return (
            2
            * pi
            * epsilon_0
            * self.e_r
            / (log(self.raio_externo / self.raio_interno))
        ).real

    def condutancia_linha(self):
        return (
            2
            * pi
            * self.sigma_d
            / (log(self.raio_externo / self.raio_interno))
        ).real

    def impedancia_caracteristica(self):
        return sqrt(
            (
                self.resistencia_linha()
                + 1j * (2 * pi * self.frequencia * self.indutancia_linha())
            )
            / (
                self.condutancia_linha()
                + 2 * pi * self.capacitancia_linha() * self.frequencia * 1j
            )
        )

    def velocidade_propagacao(self):
        return 1 / sqrt(mu_0 * self.mu_r * epsilon_0 * self.e_r)

    def gama(self):
        return sqrt(
            (
                self.resistencia_linha()
                + self.frequencia * 2 * pi * self.indutancia_linha() * 1j
            )
            * (
                self.condutancia_linha()
                + self.frequencia * 2 * pi * self.capacitancia_linha() * 1j
            )
        )


class CaboCondGemeos:
    def __init__(
        self,
        a: float,
        d: float,
        frequencia: float,
        mu_r: float,
        e_r: float,
        sigma_c: float,
        sigma_d: float,
    ) -> None:
        self.raio_interno = a
        self.distancia_entre_fios = d
        self.frequencia = frequencia
        self.mu_r = mu_r
        self.e_r = e_r
        self.sigma_c = sigma_c
        self.sigma_d = sigma_d

    def resistencia_linha(self):
        return (
            sqrt(self.frequencia * mu_0 * self.mu_r / self.sigma_c)
            / self.raio_interno
        )

    def indutancia_linha(self):
        return (
            (mu_0 * self.mu_r)
            * acosh(self.distancia_entre_fios / (2 * self.raio_interno))
            / pi
        ).real

    def capacitancia_linha(self):
        return (
            pi
            * epsilon_0
            * self.e_r
            / (acosh(self.distancia_entre_fios / (2 * self.raio_interno)))
        ).real

    def condutancia_linha(self):
        return (
            pi
            * self.sigma_d
            / (acosh(self.distancia_entre_fios / (2 * self.raio_interno)))
        ).real

    def impedancia_caracteristica(self):
        return sqrt(self.indutancia_linha() / self.capacitancia_linha())

    def velocidade_propagacao(self):
        return 1 / sqrt(mu_0 * self.mu_r * epsilon_0 * self.e_r)


if __name__ == '__main__':
    cabo1 = CabosCoaxias(
        a=0.45,
        b=1.47,
        frequencia=1e9,
        mu_r=1,
        e_r=2.26,
        sigma_c=5.8e7,
        sigma_d=0,
    )
    cabo2 = CabosCoaxias(
        a=0.45,
        b=1.47,
        frequencia=1e9,
        sigma_d=0,
        mu_r=1,
        e_r=2.26,
        sigma_c=5.8e7,
    )
    cabo = CaboCondGemeos(
        frequencia=1e6,
        a=0.4049 / 2,
        d=10,
        e_r=1,
        mu_r=1,
        sigma_d=0,
        sigma_c=5.8e7,
    )

    cabo3 = CabosCoaxias(
        a=0.45,
        b=1.47,
        frequencia=1e9,
        sigma_d=0,
        mu_r=1,
        e_r=2.26,
        sigma_c=5.8e7,
    )
    print(cabo3.gama())
