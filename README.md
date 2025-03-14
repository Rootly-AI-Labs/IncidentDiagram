<h1 align="center">Incident Diagram 🗾</h1>
<div align="center">
  <img src="https://img.shields.io/badge/OpenAI_Compatible-Compatible?style=flat-square&logo=openai&labelColor=black&color=white" alt="OpenAI logo">
  <img src="https://img.shields.io/badge/Gemini_Compatible-Compatible?style=flat-square&logo=googlegemini&labelColor=black&color=%238E75B2" alt="Gemini logo">
  <img src="https://img.shields.io/badge/Anthropic_Compatible-Compatible?style=flat-square&logo=anthropic&labelColor=black&color=white" alt="Anthropic logo">
  <img src="https://img.shields.io/badge/smolagents-Compatible?style=flat-square&logo=huggingface&logoColor=%23FF9D00&labelColor=%23FFD21E&color=white" alt="Huggingface logo">
  <img src="https://img.shields.io/badge/Made%20by%20-%20Rootly%20AI%20Lab-blue?style=flat-square" alt="Made by Rootly AI Lab">
  <img src="https://img.shields.io/badge/Project_episode-video?style=flat-square&logo=youtube&logoColor=%23FF0000&color=white" alt="YouTube">
</div>
<br>
Generates a diagram highlighting what happened during an incident by ingesting the retrospective and associated codebase. LLM-powered.

```
$ incidentdiagram -f example_incident.txt  -u https://github.com/Rootly-AI-Labs/EventOrOutage
.
Chart generated in artifacts/incident.md
```

<div align="center">
   <img src="incidentdiagramexample.png" alt="Diagram generated using IncidentDiagram">
</div>

This is a prototype and is not meant for production use.

## Requirements 📋
* `.env` file with OpenAPI/Gemini/Anthropic API Key (at least one)
* Python > 3.10

## Getting started 🚀
```
python -m venv .venv
source .venv/bin/activate
pip install .
cp .example.env .env # Add api keys to .env after copying
incidentdiagram -f example_incident.txt  -u https://github.com/Rootly-AI-Labs/EventOrOutage
```
The example above uses an incident that goes along with the app `https://github.com/Rootly-AI-Labs/EventOrOutage` and a fictive incident retrospective in  `example_incident.txt`.

## Examples 📖
Here are a few ways you can use IncidentDiagram:
* `incidentdiagram -f incident.txt  -u https://github.com/Rootly-AI-Labs/EventOrOutage` – will download the code from github and generate a diagram based on the incident summary in incident.txt
* `incidentdiagram -f incident.txt  -u https://github.com/Rootly-AI-Labs/EventOrOutage/tree/main -m gpt-4o` – Use a different model
* `incidentdiagram -iu www.postmortems.com/1345  -u https://github.com/Rootly-AI-Labs/EventOrOutage -m claude-3.5` – Download the incident summary from a URL and generate a diagram

## Stack 🛠️
-   **LLMs:** [Open AI LLMs](https://platform.openai.com/docs/api-reference/models), [Anthropic LLMs](https://docs.anthropic.com/en/api/models-list), [Gemini LLMs](https://ai.google.dev/api/models).
-   **Agent:** HuggingFace smolagents
-   **Data Sources:** External APIs for holidays, news, and event tracking

## Future Improvements
- More charts from incident reports
- Add ollama models
- The prototype assumes that the incident retrospective mentions the components that were affected

## Backstory for this prototype
Explaining an outage can be challenging, especially for complex incidents in distributed systems, which have become the norm. People also have different preferences for how information is presented, and often, a visual representation is worth a thousand words. However, manually creating application and infrastructure diagrams is time-consuming, making it impractical to do so for every incident. That's why we believe **Incident Diagram** could be a valuable tool for SREs and on-call practitioners, helping them quickly visualize and understand what went wrong.

## About the Rootly AI Labs
This project was developed by the [Rootly AI Labs](https://labs.rootly.ai/). The AI Labs is building the future of system reliability and operational excellence. We operate as an open-source incubator, sharing ideas, experimenting, and rapidly prototyping. We're committed to ensuring our research benefits the entire community.
![Rootly AI logo](https://github.com/Rootly-AI-Labs/EventOrOutage/raw/main/rootly-ai.png)
