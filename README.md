
# Incident Diagram 🥳☄️
IncidentDiagram is a tool that leverages LLMs to help visualize details in a post-incident analysis or post-mortem.

The initial prototype assumes that the incident review mentions the components that were affected.

```
$ incidentdiagram -f incident.txt  -u https://github.com/Rootly-AI-Lab/EventOrOutage/tree/main -m claude-3.5
.
.
Chart generated in artifacts/incident.md
```

## Get started 🚀
```
python -m venv .venv
source .venv/bin/activate
pip install .
echo "A lot of details about the incident" > incident.txt
incidentdiagram -f incident.txt  -u https://github.com/Rootly-AI-Lab/EventOrOutage/tree/main -m claude-3.5
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
* `incidentdiagram -f incident.txt  -u https://github.com/Rootly-AI-Lab/EventOrOutage/tree/main -m claude-3.5` – will download the code from github and generate a diagram based on the incident summary in incident.txt
* `incidentdiagram -f incident.txt  -u https://github.com/Rootly-AI-Lab/EventOrOutage/tree/main -m gpt-4o` – Use a different model
* `incidentdiagram -iu www.postmortems.com/1345  -u https://github.com/Rootly-AI-Lab/EventOrOutage/tree/main -m claude-3.5` – Download the incident summary from a URL and generate a diagram

## Stack 🛠️
-   **LLMs:** GPT-4, Claude, Gemini and self-hosted (Deepseek).
-   **Agent:** HuggingFace smolagents
-   **Data Sources:** External APIs for holidays, news, and event tracking

## Backstory


## Future Improvements
- More charts from incident reports

## About the Rootly AI Lab
This project was developed by the Rootly AI Lab. The AI Lab is a fellow-led program designed to redefine reliability and system operations. We develop innovative prototypes, create open-source tools, and produce research reports we share with the community.
![Rootly AI logo](Rootly_AI_Logo_White.png)
