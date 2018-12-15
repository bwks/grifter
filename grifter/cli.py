import click

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
)

from .validators import (
    validate_guests_in_guest_config,
    validate_guest_interfaces,
)


config = load_data(DEFAULT_CONFIG_FILE)
interface_mappings = generate_guest_interface_mappings()


@click.group(context_settings={'help_option_names': ['-h', '--help']})
@click.version_option(version='0.2.0')
def cli():
    """Create a Vagrantfile from a YAML data input file."""
    pass


@cli.command(help='''
    Create a Vagrantfile.
    
    DATAFILE - Location of DATAFILE.
    ''')
@click.argument('datafile')
def create(datafile):
    """Create a Vagrantfile."""
    guest_data = load_data(datafile)

    errors = validate_data(guest_data)

    if not errors:
        try:
            validate_guests_in_guest_config(guest_data, config)
            validate_guest_interfaces(guest_data, config, interface_mappings)
        except AttributeError as e:
            errors.append(e)

    elif not errors:
        loopbacks = generate_loopbacks(guest_data)
        merged_data = update_guest_data(guest_data)
        update_guest_interfaces(merged_data, config)
        update_guest_additional_storage(merged_data)

        return generate_vagrant_file(merged_data, loopbacks)
    else:
        for error in errors:
            click.echo(error)


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
