from src.transitorios import TransitoriosDegrau


def test_valor_tau_l():
    """
    Verificação do resultado do cálculo do coeficiente de reflexão da carga
    """
    td = TransitoriosDegrau(
        z0=75, zl=125, zs=25, vs=4, up=3 * 10e7, comprimento=6 * 10e-2
    )
    assert td.calculo_tau_l() == 0.25


def test_valor_tau_s():
    """
    Verificação do resultado do cálculo do coeficiente de reflexão da fonte
    """
    td = TransitoriosDegrau(
        z0=75, zl=125, zs=25, vs=4, up=3 * 10e7, comprimento=6 * 10e-2
    )
    assert td.calculo_tau_s() == -0.5


def test_valor_tempo_de_transicao_da_onda():
    """
    Verificação do resultado do cálculo do tempo de viagem da onda
    """
    td = TransitoriosDegrau(
        z0=75, zl=125, zs=25, vs=4, up=0.1, comprimento=6e-2
    )
    assert td.calculo_tempo_transito() == 2e-9


def test_valor_tensao_em_regime_permanente():
    """
    Verificação do resultado do cálculo da tensão resultante
    em regime permanente
    """
    td = TransitoriosDegrau(
        z0=75, zl=125, zs=25, vs=4, up=3 * 10e7, comprimento=6 * 10e-2
    )
    assert round(td.calculo_tensao_final(), 2) == 3.33


def test_valores_medidos_no_meio_da_linha():
    """
    Verificação do resultado do cálculo das tensões em cada instante
    de ciclo de tempo definido
    """
    td = TransitoriosDegrau(
        z0=75, zl=125, zs=25, vs=4, up=3 * 10e7, comprimento=6 * 10e-2
    )
    assert td.tensoes_meio_linha()[1:] == [3.75, 3.375, 3.28125]
