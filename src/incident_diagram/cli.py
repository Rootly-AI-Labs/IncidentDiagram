import click
from gitingest import ingest
import os
from diagram import Diagram

class CLI:
    def __init__(self):
        pass

    @click.command()
    @click.option("--dir", "-d", type=click.Path(exists=False), help="Path of source code git directory on disk")
    @click.option("--url", "-u", type=str, help="Github url of source code")
    @click.option('--format', '-f', default='png', help='Output format (png, svg, etc)')
    @click.option('--model', '-m', default='gpt-4o', help='Model to use for the diagram')
    def diagram(dir: str, url: str, format: str, model: str):
        """Create an incident diagram from input file and save to output path"""
        
        if dir:
            raise NotImplementedError("Directory input not implemented yet")
            summary, tree, code = ingest(dir)
            diagram = Diagram(tree, code, model)
            diagram.generate()
        elif url:
            summary, tree, code = ingest(url)
            diagram = Diagram(tree, code, model)
            diagram.generate()
           
        else:
            print("No input provided")    

if __name__ == "__main__":
    CLI.diagram()