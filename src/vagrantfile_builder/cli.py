import click

from vagrantfile_builder import generate_loopbacks
from vagrantfile_builder import load_host_data
from vagrantfile_builder import update_hosts
from vagrantfile_builder import generate_vagrant_file


@click.command()
@click.option('-c', '--create', is_flag=True, help='Create Vagrantfile')
@click.argument('datafile')
def cli(create, datafile):
    """
    Create a Vagrantfile from a YAML data input file.

    DATAFILE: Location of DATAFILE
    """
    data = load_host_data(datafile)
    loopbacks = generate_loopbacks(data['hosts'])
    update_hosts(data['hosts'])
    vagrantfile = generate_vagrant_file(data, loopbacks)

    return vagrantfile if create else click.echo(vagrantfile)
