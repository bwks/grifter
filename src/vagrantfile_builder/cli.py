import click

from vagrantfile_builder import generate_loopbacks
from vagrantfile_builder import load_host_data
from vagrantfile_builder import update_hosts
from vagrantfile_builder import generate_vagrant_file


@click.group(context_settings={'help_option_names':['-h','--help']})
def cli():
    pass


@click.command()
@click.option('-c', '--create', help='Create Vagrantfile')
@click.argument('datafile')
def command(create, datafile):
    """
    Create a Vagrantfile from a YAML data input file.

    DATAFILE: Location of DATAFILE
    """
    if create:
        data = load_host_data(datafile)
        loopbacks = generate_loopbacks(data['hosts'])
        update_hosts(data['hosts'])
        return generate_vagrant_file(data, loopbacks)
    else:
        cli.help()


@click.command()
@click.pass_context
def help(ctx):
    print(ctx.parent.get_help())


cli.add_command(command)
cli.add_command(help)
