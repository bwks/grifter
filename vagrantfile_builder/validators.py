required_keys = ['name', 'vagrant_box']


def validate_required_keys(guest):
    for key in required_keys:
        if not guest.get(key):
            raise AttributeError(f'{key} is a required key')
    if not guest['vagrant_box'].get('name'):
        raise AttributeError('vagrant_box["name"] is a required key')


def validate_required_values(guest):
    if not guest['name']:
        raise ValueError('name is a required value and cannot be empty')
    if not guest['vagrant_box']['name']:
        raise ValueError('vagrant_box["name"] is a required value and cannot be empty')
