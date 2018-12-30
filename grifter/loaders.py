import yaml
import json
import logging
import os

from jinja2 import Environment, FileSystemLoader

logger = logging.getLogger(__name__)

USER_HOME = os.path.expanduser('~')
DEFAULT_CONFIG_DIRS = [
    '/opt/grifter',
    f'{USER_HOME}/.grifter',
    '.',
]


def render_from_template(
        template_name, template_directory, custom_filters=None,
        trim_blocks=True, lstrip_blocks=True, **kwargs
        ):
    """
    Render template with custom filters
    """
    loader = FileSystemLoader(template_directory)
    env = Environment(loader=loader, trim_blocks=trim_blocks, lstrip_blocks=lstrip_blocks)

    if custom_filters is not None:
        for custom_filter in custom_filters:
            env.filters[custom_filter.__name__] = custom_filter

    template = env.get_template(template_name)
    return template.render(**kwargs)


def load_data(location, data_type='yaml'):
    """
    Load data file from location
    :param location: Location of YAML file
    :param data_type: Type of source data YAML|JSON
    :return: Dictionary of data
    """
    valid_types = ['yaml', 'json']
    if data_type.lower() not in valid_types:
        raise AttributeError('Valid data types are yaml or json')

    with open(location, 'r') as f:
        if data_type.lower() == 'yaml':
            return yaml.safe_load(f)
        elif data_type.lower() == 'json':
            return json.load(f)


def load_config_file(config_file):
    """
    Load config_file from the following locations top to
    bottom least to most preferred. Value are overwritten not merged:
      - /opt/grifter/
      - ~/.grifter/
      - ./
    :param config_file: Guest defaults filename
    :return: Dict of guest default data or empty dict
    """
    config = {}
    for directory in DEFAULT_CONFIG_DIRS:
        try:
            config = load_data(f'{directory}/{config_file}')
            logger.info(f'File: "{directory}/{config_file}" found')
        except FileNotFoundError:
            logger.warning(f'File: "{directory}/{config_file}" not found')
        except PermissionError:
            logger.error(f'File: "{directory}/{config_file}" permission denied')

    return config
