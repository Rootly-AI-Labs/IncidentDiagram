import pytest
import os
from pathlib import Path

@pytest.fixture
def mock_env_vars(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")
    monkeypatch.setenv("GEMINI_API_KEY", "test-key")
    monkeypatch.setenv("HOLIDAY_API_KEY", "test-key")
    monkeypatch.setenv("CALENDARIFIC_API_KEY", "test-key")

@pytest.fixture
def sample_incident_text():
    return "Test incident description"

@pytest.fixture
def sample_repo_url():
    return "https://github.com/test/repo"
