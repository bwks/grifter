import os


BASE_DIR = os.path.join(os.path.dirname(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
DEFAULTS_FILE = f'{BASE_DIR}/defaults.yml'
BLACKHOLE_LOOPBACK_MAP = {'blackhole': '127.6.6.6'}
