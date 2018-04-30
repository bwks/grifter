import pytest

from vagrantfile_builder.api import (
    load_host_data,
    generate_loopbacks,
)

from .mock_data import mock_load_host_data


def test_host_data_matches_dict():
    assert load_host_data('examples/hosts.yml') == mock_load_host_data


def test_generate_loopbacks_host_list_not_list_type_raises_exception():
    with pytest.raises(AttributeError):
        generate_loopbacks(host_list="")


def test_generate_loopbacks_host_list_is_none_raises_exception():
    with pytest.raises(AttributeError):
        generate_loopbacks(host_list=None)


def test_generate_loopbacks_host_list_empty_raises_exception():
    with pytest.raises(ValueError):
        generate_loopbacks(host_list=[])


def test_generate_loopbacks_returned_loopback_dict():
    expected_loopback_dict = {
        'blackhole': '127.6.6.6',
        'sw01': '127.255.1.1',
        'sw02': '127.255.1.2'
    }
    assert generate_loopbacks(mock_load_host_data['hosts']) == expected_loopback_dict
