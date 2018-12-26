import copy
import time

from unittest import mock

from grifter.utils import get_uuid
from grifter.api import (
    generate_loopbacks,
    update_guest_additional_storage,
    generate_guest_interface_mappings,
)
from grifter.loaders import render_from_template
from grifter.constants import (
    TEMPLATES_DIR,
    TIMESTAMP_FORMAT)
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
@mock.patch('uuid.uuid5', return_value="688c29aa-e657-5d27-b4bb-d745aad2812e")
@mock.patch('time.strftime', return_value='2018-12-26--17-58-55')
def test_render_vagrantfile_with_additional_storage_interfaces(mock_storage_size, mock_random,
                                                               mock_uuid, mock_time):
    time_now = time.strftime(TIMESTAMP_FORMAT)
    guest_data = copy.deepcopy(mock_guest_data)
    loopbacks = generate_loopbacks(guest_data)
    guest_data['sw01']['provider_config']['additional_storage_volumes'] = mock_additional_storage_volumes
    update_guest_additional_storage(guest_data)

    vagrantfile = render_from_template(
        template_name='guest.j2',
        template_directory=TEMPLATES_DIR,
        custom_filters=custom_filters,
        guests=guest_data,
        loopbacks=loopbacks,
        interface_mappings=generate_guest_interface_mappings(),
        domain_uuid=get_uuid(),
        creation_time=time_now,
    )

    assert mock_vagrantfile_with_additional_storage_volumes == vagrantfile
