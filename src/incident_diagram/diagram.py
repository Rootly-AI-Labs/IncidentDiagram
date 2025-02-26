from smolagents import LiteLLMModel, CodeAgent, LogLevel
import yaml
from pathlib import Path
import litellm
import os
from llm_utils import LLMUtils

class Diagram:
    """Main class for handling incident diagram creation"""
    LLM_LOGLEVEL = LogLevel.INFO
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
    def __init__(self, tree, code, model):
        self.tree = tree
        self.code = code
        self._load_prompts()
        self.model = LLMUtils.get_llm_model(model)

        # litellm._turn_on_debug()
        # Just to be consistent, I am doing all formatting in the run method.
        parser_prompts = {}
        parser_prompts['system'] = self.prompts["code_parser"]["system"]
        parser_prompts['user'] = self.prompts["code_parser"]["user"]
        self.code_parser = {
            "agent": CodeAgent(
                tools=[],
                model=self.model, 
                verbosity_level = self.LLM_LOGLEVEL,
                max_steps=self.LLM_MAX_STEPS_OVERRIDE
            ),
            "prompt": parser_prompts
        }
        incident_prompts = {}
        incident_prompts['system'] = self.prompts["incident_parser"]["system"]
        incident_prompts['user'] = self.prompts["incident_parser"]["user"]
        self.incident_parser = {
            "agent": CodeAgent(
                tools=[],
                model=self.model, 
                verbosity_level = self.LLM_LOGLEVEL,
                max_steps=self.LLM_MAX_STEPS_OVERRIDE
            ),
            "prompt": incident_prompts
        }

        diagram_prompts = {}
        diagram_prompts['system'] = self.prompts["diagram_generator"]["system"]
        diagram_prompts['user'] = self.prompts["diagram_generator"]["user"]
        self.diagram_generator = {
            "agent": CodeAgent(
                tools=[],
                model=self.model, 
                verbosity_level = self.LLM_LOGLEVEL,
                max_steps=self.LLM_MAX_STEPS_OVERRIDE
            ),
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
    
    def generate(self, output_path):
        """Generate the diagram and save to output path"""
        # print()
        components = self.code_parser['agent'].run(self._format_prompt(self.code_parser['prompt'], tree=self.tree, code=self.code))
        incident = self.incident_parser['agent'].run(self._format_prompt(self.incident_parser['prompt'], components=components, incident=self.incident))
        chart = self.diagram_generator['agent'].run(self._format_prompt(self.diagram_generator['prompt'], components=components, affected_components=incident))
        
        # Create directory if it doesn't exist
        os.makedirs(output_path, exist_ok=True)
        output_file = os.path.join(output_path, "incident.md")
        with open(output_file, "w") as f:
            f.write(chart)
        # self.agent.run(self.prompts["generate_chart"])
        return "Diagram generated"