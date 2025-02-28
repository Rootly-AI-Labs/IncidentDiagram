import click
import os
from incident_diagram.diagram import Diagram
import requests

class CLI:
    def __init__(self):
        pass

    @click.command()
    @click.option("--dir", "-d", type=click.Path(exists=False), help="Path of source code git directory on disk")
    @click.option("--url", "-u", type=str, help="Github url of source code")
    @click.option('--model', '-m', default='gpt-4o', help='Model to use for the diagram')
    @click.option('--output-path', '-o', type=click.Path(exists=False), help='Path to save the output file')
    @click.option('--incident-summary', '-i', type=str, help='Incident summary')
    @click.option('--incident-summary-file', '-f', type=click.Path(exists=True), help='Path to the incident summary file')
    @click.option('--incident-summary-url', '-iu', type=str, help='URL to the incident summary')
    def diagram(dir: str, url: str, model: str, output_path: str, incident_summary: str, incident_summary_file: str, incident_summary_url: str):
        """Create an incident diagram from input file and save to output path"""

        if incident_summary is None and incident_summary_file is None and incident_summary_url is None:
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

        diagram = Diagram(url = url, directory = dir, incident_summary = incident_summary, model = model)
        diagram.generate(output_path)
        exit(0)


if __name__ == "__main__":
    CLI.diagram()
