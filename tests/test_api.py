import pytest

from vagrantfile_builder.api import (
    load_host_data,
    generate_loopbacks,
    update_interfaces,
)

from .mock_data import (
    mock_load_host_data,
    mock_host_interfaces,
)


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


def test_update_interfaces_with_same_interface_count_returns_same_list_of_interfaces():
    assert update_interfaces(2, mock_host_interfaces) == mock_host_interfaces


def test_update_interfaces_with_blackhole_interfaces():
    blackhole_interfaces = [
        {
            'name': f'bh-int3',
            'local_port': 3,
            'remote_host': 'blackhole',
            'remote_port': 666
        },
        {
            'name': f'bh-int4',
            'local_port': 4,
            'remote_host': 'blackhole',
            'remote_port': 666
        }
      ]

    expected_intefaces = mock_host_interfaces + blackhole_interfaces

    assert update_interfaces(4, mock_host_interfaces) == expected_intefaces
