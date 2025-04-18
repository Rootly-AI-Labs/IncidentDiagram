import click
import os
from incident_diagram.diagram import Diagram
import requests
import logging
from smolagents import LogLevel

class CLI:
    def __init__(self):
        pass

    @click.command()
    @click.option("--url", "-u", type=str, help="Github url of source code")
    @click.option('--model-id', '-m', default='o3-mini', help='Model to use for the diagram')
    @click.option('--output-path', '-o', type=click.Path(exists=False), help='Path to save the output file')
    @click.option('--incident-summary-file', '-f', type=click.Path(exists=True), help='Path to the incident summary file')
    @click.option('--incident-summary-url', '-iu', type=str, help='URL to the incident summary')
    @click.option('--verbosity', '-v', type=int, default=-1, help='Verbosity level')
    def diagram(
        url: str,
        model_id: str,
        output_path: str,
        incident_summary_file: str,
        incident_summary_url: str,
        verbosity: int
    ):
        """Create an incident diagram from input file and save to output path"""

        if incident_summary_file is None and incident_summary_url is None:
            click.echo("Error: Incident summary is required")
            exit(1)

        if incident_summary_file is not None:
            with open(incident_summary_file, 'r') as f:
                incident_summary = f.read()
        elif incident_summary_url is not None:
            with requests.get(incident_summary_url) as response:
                incident_summary = response.text

        if url is None and dir is None:
            click.echo("Error: Github repository URL or directory is required")
            exit(1)

        if output_path is None:
            current_dir = os.getcwd()
            output_path = os.path.join(current_dir, "artifacts")
            click.echo(f"Output path not provided, using {output_path}")

        if verbosity == 0:
            llm_loglevel = LogLevel.ERROR
            verbosity_level = logging.ERROR
        elif verbosity == 1:
            llm_loglevel = LogLevel.INFO
            verbosity_level = logging.INFO
        elif verbosity == 2:
            llm_loglevel = LogLevel.DEBUG
            verbosity_level = logging.DEBUG
        elif verbosity == -1:
            llm_loglevel = LogLevel.OFF
            verbosity_level = logging.CRITICAL
        else:
            click.echo("Error: Invalid verbosity level")
            exit(1)
        try:
            diagram = Diagram(url = url, directory = dir, incident_summary = incident_summary, model_id = model_id, llm_loglevel = llm_loglevel, verbosity_level = verbosity_level)
            diagram.generate(output_path)
        except Exception as e:
            click.echo(f"Error: {e}")
            exit(1)
        exit(0)


if __name__ == "__main__":
    CLI.diagram()
