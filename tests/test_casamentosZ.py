from CasamentoQO import CasadorQuartoOnda


def test_calculo_rs():
    quarto_onda = CasadorQuartoOnda(z0=50, rl=100)
    assert round(quarto_onda.calculo_zs().real, 1) == 70.7


def test_calculo_rs_lista_revisao():
    casador = CasadorQuartoOnda(z0=50, rl=170)
    assert round(casador.calculo_zs().real, 1) == 92.2
