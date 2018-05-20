import os
from .loaders import load_data

BASE_DIR = os.path.join(os.path.dirname(__file__))

TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')

EXAMPLES_DIR = os.path.join(BASE_DIR, 'examples')
GROUPS_EXAMPLE_FILE = f'{EXAMPLES_DIR}/groups-example.yml'
GUESTS_EXAMPLE_FILE = f'{EXAMPLES_DIR}/guests-example.yml'

GUEST_DEFAULTS_FILE = f'{BASE_DIR}/defaults.yml'
ALL_GUEST_DEFAULTS = load_data(GUEST_DEFAULTS_FILE)

BLACKHOLE_LOOPBACK_MAP = {'blackhole': '127.6.6.6'}
