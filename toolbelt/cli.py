import click

from toolbelt import generate_loopbacks
from toolbelt import load_host_data
from toolbelt import update_hosts
from toolbelt import generate_vagrant_file


@click.command()
@click.option('--data_file', help='location of data file')
def make_vagrant_file(data_file):
    data = load_host_data(data_file)
    loopbacks = generate_loopbacks(data['hosts'])
    update_hosts(data['hosts'])
    return generate_vagrant_file(data, loopbacks)


if __name__ == '__main':
    make_vagrant_file()
