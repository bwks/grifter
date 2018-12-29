import os

from .loaders import load_data

BASE_DIR = os.path.join(os.path.dirname(__file__))

TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')

VAGRANTFILE_BACKUP_DIR = 'vagrantfile-backup'

EXAMPLES_DIR = os.path.join(BASE_DIR, 'examples')
GROUPS_EXAMPLE_FILE = f'{EXAMPLES_DIR}/groups-example.yml'
GUESTS_EXAMPLE_FILE = f'{EXAMPLES_DIR}/guests-example.yml'

DEFAULT_CONFIG_FILE = f'{BASE_DIR}/config.yml'
GUEST_DEFAULTS_FILE = f'{BASE_DIR}/defaults.yml'
ALL_GUEST_DEFAULTS = load_data(GUEST_DEFAULTS_FILE)

TESTS_DIR = os.path.join(BASE_DIR, '../tests')

SCHEMAS_DIR = os.path.join(BASE_DIR, 'schemas')
GUEST_SCHEMA_FILE = f'{SCHEMAS_DIR}/guest-schema.yml'
GUEST_CONFIG_SCHEMA = f'{SCHEMAS_DIR}/guest-config-schema.yml'
GUEST_PAIRS_SCHEMA = f'{SCHEMAS_DIR}/guest-pairs-schema.yml'

BLACKHOLE_LOOPBACK_MAP = {'blackhole': '127.6.6.6'}

DATA_INTERFACES_BASE_PORT = 10000
INTERNAL_INTERFACES_BASE_PORT = 11000
RESERVED_INTERFACES_BASE_PORT = 12000

TIMESTAMP_FORMAT = '%Y-%m-%d--%H-%M-%S'
