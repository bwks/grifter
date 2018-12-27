import time
import pytest
from unittest import mock

from grifter.utils import get_uuid
from grifter.constants import (
    BASE_DIR,
    TIMESTAMP_FORMAT,
)
from grifter.constants import TEMPLATES_DIR
from grifter.custom_filters import (
    explode_port,
)
from grifter.loaders import (
    render_from_template,
    load_data
)
from grifter.api import (
    generate_loopbacks,
    generate_guest_interface_mappings,
)
from .mock_data import (
    mock_vagrantfile,
    mock_guest_data,
)

custom_filters = [
    explode_port,
]

interface_mappings = generate_guest_interface_mappings()


@mock.patch('random.randint', return_value=255)
@mock.patch('uuid.uuid5', return_value="688c29aa-e657-5d27-b4bb-d745aad2812e")
@mock.patch('time.strftime', return_value='2018-12-26--17-58-55')
def test_render_from_template(mock_random, mock_uuid, mock_time):
    time_now = time.strftime(TIMESTAMP_FORMAT)
    loopbacks = generate_loopbacks(mock_guest_data)
    vagrantfile = render_from_template(
        template_name='guest.j2',
        template_directory=TEMPLATES_DIR,
        custom_filters=custom_filters,
        guests=mock_guest_data,
        loopbacks=loopbacks,
        interface_mappings=interface_mappings,
        domain_uuid=get_uuid(),
        creation_time=time_now,
        blackhole_interfaces={},
    )
    assert vagrantfile == mock_vagrantfile


def test_load_data_with_invalid_data_type_raises_attribute_error():
    with pytest.raises(AttributeError):
        load_data('blah', data_type='invalid')


def test_load_json_data():
    data = load_data(f'{BASE_DIR}/../tests/mock_json_data.json', data_type='json')
    assert {'some': 'data'} == data
