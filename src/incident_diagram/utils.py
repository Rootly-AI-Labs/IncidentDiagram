from dotenv import load_dotenv
import os
import yaml
from smolagents import LiteLLMModel
class Utils:
    def __init__(self):
        pass
    @staticmethod
    def load_dotenv():
        # Load environment variables from .env file in current working directory
        env_path = os.path.join(os.getcwd(), '.env')
        load_dotenv(env_path)
        # Set default environment variables
        if os.getenv("OPENAI_API_KEY") is not None:
            os.environ.setdefault("OPENAI_API_KEY", os.getenv("OPENAI_API_KEY"))
        if os.getenv("ANTHROPIC_API_KEY") is not None:
            os.environ.setdefault("ANTHROPIC_API_KEY", os.getenv("ANTHROPIC_API_KEY"))
        if os.getenv("GEMINI_API_KEY") is not None:
            os.environ.setdefault("GEMINI_API_KEY", os.getenv("GEMINI_API_KEY"))
