# Resume Graph – AI-Powered Resume Analysis System

An AI-powered resume analysis application built using Python, LangGraph, and Google Gemini.

## Overview

Resume Graph is designed to analyze resume content and provide AI-generated insights to help candidates understand their skills, strengths, and areas for improvement.

The application uses a graph-based workflow to organize the resume analysis process.

## Problem Statement

Job seekers often struggle to identify missing skills, understand resume weaknesses, and evaluate how well their resumes match professional expectations.

This project aims to simplify resume analysis using Generative AI and structured workflows.

## Key Features

- AI-powered resume analysis.
- Resume content processing.
- Graph-based workflow orchestration.
- LLM-powered analysis.
- Interactive application interface.
- Structured analysis and recommendations.

## Technology Stack

- Programming Language: Python
- Frontend: Streamlit
- Workflow Orchestration: LangGraph
- LLM: Google Gemini API
- Environment Configuration: Python environment variables

## How It Works

1. The user provides resume information or uploads a resume.
2. The application extracts or processes the resume content.
3. The content is passed into the graph workflow.
4. LangGraph manages the configured processing steps.
5. The LLM analyzes the resume.
6. The application presents the generated feedback.

## Project Structure

```text
resume-graph/
│
├── app.py
├── graphs/
├── requirements.txt
├── .gitignore
└── README.md
```

## Installation

Clone the repository:

```bash
git clone https://github.com/savuniharika/resume-graph.git
cd resume-graph
```

Create and activate a virtual environment:

```bash
python -m venv .venv
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Configure the required Gemini API key using the environment variable expected by the application.

Run the application:

```bash
streamlit run app.py
```

## Future Improvements

- Add job-description matching.
- Calculate skill-match scores.
- Provide ATS-oriented feedback.
- Add multiple specialized analysis nodes.
- Add structured output validation.
- Include resume improvement suggestions.
- Add evaluation using a test dataset.
