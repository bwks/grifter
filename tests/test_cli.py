from click.testing import CliRunner

from grifter.constants import (
    GUESTS_EXAMPLE_FILE,
    GROUPS_EXAMPLE_FILE,
)

from grifter.cli import cli

from .mock_data import mock_invalid_guest_data_file


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


def test_cli_create_with_invalid_data_output():
    runner = CliRunner()
    result = runner.invoke(cli, ['create', mock_invalid_guest_data_file])

    assert result.exit_code == 1
    assert result.output == "{'vagrant_box': [{'name': ['empty values not allowed']}]}\n"
