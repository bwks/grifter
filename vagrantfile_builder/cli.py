import click

from .constants import (
    GUESTS_EXAMPLE_FILE,
    GROUPS_EXAMPLE_FILE,
    GUEST_DEFAULTS_FILE
)

from .loaders import load_data

from vagrantfile_builder import (
    generate_loopbacks,
    update_guest_interfaces,
    generate_vagrant_file,
    update_guest_data,
)


@click.group(context_settings={'help_option_names': ['-h', '--help']})
@click.version_option(version='0.1.0')
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
    data = load_data(datafile)
    loopbacks = generate_loopbacks(data['guests'])
    merged_data = update_guest_data(data)
    update_guest_interfaces(merged_data['guests'])
    return generate_vagrant_file(merged_data, loopbacks)


@cli.command(help='Print default variables.')
@click.option('--guest', is_flag=True)
@click.option('--group', is_flag=True)
def variables(guest, group):
    """Create a blank Variables file"""
    if guest:
        with open(GUEST_DEFAULTS_FILE, 'r') as f:
            click.echo(f.read())
    if group:
        click.echo('add group option')


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
