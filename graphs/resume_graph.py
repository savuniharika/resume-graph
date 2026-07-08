import os
from pathlib import Path
from typing import TypedDict
import re
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai
from langgraph.graph import StateGraph, END

# -----------------------------
# Load API Key
# -----------------------------
api_key = None

try:
    api_key = st.secrets["GOOGLE_API_KEY"]
except Exception:
    pass

if not api_key:
    env_path = Path(__file__).resolve().parent.parent / ".env"

    if env_path.exists():
        load_dotenv(env_path)

    api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError("GOOGLE_API_KEY not found")

genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-2.5-flash")


# -----------------------------
# State
# -----------------------------
class InterviewState(TypedDict):
    resume: str
    answer: str
    analysis: str
    questions: list
    evaluation: str


# -----------------------------
# Node 1
# -----------------------------
def analyze_resume(resume):

    prompt = f"""
You are an HR recruiter.

Analyze the following resume.

Resume:
{resume}

Give:
- Summary
- Strengths
- Weaknesses
- Skills
"""

    response = model.generate_content(prompt)

    return response.text


# -----------------------------
# Node 2
# -----------------------------
def generate_questions(resume):

    prompt = f"""
You are a Senior Technical Interviewer at a top software company.

Candidate Resume:
{resume}

Generate exactly 5 interview questions.

Requirements:
- Return ONLY the 5 numbered questions.
- No introduction or conclusion.
- Questions must be based only on the resume.
- Do not assume any experience not mentioned.
- Mix the questions as follows:
  1. One fundamental technical question.
  2. One project-based question.
  3. One practical coding or AI design question.
  4. One problem-solving or debugging question.
  5. One HR/behavioral question.
- Questions should sound like a real interviewer.
- Keep each question under 40 words.
"""

    response = model.generate_content(prompt)

    text = response.text

    questions = []

    for line in text.split("\n"):
        line = line.strip()

        if not line:
            continue

        # Remove numbering like 1. 2. 3.
        line = re.sub(r'^\d+\.\s*', '', line)

        # Skip unwanted lines
        if "interview questions" in line.lower():
            continue
        if "here are" in line.lower():
            continue

        questions.append(line)

    return questions[:5]
# -----------------------------
# Node 3
# -----------------------------
def evaluate_answer(analysis,questions,answer):

    prompt = f"""
Resume Analysis:

{analysis}

Interview Questions:

{questions}

Candidate Answer:

{answer}

Evaluate the answer.

give:

- Score out of 10
- Strengths
- Weaknesses
- suggestions
"""

    response = model.generate_content(prompt)

    return response.text


# -----------------------------
# Build Graph
# -----------------------------
builder = StateGraph(InterviewState)

builder.add_node("analysis", analyze_resume)
builder.add_node("questions", generate_questions)
builder.add_node("evaluation", evaluate_answer)

builder.set_entry_point("analysis")

builder.add_edge("analysis", "questions")
builder.add_edge("questions", "evaluation")
builder.add_edge("evaluation", END)

graph = builder.compile()