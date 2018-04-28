import pytest

from vagrantfile_builder.custom_filters import explode_port


def test_port_explosion():
    assert explode_port(10) == 10010


def test_blackhole_port_expolosion():
    assert explode_port(666) == 10666


def test_port_explosion_non_int_raises_exception():
    with pytest.raises(AttributeError):
        explode_port('1')


def test_port_explosion_less_than_1_raises_exception():
    with pytest.raises(AttributeError):
        explode_port(0)


def test_port_explosion_greater_than_999_raises_exception():
    with pytest.raises(AttributeError):
        explode_port(100)
