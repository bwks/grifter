import pytest

from grifter.utils import (
    get_mac,
    remove_duplicates,
    sort_nicely,
    dict_merge
)


def test_get_mac_returns_default_oui():
    assert get_mac()[0:8] == '28:b7:ad'


def test_get_mac_returns_custom_oui():
    assert get_mac('00:00:00')[0:8] == '00:00:00'


def test_remote_duplicates():
    data = [(0, 1, 2, 3), (2, 3, 0, 1)]
    expected = [(0, 1, 2, 3)]
    assert remove_duplicates(data) == expected


def test_sort_nicely():
    data = [
        'p1r50-ge-0/0/9 <--> p1sw10-swp5',
        'p1r1-ge-0/0/2 <--> p1r2-ge-0/0/1',
        'p1r5-ge-0/0/9 <--> p1sw1-swp5',
        'p1r2-ge-0/0/9 <--> p1sw1-swp2',
    ]
    expected = [
        'p1r1-ge-0/0/2 <--> p1r2-ge-0/0/1',
        'p1r2-ge-0/0/9 <--> p1sw1-swp2',
        'p1r5-ge-0/0/9 <--> p1sw1-swp5',
        'p1r50-ge-0/0/9 <--> p1sw10-swp5',
    ]
    assert expected == sort_nicely(data)


def test_sort_nicely_empty_list_returns_empty_list():
    data = []
    expected = []
    assert expected == sort_nicely(data)


def test_sort_nicely_non_list_type_raises_attribute_error():
    with pytest.raises(AttributeError):
        sort_nicely('')


def test_dict_merge():
    a = {1: {"a": "A"}, 2: {"b": "B", "c": "C"}, 3: [{1: 2}]}
    b = {1: {"a": "A"}, 2: {"b": "D"}, 3: [{4: 5}], 4: {'x': 'y'}, 5: 6}
    expected = {1: {'a': 'A'}, 2: {'b': 'D', 'c': 'C'}, 3: [{4: 5}], 4: {'x': 'y'}, 5: 6}
    assert dict_merge(a, b) == expected
