import pytest

from vagrantfile_builder.custom_filters import explode_port


def test_answer():
    assert explode_port(10) == 10010