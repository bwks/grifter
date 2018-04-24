import click

from vagrantfile_builder import generate_loopbacks
from vagrantfile_builder import load_host_data
from vagrantfile_builder import update_hosts
from vagrantfile_builder import generate_vagrant_file


@click.group(context_settings={'help_option_names': ['-h', '--help']})
@click.version_option(version='0.1.0')
def cli():
    """
    Create a Vagrantfile from a YAML data input file.
    """
    pass


help_message = """
    Create a Vagrantfile
    
    DATAFILE: Location of DATAFILE
    """


@cli.command(help=help_message)
@click.argument('datafile')
def create(datafile):
    data = load_host_data(datafile)
    loopbacks = generate_loopbacks(data['hosts'])
    update_hosts(data['hosts'])
    return generate_vagrant_file(data, loopbacks)
