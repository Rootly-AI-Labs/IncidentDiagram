from pathlib import Path
from setuptools import setup

# This is where you add any fancy path resolution to the local lib:
local_path: str = (Path(__file__).parent.parent / "gitingest").as_uri()

setup(
    install_requires=[
        #f"gitingest @ git+ssh://git@github.com/cyclotruc/gitingest.git@c96a7d3",
        f"gitingest @ {local_path}",
        "click>=8.0.0",
        "toml>=0.10.0",
        "smolagents",
        "litellm",
        "tomli",
        "halo",
        "asyncio"

    ]
)
