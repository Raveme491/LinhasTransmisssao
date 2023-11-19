import math

import pytest
from scipy.constants import speed_of_light

from ParaDist import CaboCondGemeos, CabosCoaxias


def test_resistencia_linha_coaxial():
    cabo1 = CabosCoaxias(
        a=0.45,
        b=1.47,
        frequencia=1e9,
        mu_r=1,
        e_r=2.26,
        sigma_c=5.8e7,
        sigma_d=0,
    )
    assert cabo1.resistencia_linha() == 3.8112


def test_indutancia_linha_coaxial():
    cabo = CabosCoaxias(
        a=0.45,
        b=1.47,
        frequencia=1e9,
        mu_r=1,
        e_r=2.26,
        sigma_c=5.8e7,
        sigma_d=0,
    )

    assert cabo.indutancia_linha() == 2.3675401953056645e-07


def test_capacitancia_linha_coaxial():
    cabo = CabosCoaxias(
        a=0.45,
        b=1.47,
        frequencia=1e9,
        mu_r=1,
        e_r=2.26,
        sigma_c=5.8e7,
        sigma_d=0,
    )

    assert cabo.capacitancia_linha() == 1.0621104265376237e-10


def test_condutancia_linha_coaxial():
    cabo = CabosCoaxias(
        a=0.45,
        b=1.47,
        frequencia=1e9,
        mu_r=1,
        e_r=2.26,
        sigma_c=5.8e7,
        sigma_d=0,
    )

    assert cabo.condutancia_linha() == 0.0


def test_impedancia_caracteristica_coaxial():
    cabo = CabosCoaxias(
        a=0.45,
        b=1.47,
        frequencia=1e9,
        sigma_d=0,
        mu_r=1,
        e_r=2.26,
        sigma_c=5.8e7,
    )

    assert (
        round(cabo.impedancia_caracteristica().real, 2) == 47.21
        and round(cabo.impedancia_caracteristica().imag, 2) == -0.06
    )


def test_gama_coaxial():
    cabo = CabosCoaxias(
        a=0.45,
        b=1.47,
        frequencia=1e9,
        sigma_d=0,
        mu_r=1,
        e_r=2.26,
        sigma_c=5.8e7,
    )

    assert (
        round(cabo.gama().real, 2) == 0.04
        and math.floor(cabo.gama().imag) == 31.0
    )


def test_velocidade_propagacao_gemeo():
    cabo = CaboCondGemeos(
        frequencia=1e6,
        a=0.4049 / 2,
        d=10,
        e_r=1,
        mu_r=1,
        sigma_d=0,
        sigma_c=5.8e7,
    )
    assert (
        pytest.approx(cabo.velocidade_propagacao().real, 0.5) == speed_of_light
    )


# def test_resistencia_linha_gemeo():
#     cabo = CaboCondGemeos(
#         frequencia=1e6,
#         a=0.4049 / 2,
#         d=10,
#         e_r=1,
#         mu_r=0.99,
#         sigma_d=0,
#         sigma_c=5.8e7,
#     )
#     assert cabo.resistencia_linha() == 0.41


# def test_impedancia_caracteristica_gemeo():
#     cabo = CaboCondGemeos(
#         frequencia=1e6,
#         a=0.4049 / 2,
#         d=10,
#         e_r=1,
#         mu_r=1,
#         sigma_d=0,
#         sigma_c=5.8e7,
#     )
#     assert cabo.impedancia_caracteristica() == 580
