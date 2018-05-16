import yaml

from .constants import BASE_DIR


DEFAULTS_FILE = f'{BASE_DIR}/defaults.yml'


def defaults(defaults_file=DEFAULTS_FILE):
    """
    Load guest absolute defaults
    :param defaults_file: File location
    :return: Dict of guest default values.
    """
    with open(defaults_file, 'r') as f:
        return yaml.load(f)
