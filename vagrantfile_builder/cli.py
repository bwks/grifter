import click

from .loaders import (
    load_data,
)

from vagrantfile_builder import (
    generate_loopbacks,
    update_guests,
    generate_vagrant_file,
)


@click.group(context_settings={'help_option_names': ['-h', '--help']})
@click.version_option(version='0.1.0')
def cli():
    """Create a Vagrantfile from a YAML data input file."""
    pass


@cli.command(help="""
    Create a Vagrantfile.
    
    DATAFILE: Location of DATAFILE.
    """)
@click.argument('datafile')
def create(datafile):
    """Create a Vagrantfile."""
    data = load_data(datafile)
    loopbacks = generate_loopbacks(data['hosts'])
    update_guests(data['hosts'])
    return generate_vagrant_file(data, loopbacks)
