import pytest
from click.testing import CliRunner
from incident_diagram.cli import CLI
from unittest.mock import patch

@pytest.fixture
def runner():
    return CliRunner()

def test_cli_missing_params(runner):
    result = runner.invoke(CLI.diagram)
    assert result.exit_code != 0
    assert "Error: Incident summary is required" in result.output

@pytest.mark.skip(reason="Test temporarily disabled")
@patch('incident_diagram.cli.Diagram')
def test_cli_with_file(runner, mock_env_vars):
    with runner.isolated_filesystem():
        with open('incident.txt', 'w') as f:
            f.write('test incident')

        result = runner.invoke(CLI.diagram, [
            '-f', 'incident.txt',
            '-u', 'https://github.com/test/repo'
        ])

        print(result.stdout)
        print(result.stderr)
        print(result.return_value)
        print(result.exit_code)
        print(result.exception)
        print(result.exc_info)

        assert result.exit_code == 0
