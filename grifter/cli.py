import click
import sys

from .constants import (
    GUESTS_EXAMPLE_FILE,
    GROUPS_EXAMPLE_FILE,
)
from .loaders import (
    load_data,
    load_config_file,
)
from .api import (
    generate_loopbacks,
    update_guest_interfaces,
    generate_vagrant_file,
    update_guest_data,
    update_guest_additional_storage,
    generate_guest_interface_mappings,
    update_reserved_interfaces,
    generate_connections_list,
    merge_user_config,
    generate_dotfile,
    generate_connection_strings,
)
from .validators import (
    validate_guests_in_guest_config,
    validate_guest_interfaces,
    validate_data,
    validate_config,
)

interface_mappings = generate_guest_interface_mappings()


def validate_guest_config(config):
    errors = validate_config(config)
    if errors:
        display_errors(errors)


def validate_guest_data(guest_data, config):
    """
    Validate and update guest data if validation is successful.
    :param guest_data: Dict of guest data.
    :param config: Dict of config data.
    :return: Dict of updated data.
    """
    guest_defaults = load_config_file('guest-defaults.yml')
    errors = []

    guest_errors = validate_data(guest_data)
    if guest_errors:
        errors += guest_errors

    if guest_defaults:
        guest_defaults_errors = validate_data(guest_defaults, guest_default_data=True)
        if guest_defaults_errors:
            errors += guest_defaults_errors

    if not errors:
        merged_data = update_guest_data(guest_data)
        update_guest_interfaces(merged_data, config)
        update_reserved_interfaces(merged_data, config)
        update_guest_additional_storage(merged_data)

        try:
            validate_guests_in_guest_config(merged_data, config)
            validate_guest_interfaces(merged_data, config, interface_mappings)
        except AttributeError as e:
            errors.append(e)
        if not errors:
            return merged_data
    if errors:
        display_errors(errors)


def load_data_file(datafile):
    """
    Load data file.
    :param datafile: Name of datafile
    :return: Dict of guest data.
    """
    try:
        guest_data = load_data(datafile)
    except FileNotFoundError:
        click.echo(f'Datafile: {datafile} not found.')
        sys.exit(1)
    return guest_data


def display_errors(errors_list):
    """
    Outputs a list of errors
    :param errors_list: List of errors
    """
    for error in errors_list:
        click.echo(error)
    sys.exit(1)


def display_connections(connections, guest=''):
    """
    Output a list of connections
    :param connections: List of dicts containing connection information ie:
      [{'local_guest': 'p1sw1',
        'local_port': 'swp7',
        'remote_guest': 'p1r7',
        'remote_port': 'ge-0/0/9'}]
    :param guest: Display connections for guest.
    """
    if guest:
        guest_connections = [i for i in connections if i['local_guest'] == guest]
        connections_list = generate_connection_strings(guest_connections)
    else:
        connections_list = generate_connection_strings(connections)

    for i in connections_list:
        click.echo(i)


@click.group(context_settings={'help_option_names': ['-h', '--help']})
@click.version_option(version='0.2.11')
def cli():
    """Create a Vagrantfile from a YAML data input file."""
    pass


@cli.command(help='''
    Create a Vagrantfile.
    
    DATAFILE - Name of DATAFILE.
    ''')
@click.argument('datafile')
def create(datafile):
    """Create a Vagrantfile."""
    guest_config = merge_user_config()
    validate_guest_config(guest_config)
    guest_data = load_data_file(datafile)
    validated_guest_data = validate_guest_data(guest_data, guest_config)
    loopbacks = generate_loopbacks(guest_data)
    generate_vagrant_file(validated_guest_data, loopbacks)
    unsorted_connections = generate_connections_list(validated_guest_data, interface_mappings,
                                                     unique=True)
    connections_list = generate_connection_strings(unsorted_connections, dotfile=True)
    generate_dotfile(connections_list)


@cli.command(help='Print example file declaration.')
@click.option('--guest', is_flag=True)
@click.option('--group', is_flag=True)
def example(guest, group):
    """Display example variable file"""
    if guest:
        with open(GUESTS_EXAMPLE_FILE, 'r') as f:
            click.echo(f.read())
    if group:
        with open(GROUPS_EXAMPLE_FILE, 'r') as f:
            click.echo(f.read())


@cli.command(help='''
    Show device to device connections.

    DATAFILE - Name of DATAFILE.
    ''')
@click.argument('datafile')
@click.argument('guest', default='')
@click.option('--unique', is_flag=True, default=False, help='Remove duplicate connections.')
def connections(datafile, guest, unique):
    """Show device to device connections."""
    guest_config = merge_user_config()
    validate_guest_config(guest_config)
    guest_data = load_data_file(datafile)
    validated_guest_data = validate_guest_data(guest_data, guest_config)
    connections_list = generate_connections_list(validated_guest_data, interface_mappings, unique)
    display_connections(connections_list, guest)


@cli.command(help='''
    Create topology.dot file.

    DATAFILE - Name of DATAFILE.
    ''')
@click.argument('datafile')
def dotfile(datafile):
    """Generate undirected dotfile."""
    guest_config = merge_user_config()
    validate_guest_config(guest_config)
    guest_data = load_data_file(datafile)
    validated_guest_data = validate_guest_data(guest_data, guest_config)
    unsorted_connections = generate_connections_list(validated_guest_data, interface_mappings, unique=True)
    connections_list = generate_connection_strings(unsorted_connections, dotfile=True)
    generate_dotfile(connections_list)
