import pytest

from grifter.custom_filters import explode_port

test_ports = [
    (0, 10000),
    (10, 10010),
]


@pytest.mark.parametrize("a,expected", test_ports)
def test_port_explosion(a, expected):
    assert explode_port(a) == expected


def test_blackhole_port_expolosion():
    assert explode_port(666) == 10666


def test_port_explosion_non_int_raises_exception():
    with pytest.raises(AttributeError):
        explode_port('1')


def test_port_explosion_greater_than_999_raises_exception():
    with pytest.raises(AttributeError):
        explode_port(100)
