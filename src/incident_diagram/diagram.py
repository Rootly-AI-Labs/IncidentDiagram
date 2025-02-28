from smolagents import LiteLLMModel, CodeAgent, LogLevel
import yaml
from pathlib import Path
import litellm
import os
from incident_diagram.llm_utils import LLMUtils
from gitingest import ingest_async
from halo import Halo
import asyncio
import nest_asyncio
import logging




class Diagram:
    """Main class for handling incident diagram creation"""
    LLM_MAX_STEPS_OVERRIDE = 6
    # Load the model and agent configurations
    def _load_prompts(self):
        self.prompts = {}
        prompt_path = Path(__file__).parent / "prompts.yaml"
        print(prompt_path)
        with open(prompt_path) as f:
            prompts = yaml.safe_load(f)
            for key, value in prompts.items():
                item = {}
                item["system"] = value["system"]
                item["user"] = value["user"]
                self.prompts[key] = item
        return self.prompts
    # Initialize model and agent
    def __init__(
            self,
            url = None,
            directory = None,
            incident_summary = None,
            model = "gpt-4o",
            llm_loglevel = LogLevel.ERROR,
            verbosity_level = logging.ERROR
        ):
        self.llm_loglevel = llm_loglevel
        self.verbosity_level = verbosity_level
        logging.basicConfig(level=self.verbosity_level)

        # This is a hack to make the ingest_async function work with the sync code for Jupyter notebooks
        nest_asyncio.apply()
        loop = asyncio.get_event_loop()

        if url is not None:
            _, self.tree, self.code = loop.run_until_complete(ingest_async(url))
        elif directory is not None:
            _, self.tree, self.code = loop.run_until_complete(ingest_async(directory))
        else:
            raise ValueError("Either url or directory must be provided")

        if incident_summary is not None:
            self.incident_summary = incident_summary
        else:
            raise ValueError("incident_summary must be provided")

        self._load_prompts()
        self.model = LLMUtils.get_llm_model(model)


        # litellm._turn_on_debug()
        # Just to be consistent, I am doing all formatting in the run method.
        parser_prompts = {}
        parser_prompts['system'] = self.prompts["code_parser"]["system"]
        parser_prompts['user'] = self.prompts["code_parser"]["user"]
        self.code_parser = {
            "agent": self._get_code_agent(),
            "prompt": parser_prompts
        }
        incident_prompts = {}
        incident_prompts['system'] = self.prompts["incident_parser"]["system"]
        incident_prompts['user'] = self.prompts["incident_parser"]["user"]
        self.incident_parser = {
            "agent": self._get_code_agent(),
            "prompt": incident_prompts
        }

        diagram_prompts = {}
        diagram_prompts['system'] = self.prompts["diagram_generator"]["system"]
        diagram_prompts['user'] = self.prompts["diagram_generator"]["user"]
        self.diagram_generator = {
            "agent": self._get_code_agent(),
            "prompt": diagram_prompts
        }

    def _format_prompt(self, prompt, **kwargs):
        formatted_prompt = {}
        for key, value in prompt.items():
            # for arg_key, arg_value in kwargs.items():
                # to keep it simple, variable substition is only done in 'user' prompts
            if key == 'user':
                #print(**kwargs)
                formatted_prompt[key] = value.format(**kwargs)
            else:
                formatted_prompt[key] = value

        # Join formatted prompts into single string with key:value pairs
        prompt_str = "\n\n".join([f"{key} : {value}" for key, value in formatted_prompt.items()])
        return prompt_str

    def generate(self, output_path=None):
        """Generate the diagram and save to output path"""

        components = self._run_with_spinner("Parsing code", lambda: self.code_parser['agent'].run(self._format_prompt(self.code_parser['prompt'], tree=self.tree, code=self.code)))
        incident_components = self._run_with_spinner("Parsing incident", lambda: self.incident_parser['agent'].run(self._format_prompt(self.incident_parser['prompt'], components=components, incident=self.incident_summary)))
        chart = self._run_with_spinner("Generating diagram", lambda: self.diagram_generator['agent'].run(self._format_prompt(self.diagram_generator['prompt'], components=components, affected_components=incident_components)))

        if not isinstance(chart, str):
            raise ValueError("Generated Output was not a string. LLM is probably not performing well. Please try again.")
        if not "```mermaid" in chart:
            chart = "```mermaid\n" + chart + "\n```"
        if output_path is not None:
            # Create directory if it doesn't exist
            os.makedirs(output_path, exist_ok=True)
            output_file = os.path.join(output_path, "incident.md")
            with open(output_file, "w") as f:
                f.write(chart)
            print(f"Chart generated in {output_file}")
            return output_file
        else:
            return chart

    def _get_code_agent(self):
        return CodeAgent(
            tools=[],
            model=self.model,
            verbosity_level = self.llm_loglevel,
            max_steps=self.LLM_MAX_STEPS_OVERRIDE,
            additional_authorized_imports=["json"]
        )

    def _run_with_spinner(self, text:str, function ):
        spinner = Halo(text=text, spinner='dots')
        try:
            result = function()
            spinner.stop()
            return result
        except Exception as e:
            spinner.fail(f'Failed to run {text}')
            raise e
