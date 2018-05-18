from vagrantfile_builder.constants import (
    BASE_DIR,
)

from vagrantfile_builder.utils import (
    get_mac,
)


def test_get_mac_returns_default_oui():
    assert get_mac()[0:8] == '28:b7:ad'


def test_get_mac_returns_custom_oui():
    assert get_mac('00:00:00')[0:8] == '00:00:00'
