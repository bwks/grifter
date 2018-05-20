from click.testing import CliRunner

from vagrantfile_builder.constants import (
    GUESTS_EXAMPLE_FILE,
    GROUPS_EXAMPLE_FILE,
)

from vagrantfile_builder.cli import cli


def test_cli_example_guest_output():
    runner = CliRunner()
    result = runner.invoke(cli, ['example', '--guest'])

    with open(GUESTS_EXAMPLE_FILE, 'r') as f:
        expected = f.read()

    assert result.exit_code == 0
    assert result.output == f'{expected}\n'


def test_cli_example_group_output():
    runner = CliRunner()
    result = runner.invoke(cli, ['example', '--group'])

    with open(GROUPS_EXAMPLE_FILE, 'r') as f:
        expected = f.read()

    assert result.exit_code == 0
    assert result.output == f'{expected}\n'

