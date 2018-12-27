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


config = load_data(DEFAULT_CONFIG_FILE)
interface_mappings = generate_guest_interface_mappings()


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


def display_connections(connections_list, guest=''):
    """
    Output a list of connections
    :param connections_list: List of dicts containing connection information ie:
      [{'local_guest': 'p1sw1',
        'local_port': 'swp7',
        'remote_guest': 'p1r7',
        'remote_port': 'ge-0/0/9'}]
    :param guest: Display connections for guest. TODO
    """
    guest_connections = []
    if guest:
        for i in connections_list:
            if i['local_guest'] == guest:
                guest_connections.append(
                    f"{i['local_guest']}-{i['local_port']} <--> {i['remote_guest']}-{i['remote_port']}"
                )
        for i in guest_connections:
            click.echo(i)
    else:
        for i in connections_list:
            click.echo(
                f"{i['local_guest']}-{i['local_port']} <--> {i['remote_guest']}-{i['remote_port']}"
            )


@click.group(context_settings={'help_option_names': ['-h', '--help']})
@click.version_option(version='0.2.4')
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

    errors = validate_data(guest_data)

    if not errors:
        loopbacks = generate_loopbacks(guest_data)
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
            return generate_vagrant_file(merged_data, loopbacks)
        else:
            display_errors(errors)
    else:
        display_errors(errors)


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
@click.option('--unique', is_flag=True, default=False)
def connections(datafile, guest, unique):
    """Show device to device connections."""
    guest_data = load_data_file(datafile)

    errors = validate_data(guest_data)

    if not errors:
        connections_list = generate_connections_list(guest_data, interface_mappings, unique)
        display_connections(connections_list, guest)
    else:
        display_errors(errors)
