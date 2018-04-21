import click

from toolbelt import generate_loopbacks
from toolbelt import load_host_data
from toolbelt import update_hosts
from toolbelt import generate_vagrant_file


@click.command()
@click.argument('data_file')
def cli(data_file):
    data = load_host_data(data_file)
    loopbacks = generate_loopbacks(data['hosts'])
    update_hosts(data['hosts'])
    return generate_vagrant_file(data, loopbacks)


if __name__ == '__main__':
    cli()
