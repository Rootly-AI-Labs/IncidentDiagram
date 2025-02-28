import pytest
from incident_diagram.utils import Utils
import os

def test_load_dotenv_missing_file(tmp_path, monkeypatch):
    monkeypatch.setattr(os, 'getcwd', lambda: str(tmp_path))
    Utils.load_dotenv()
    # Should not raise an error when .env is missing
    assert True
