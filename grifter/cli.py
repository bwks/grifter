import click
import sys

from .constants import (
    GUESTS_EXAMPLE_FILE,
    GROUPS_EXAMPLE_FILE,
    DEFAULT_CONFIG_FILE,
)
from .loaders import load_data
from .api import (
    generate_loopbacks,
    update_guest_interfaces,
    generate_vagrant_file,
    update_guest_data,
    validate_data,
    update_guest_additional_storage,
    generate_guest_interface_mappings,
    update_reserved_interfaces,
    generate_connections_list,
)
from .validators import (
    validate_guests_in_guest_config,
    validate_guest_interfaces,
)
from .utils import sort_nicely


config = load_data(DEFAULT_CONFIG_FILE)
interface_mappings = generate_guest_interface_mappings()


def validate_guest_data(guest_data):
    """
    Validate and update guest data if validation is successful.
    :param guest_data: Dict of guest data
    :return: Dict of updated data.
    """
    errors = validate_data(guest_data)
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
    exit(1)


def display_connections(connections_list, guest=''):
    """
    Output a list of connections
    :param connections_list: List of dicts containing connection information ie:
      [{'local_guest': 'p1sw1',
        'local_port': 'swp7',
        'remote_guest': 'p1r7',
        'remote_port': 'ge-0/0/9'}]
    :param guest: Display connections for guest.
    """
    guest_connections = []

    def make_link(x):
        return f"{x['local_guest']}-{x['local_port']} <--> {x['remote_guest']}-{x['remote_port']}"

    if guest:
        for i in connections_list:
            if i['local_guest'] == guest:
                guest_connections.append(make_link(i))
    else:
        for i in connections_list:
            guest_connections.append(make_link(i))

    for i in sort_nicely(guest_connections):
        click.echo(i)


@click.group(context_settings={'help_option_names': ['-h', '--help']})
@click.version_option(version='0.2.6')
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

    guest_data = load_data_file(datafile)
    validated_guest_data = validate_guest_data(guest_data)
    loopbacks = generate_loopbacks(guest_data)
    return generate_vagrant_file(validated_guest_data, loopbacks)


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
    guest_data = load_data_file(datafile)
    validated_guest_data = validate_guest_data(guest_data)
    connections_list = generate_connections_list(validated_guest_data, interface_mappings, unique)
    display_connections(connections_list, guest)
