import pytest
from incident_diagram.llm_utils import LLMUtils

def test_get_llm_model_gpt(mock_env_vars):
    model = LLMUtils.get_llm_model("gpt-4")
    assert model is not None
    assert model.model_id == "gpt-4"

def test_get_llm_model_claude(mock_env_vars):
    model = LLMUtils.get_llm_model("claude-3")
    assert model is not None
    assert "claude-3" in model.model_id

def test_get_llm_model_invalid():
    with pytest.raises(ValueError) as exc_info:
        LLMUtils.get_llm_model("invalid-model")
    assert "Unsupported model type" in str(exc_info.value)

def test_get_llm_model_missing_key(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    with pytest.raises(ValueError) as exc_info:
        LLMUtils.get_llm_model("gpt-4")
    assert "OPENAI_API_KEY must be set" in str(exc_info.value)
