import pytest
from incident_diagram.diagram import Diagram
from unittest.mock import Mock, patch

@pytest.fixture
def mock_ingest():
    with patch('incident_diagram.diagram.ingest') as mock:
        mock.return_value = (None, "mock_tree", "mock_code")
        yield mock

def test_diagram_initialization(mock_ingest, mock_env_vars):
    diagram = Diagram(
        url="https://github.com/test/repo",
        incident_summary="test incident"
    )
    assert diagram.incident_summary == "test incident"
    assert diagram.tree == "mock_tree"
    assert diagram.code == "mock_code"

def test_diagram_missing_params():
    with pytest.raises(ValueError) as exc_info:
        Diagram()
    assert "Either url or directory must be provided" in str(exc_info.value)

@patch('incident_diagram.diagram.CodeAgent')
def test_diagram_generate(mock_agent, mock_ingest, mock_env_vars, tmp_path):
    mock_agent.return_value.run.return_value = "```mermaid\ngraph TD\nA-->B\n```"

    diagram = Diagram(
        url="https://github.com/test/repo",
        incident_summary="test incident"
    )

    output_file = diagram.generate(str(tmp_path))
    assert output_file == str(tmp_path / "incident.md")
    assert (tmp_path / "incident.md").exists()
