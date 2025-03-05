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
            model_id = "o3-mini",
            llm_loglevel = LogLevel.ERROR,
            verbosity_level = logging.ERROR
        ):
        """
        Initialize the Diagram class.
        url: The url of the repository to ingest.
        directory: The directory to ingest. Either url or directory must be provided.
        incident_summary: Text containing the incident summary.
        model_id: The model_id to use.
        llm_loglevel: The log level for the LLM.
        verbosity_level: The log level for the logger.
        """
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
        self.model = LLMUtils.get_llm_model(model_id)

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

        timeline_prompts = {}
        timeline_prompts['system'] = self.prompts["timeline_parser"]["system"]
        timeline_prompts['user'] = self.prompts["timeline_parser"]["user"]
        self.timeline_parser = {
            "agent": self._get_code_agent(),
            "prompt": timeline_prompts
        }

        timeline_chart_prompts = {}
        timeline_chart_prompts['system'] = self.prompts["timeline_chart_generator"]["system"]
        timeline_chart_prompts['user'] = self.prompts["timeline_chart_generator"]["user"]
        self.timeline_chart_generator = {
            "agent": self._get_code_agent(),
            "prompt": timeline_chart_prompts
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
        chart = self._run_with_spinner("Generating components diagram", lambda: self.diagram_generator['agent'].run(self._format_prompt(self.diagram_generator['prompt'], components=components, affected_components=incident_components)))

        timeline = self._run_with_spinner("Generating timeline", lambda: self.timeline_parser['agent'].run(self._format_prompt(self.timeline_parser['prompt'], incident=self.incident_summary)))
        timeline_chart = self._run_with_spinner("Generating timeline chart", lambda: self.timeline_chart_generator['agent'].run(self._format_prompt(self.timeline_chart_generator['prompt'], timeline=timeline)))

        if not isinstance(chart, str):
            raise ValueError("Generated Output was not a string. LLM is probably not performing well. Please try again.")
        if not isinstance(chart, str):
            raise ValueError("Generated Output was not a string. LLM is probably not performing well. Please try again.")

        if not "```mermaid" in chart:
            chart = "```mermaid\n" + chart + "\n```"
        if not "```mermaid" in timeline_chart:
            timeline_chart = "```mermaid\n" + timeline_chart + "\n```"

        # append timeline_chart to chart
        chart = chart + "\n\n" + timeline_chart

        if output_path is not None:
            # Create directory if it doesn't exist
            os.makedirs(output_path, exist_ok=True)
            output_file = os.path.join(output_path, "incident.md")
            with open(output_file, "w") as f:
                f.write(chart)
            print(f"Markdown file with charts generated in {output_file}")
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
        if self._is_notebook():
            print(text + " ...")
            return function()
        else:
            spinner = Halo(text=text + " ..." , spinner='dots')
            spinner.start()
            try:
                result = function()
                spinner.stop()
                return result
            except Exception as e:
                spinner.fail(f'Failed to run {text}')
                raise e

    # https://stackoverflow.com/questions/15411967/how-can-i-check-if-code-is-executed-in-the-ipython-notebook
    def _is_notebook(self) -> bool:
        try:
            shell = get_ipython().__class__.__name__
            if shell == 'ZMQInteractiveShell':
                return True   # Jupyter notebook or qtconsole
            elif shell == 'TerminalInteractiveShell':
                return False  # Terminal running IPython
            else:
                return False  # Other type (?)
        except NameError:
            return False      # Probably standard Python interpreter
