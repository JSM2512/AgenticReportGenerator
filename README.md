# Agent Based Report Generation Streamlit App

## Overview

This project is a Streamlit web application that generates structured reports using a multi-stage orchestration workflow. The system leverages LLMs and a modular graph-based approach to plan, parallelize, and synthesize report sections on any user-specified topic.

## Features

- **Interactive Streamlit Interface**: Enter a topic and generate AI-curated multi-section reports in your browser.
- **Orchestrator-Worker Design**: Tasks are broken into subtasks (sections), assigned to parallel AI workers, and results are synthesized automatically.
- **Customizable Topics**: Flexible for any topic specified by the user.
- **Graph-Based Workflow**: Visualizes and manages report generation steps as a directed state graph.

## Tech Stack

```text
- Python 3.10+
- Streamlit (UI)
- LangGraph (workflow orchestration)
- LangChain-Groq (LLM integration)
- Pydantic (data modeling)
- python-dotenv (environment variable management)
```

## Installation
To install the MultiToolAgent project, follow these steps:
1. Clone the repository:
   ```bash
   git clone https://github.com/JSM2512/AgenticReportGenerator.git
   ```
2. Navigate into the project directory with environment creation:
   ```bash
   # Using conda
   conda create -n venv python=3.12
   conda activate venv/
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage with Streamlit
To use the Code with Streamlit:
1. Go to terminal:
   ```python
   cd Code
   streamlit run app.py
   ```
2. This will run the app on your browser.

