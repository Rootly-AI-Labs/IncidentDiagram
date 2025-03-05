# Incident Diagram 🥳☄️
IncidentDiagram is a tool that leverages LLMs to help visualize details in a post-incident analysis or post-mortem.

The initial prototype assumes that the incident review mentions the components that were affected.

```
$ incidentdiagram -f example_incident.txt  -u https://github.com/Rootly-AI-Lab/EventOrOutage
.
.
Chart generated in artifacts/incident.md
```

This repo has an [example chart](example_output.md) for reference

## Get started 🚀
```
python -m venv .venv
source .venv/bin/activate
pip install .
```
An example incident that goes along with the example repo `https://github.com/Rootly-AI-Lab/EventOrOutage` is present as `example_incident.txt` in this repo

```
cp .example.env .env # Add api keys to .env after copying

incidentdiagram -f example_incident.txt  -u https://github.com/Rootly-AI-Lab/EventOrOutage
```

## Develop
```
pip install -e .[dev]
```
To run tests:
```
pytest
```
**Requires:**
* Python > 3.10
* OpenAPI/Gemini/Anthropic API Key

## Examples 📖
Here are a few ways you can use IncidentDiagram:
* `incidentdiagram -f incident.txt  -u https://github.com/Rootly-AI-Lab/EventOrOutage` – will download the code from github and generate a diagram based on the incident summary in incident.txt
* `incidentdiagram -f incident.txt  -u https://github.com/Rootly-AI-Lab/EventOrOutage/tree/main -m gpt-4o` – Use a different model
* `incidentdiagram -iu www.postmortems.com/1345  -u https://github.com/Rootly-AI-Lab/EventOrOutage -m claude-3.5` – Download the incident summary from a URL and generate a diagram

## Stack 🛠️
-   **LLMs:** [Open AI LLMs](https://platform.openai.com/docs/api-reference/models), [Anthropic LLMs](https://docs.anthropic.com/en/api/models-list), [Gemini LLMs](https://ai.google.dev/api/models).
-   **Agent:** HuggingFace smolagents
-   **Data Sources:** External APIs for holidays, news, and event tracking

## Backstory


## Future Improvements
- More charts from incident reports
- Add ollama models

## About the Rootly AI Lab
This project was developed by the Rootly AI Lab. The AI Lab is a fellow-led program designed to redefine reliability and system operations. We develop innovative prototypes, create open-source tools, and produce research reports we share with the community.
![Rootly AI logo](Rootly_AI_Logo_White.png)
