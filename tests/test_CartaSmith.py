import math

from CartaSmith import CartaSmith


def test_valor_impedancia_normalizada():
    carta = CartaSmith(z0=50, zl=50 + 100j)
    assert carta.impedancia_normalizada() == 1 + 2j


def test_resolucao_ex_2_11():
    carta_a = CartaSmith(z0=50, zl=0)
    assert carta_a.impedancia_normalizada() == 0

    carta_b = CartaSmith(z0=50, zl=math.inf)
    assert carta_b.impedancia_normalizada() == math.inf


def test_resolucao_ex_2_12():
    carta = CartaSmith(z0=50, zl=100 - 100j)
    """(A)"""
    assert round(carta.tau_l()[0], 2) == 0.62
    """(B)"""
    assert round(carta.rote(), 1) == 4.3
    """(C)"""
