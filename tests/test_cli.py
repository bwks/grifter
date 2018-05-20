from click.testing import CliRunner

from vagrantfile_builder.constants import GUEST_DEFAULTS_FILE
from vagrantfile_builder.cli import cli


def test_cli_variables_guest_output():
    runner = CliRunner()
    result = runner.invoke(cli, ['variables', '--guest'])

    with open(GUEST_DEFAULTS_FILE, 'r') as f:
        expected = f.read()

    assert result.exit_code == 0
    assert result.output == f'{expected}\n'


def test_cli_variables_group_output():
    runner = CliRunner()
    result = runner.invoke(cli, ['variables', '--group'])

    expected = 'add group option\n'

    assert result.exit_code == 0
    assert result.output == f'{expected}'
