from smolagents import LiteLLMModel
import os
import litellm

class LLMUtils:
    def __init__(self):
        pass

    def get_llm_model(model_id: str) -> LiteLLMModel:
        """Get the LLM model based on the model type.

        Args:
            model: Model type ('gpt' or 'claude')
        Returns:
            LiteLLMModel: Configured model instance
        """
        llm_model = None
        match model_id:
            case model_id if model_id.startswith("claude"):
                if "ANTHROPIC_API_KEY" not in os.environ:
                    raise ValueError("ANTHROPIC_API_KEY must be set in .env file or environment variable")
                llm_model = LiteLLMModel(
                    model_id="anthropic/" + model_id,
                    api_key=os.environ["ANTHROPIC_API_KEY"],
                    temperature=0.2
                )
            case model_id if model_id.startswith("gpt"):
                if "OPENAI_API_KEY" not in os.environ:
                    raise ValueError("OPENAI_API_KEY must be set in .env file or environment variable")
                llm_model = LiteLLMModel(
                    model_id=model_id,
                    api_base="https://api.openai.com/v1",
                    api_key=os.environ["OPENAI_API_KEY"],
                    temperature=0.2
                )
            case model_id if model_id.startswith("o1") or model_id.startswith("o3"):
                # O-series models don't support temperature=0.2. Only temperature=1 is supported.
                if "OPENAI_API_KEY" not in os.environ:
                    raise ValueError("OPENAI_API_KEY must be set in .env file or environment variable")
                llm_model = LiteLLMModel(
                    model_id=model_id,
                    api_base="https://api.openai.com/v1",
                    api_key=os.environ["OPENAI_API_KEY"]
                    )
            case model_id if model_id.startswith("gemini"):
                if "GEMINI_API_KEY" not in os.environ:
                    raise ValueError("GEMINI_API_KEY must be set in .env file or environment variable")
                llm_model = LiteLLMModel(
                    model_id="google/" + model_id,
                    api_key=os.environ["GEMINI_API_KEY"],
                    temperature=0.2
                )
            case _:
                raise ValueError(f"Unsupported model type: {model_id}.\n Supported models prefixes are: gpt, claude and gemini. \n Send a pull request to add support for more models.")
        return llm_model
