import pytest

from vagrantfile_builder.constants import (
    BASE_DIR,
)

from vagrantfile_builder.constants import TEMPLATES_DIR

from vagrantfile_builder.custom_filters import (
    explode_port,
)

from vagrantfile_builder.loaders import (
    render_from_template,
    load_data
)

from vagrantfile_builder.api import generate_loopbacks

from .mock_data import (
    mock_vagrantfile,
    mock_guest_data,
)

custom_filters = [
    explode_port,
]


def test_render_from_template():
    loopbacks = generate_loopbacks(mock_guest_data['guests'])
    vagrantfile = render_from_template(
        template_name='guest.j2',
        template_directory=TEMPLATES_DIR,
        custom_filters=custom_filters,
        guests=mock_guest_data['guests'],
        loopbacks=loopbacks
    )
    assert vagrantfile == mock_vagrantfile


def test_load_data_with_invalid_data_type_raises_attribute_error():
    with pytest.raises(AttributeError):
        load_data('blah', data_type='invalid')


def test_load_json_data():
    data = load_data(f'{BASE_DIR}/../tests/mock_json_data.json', data_type='json')
    assert {'some': 'data'} == data
