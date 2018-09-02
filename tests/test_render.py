import copy

from unittest import mock

from grifter.api import generate_loopbacks, update_guest_additional_storage
from grifter.loaders import render_from_template
from grifter.constants import TEMPLATES_DIR
from grifter.custom_filters import (
    explode_port,
)

from tests.mock_data import (
    mock_guest_data,
    mock_additional_storage_volumes,
    mock_vagrantfile_with_additional_storage_volumes,
)

custom_filters = [
    explode_port,
]


@mock.patch('os.path.getsize', return_value='10000')
@mock.patch('random.randint', return_value=255)
def test_render_vagrantfile_with_additional_storage_interfaces(mock_storage_size, mock_random):
    guest_data = copy.deepcopy(mock_guest_data)
    guest_data['guests'].pop(1)
    guest_data['guests'][0]['provider_config']['additional_storage_volumes'] = mock_additional_storage_volumes
    update_guest_additional_storage(guest_data['guests'])

    loopbacks = generate_loopbacks(mock_guest_data['guests'])

    vagrantfile = render_from_template(
        template_name='guest.j2',
        template_directory=TEMPLATES_DIR,
        custom_filters=custom_filters,
        guests=guest_data['guests'],
        loopbacks=loopbacks
    )

    assert mock_vagrantfile_with_additional_storage_volumes == vagrantfile
