from smolagents import LiteLLMModel
import os
import litellm

class LLMUtils:
    def __init__(self):
        pass

    def get_llm_model(model: str) -> LiteLLMModel:
        """Get the LLM model based on the model type.

        Args:
            model: Model type ('gpt' or 'claude')
        Returns:
            LiteLLMModel: Configured model instance
        """
        llm_model = None
        match model:
            case model if model.startswith("claude"):
                if "ANTHROPIC_API_KEY" not in os.environ:
                    raise ValueError("ANTHROPIC_API_KEY must be set in .env file or environment variable")
                llm_model = LiteLLMModel(
                    model_id="anthropic/" + model,
                    api_key=os.environ["ANTHROPIC_API_KEY"],
                    temperature=0.2
                )
            case model if model.startswith("gpt"):
                if "OPENAI_API_KEY" not in os.environ:
                    raise ValueError("OPENAI_API_KEY must be set in .env file or environment variable")
                llm_model = LiteLLMModel(
                    model_id=model,
                    api_base="https://api.openai.com/v1",
                    api_key=os.environ["OPENAI_API_KEY"],
                    temperature=0.2
                )
            case model if model.startswith("o1") or model.startswith("o3"):
                # O-series models don't support temperature=0.2. Only temperature=1 is supported.
                if "OPENAI_API_KEY" not in os.environ:
                    raise ValueError("OPENAI_API_KEY must be set in .env file or environment variable")
                llm_model = LiteLLMModel(
                    model_id=model,
                    api_base="https://api.openai.com/v1",
                    api_key=os.environ["OPENAI_API_KEY"]
                    )
            case model if model.startswith("gemini"):
                if "GEMINI_API_KEY" not in os.environ:
                    raise ValueError("GEMINI_API_KEY must be set in .env file or environment variable")
                llm_model = LiteLLMModel(
                    model_id="google/" + model,
                    api_key=os.environ["GEMINI_API_KEY"],
                    temperature=0.2
                )
            case model if model.startswith("ollama"):
                llm_model = LiteLLMModel(
                    model_id=model,
                    api_base="http://localhost:11434",
                    pre_init=lambda: LLMUtils._check_ollama_model(model),
                    temperature=0.2
                )
            case _:
                raise ValueError(f"Unsupported model type: {model}.\n Supported models prefixes are: gpt, claude and gemini. \n Send a pull request to add support for more models.")
        return llm_model

    def _check_ollama_model(model: str):
        if not os.system(f"ollama list | grep {model} > /dev/null 2>&1"):
            raise ValueError(f"Model {model} not found. Please install it using `ollama pull {model}`")
