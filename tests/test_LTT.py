import math
from cmath import atan, exp, pi

from src.LinhasTerminadas import LTTerminadas


def test_tau_l():
    lt = LTTerminadas(
        z0=50,
        zl=150,
        gama=0,
        comprimento=0.25,
        vss=10 * exp(pi / 6 * 1j),
        z_s=25,
    )
    assert lt.tau_l() == 0.5


def test_rote():
    lt = LTTerminadas(
        z0=50,
        zl=150,
        gama=0,
        comprimento=0.25,
        vss=10 * exp(pi / 6 * 1j),
        z_s=25,
    )
    assert lt.rote() == 3


def test_zin():
    lt = LTTerminadas(
        z0=50,
        zl=100,
        gama=0,
        comprimento=0.25,
        vss=10 * exp(pi / 6 * 1j),
        z_s=25,
    )

    assert math.ceil(lt.z_in().real) == 25


def test_vin():
    lt = LTTerminadas(
        z0=50,
        zl=100,
        gama=0,
        comprimento=0.25,
        vss=10 * exp(pi / 6 * 1j),
        z_s=25,
    )
    assert (
        math.ceil(abs(lt.v_in())) == 5
        and math.ceil((atan(lt.v_in().imag / lt.v_in().real) * 180 / pi).real)
        == 30
    )


def test_v0_mais():
    lt = LTTerminadas(
        z0=50,
        zl=100,
        gama=0,
        comprimento=0.25,
        vss=10 * exp(pi / 6 * 1j),
        z_s=25,
    )

    assert (
        round(abs(lt.v0_mais(0.25)), 2) == 7.5
        and math.floor(
            (
                atan(lt.v0_mais(0.25).imag / lt.v0_mais(0.25).real) * 180 / pi
            ).real
        )
        == -60
    )


def test_vl():
    lt = LTTerminadas(
        z0=50,
        zl=100,
        gama=0,
        comprimento=0.25,
        vss=10 * exp(pi / 6 * 1j),
        z_s=25,
    )

    assert (
        math.ceil(abs(lt.vl())) == 10
        and math.ceil((atan(lt.vl().imag / lt.vl().real) * 180 / pi).real)
        == -60
    )
