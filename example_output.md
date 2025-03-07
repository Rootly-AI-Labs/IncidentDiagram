```mermaid
timeline
    title Timeline Chart
    14_50 : Broken Code Change Deployed
    18_14 : Pre-Prod Errors Detected
    19_08 : Production Deployment Initiated
    19_09 : Production Outage Begins
    19_27 : Rollback Executed
```

```mermaid

%% Mermaid diagram with a hand drawn look (simulated by dashed red stroke)
flowchart TD
    CLI[CLI<br/><sub>Entry point for command line interactions</sub>]
    SingleAnomalyAgent[SingleAnomalyAgent<br/><sub>Processes single anomaly instance</sub>]
    BulkAnomalyAgent[BulkAnomalyAgent<br/><sub>*Library update introduced a bug*</sub>]
    NaiveAnomalyDetecter[NaiveAnomalyDetecter<br/><sub>Detects anomalies from CSV input</sub>]
    LLMUtils[LLMUtils<br/><sub>Configures LLM models</sub>]
    MarkdownGenerator[MarkdownGenerator<br/><sub>Generates markdown reports and diagrams</sub>]
    FileUtils[FileUtils<br/><sub>Saves markdown files</sub>]
    Utils[Utils<br/><sub>General utilities and env loading</sub>]
    SyntheticData[SyntheticData<br/><sub>Generates synthetic traffic data</sub>]
    SyntheticDataGenerator[SyntheticDataGenerator<br/><sub>Triggers synthetic data generation</sub>]
    CalendarificAPITool[CalendarificAPITool<br/><sub>Fetches holiday/event data</sub>]
    HolidaysAPITool[HolidaysAPITool<br/><sub>Fetches holiday data</sub>]
    ConfigFiles["Configuration Files<br/><sub>*The .env file was removed from version control, leading to startup failures on production machines.*</sub>"]

    %% Relationships
    CLI --> SingleAnomalyAgent
    CLI --> BulkAnomalyAgent
    CLI --> NaiveAnomalyDetecter
    CLI --> MarkdownGenerator

    BulkAnomalyAgent --> LLMUtils
    BulkAnomalyAgent --> Utils
    BulkAnomalyAgent --> HolidaysAPITool
    BulkAnomalyAgent --> CalendarificAPITool

    SingleAnomalyAgent --> LLMUtils
    SingleAnomalyAgent --> Utils
    SingleAnomalyAgent --> HolidaysAPITool
    SingleAnomalyAgent --> CalendarificAPITool

    NaiveAnomalyDetecter --> CLI
    NaiveAnomalyDetecter --> BulkAnomalyAgent

    MarkdownGenerator --> FileUtils

    SyntheticDataGenerator --> SyntheticData
    SyntheticDataGenerator --> MarkdownGenerator

    SyntheticData --> MarkdownGenerator

    %% Highlight affected components with hand-drawn style
    class BulkAnomalyAgent,ConfigFiles affected;
    classDef affected fill:#fdd,stroke:#f00,stroke-width:2px,stroke-dasharray: 5 5;

```
