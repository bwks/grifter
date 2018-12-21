from grifter.constants import (
    BASE_DIR,
)

from grifter.utils import (
    get_mac,
    remove_duplicates,
)


def test_get_mac_returns_default_oui():
    assert get_mac()[0:8] == '28:b7:ad'


def test_get_mac_returns_custom_oui():
    assert get_mac('00:00:00')[0:8] == '00:00:00'


def test_remote_duplicates():
    data = [(0, 1, 2, 3), (2, 3, 0, 1)]
    expected = [(0, 1, 2, 3)]
    assert remove_duplicates(data) == expected
