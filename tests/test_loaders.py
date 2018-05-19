import pytest

from vagrantfile_builder.loaders import load_data


# mock file loader

def test_load_data_with_invalid_data_type_raises_attribute_error():
    with pytest.raises(AttributeError):
        load_data('blah', data_type='invalid')
